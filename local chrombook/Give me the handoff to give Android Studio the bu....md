Here is the complete **Android Studio Build & Architecture Handoff Spec**. You can copy and paste this directly into Android Studio's AI assistant (Gemini in Android Studio) or use it to guide your code generation.

# **📱 Android Application Handoff Specification**

## **1\. Project Overview & Architecture**

* **Project Name:** PowerMonitor Mobile Client  
* **Firebase Project ID:** mr-pats-clouds  
* **Architecture Pattern:** MVVM (Model-View-ViewModel) with Clean Architecture using **Jetpack Compose**, **Kotlin Coroutines & Flow**, and **Hilt** (optional/preferred for DI).  
* **Core Objective:** Authenticate against a local authentication server, exchange a custom JWT token with Firebase Auth, and stream real-time workstation telemetry metrics from Firestore.

## **2\. Dependencies (build.gradle.kts)**

Ensure the following dependencies are included in app/build.gradle.kts:

Kotlin  
plugins {  
    alias(libs.plugins.android.application)  
    alias(libs.plugins.kotlin.android)  
    id("com.google.gms.google-services")  
}

dependencies {  
    // Firebase BoM  
    implementation(platform("com.google.firebase:firebase-bom:33.1.0"))  
    implementation("com.google.firebase:firebase-auth")  
    implementation("com.google.firebase:firebase-firestore")

    // Networking (Retrofit \+ OkHttp)  
    implementation("com.squareup.retrofit2:retrofit:2.11.0")  
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")  
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // Jetpack Compose & ViewModel  
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.0")  
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.0")  
    implementation(platform("androidx.compose:compose-bom:2024.05.00"))  
    implementation("androidx.compose.material3:material3")  
}

## **3\. Network & Security Configuration**

### **AndroidManifest.xml**

Add internet permissions and enable cleartext traffic for local testing (\[http://10.0.2.2:8080\](http://10.0.2.2:8080) for Android Emulator or local network IP):

XML  
\<manifest xmlns:android\="http://schemas.android.com/apk/res/android"\>  
    \<uses-permission android:name\="android.permission.INTERNET" /\>  
    \<uses-permission android:name\="android.permission.ACCESS\_NETWORK\_STATE" /\>

    \<application  
        android:usesCleartextTraffic\="true"  
        ... \>  
    \</application\>  
\</manifest\>

## **4\. Auth Server API Integration**

### **Base URL Definition**

* **Android Emulator:** \[http://10.0.2.2:8080/\](http://10.0.2.2:8080/)  
* **Physical Device (Same Wi-Fi):** http://\<YOUR\_LOCAL\_LINUX\_IP\>:8080/

### **Auth Service Interface (AuthApiService.kt)**

Kotlin  
import retrofit2.http.Body  
import retrofit2.http.POST

data class LoginRequest(  
    val username: String \= "admin",  
    val password: String \= "secret123"  
)

data class LoginResponse(  
    val status: String,  
    val token: String,  
    val uid: String  
)

interface AuthApiService {  
    @POST("api/login")  
    suspend fun login(@Body request: LoginRequest): LoginResponse  
}

## **5\. Firebase Auth Custom Token Exchange**

When the user logs in, retrieve the custom token from the Python auth server and pass it to Firebase Auth:

Kotlin  
import com.google.firebase.auth.FirebaseAuth  
import com.google.firebase.auth.FirebaseUser  
import kotlinx.coroutines.tasks.await

class AuthRepository(private val apiService: AuthApiService) {  
    private val firebaseAuth \= FirebaseAuth.getInstance()

    suspend fun authenticate(username: String, password: String): Result\<FirebaseUser\> {  
        return try {  
            // 1\. Get Custom Token from Auth Server  
            val response \= apiService.login(LoginRequest(username, password))  
            val customToken \= response.token

            // 2\. Sign in to Firebase Auth with Custom Token  
            val authResult \= firebaseAuth.signInWithCustomToken(customToken).await()  
            val user \= authResult.user ?: throw Exception("Firebase user was null")

            Result.success(user)  
        } catch (e: Exception) {  
            Result.failure(e)  
        }  
    }  
}

## **6\. Firestore Real-Time Data Stream**

The Firestore security rules require a valid auth token with custom claim role \== 'admin'.

### **Telemetry Model & Data Stream Repository (TelemetryRepository.kt)**

Kotlin  
import com.google.firebase.firestore.FirebaseFirestore  
import kotlinx.coroutines.channels.awaitClose  
import kotlinx.coroutines.flow.Flow  
import kotlinx.coroutines.flow.callbackFlow

data class TelemetryData(  
    val device\_id: String \= "",  
    val cpu\_usage: Double \= 0.0,  
    val ram\_usage: Double \= 0.0,  
    val timestamp: Long \= 0L,  
    val status: String \= "UNKNOWN"  
)

class TelemetryRepository {  
    private val db \= FirebaseFirestore.getInstance()

    fun streamTelemetry(deviceId: String \= "WORKSTATION-MAIN"): Flow\<TelemetryData?\> \= callbackFlow {  
        val docRef \= db.collection("telemetry").document(deviceId)

        val listener \= docRef.addSnapshotListener { snapshot, error \-\>  
            if (error \!= null) {  
                close(error)  
                return@addSnapshotListener  
            }

            if (snapshot \!= null && snapshot.exists()) {  
                val data \= snapshot.toObject(TelemetryData::class.java)  
                trySend(data)  
            } else {  
                trySend(null)  
            }  
        }

        awaitClose { listener.remove() }  
    }  
}

## **7\. UI Dashboard Contract (Jetpack Compose ViewState)**

Kotlin  
sealed interface DashboardUiState {  
    object Loading : DashboardUiState  
    object Unauthenticated : DashboardUiState  
    data class Success(val telemetry: TelemetryData) : DashboardUiState  
    data class Error(val message: String) : DashboardUiState  
}

### **ViewModel Logic Example (TelemetryViewModel.kt)**

Kotlin  
import androidx.lifecycle.ViewModel  
import androidx.lifecycle.viewModelScope  
import kotlinx.coroutines.flow.MutableStateFlow  
import kotlinx.coroutines.flow.StateFlow  
import kotlinx.coroutines.flow.asStateFlow  
import kotlinx.coroutines.launch

class TelemetryViewModel(  
    private val authRepository: AuthRepository,  
    private val telemetryRepository: TelemetryRepository  
) : ViewModel() {

    private val \_uiState \= MutableStateFlow\<DashboardUiState\>(DashboardUiState.Unauthenticated)  
    val uiState: StateFlow\<DashboardUiState\> \= \_uiState.asStateFlow()

    fun performLoginAndStream(username: String \= "admin", password: String \= "secret123") {  
        viewModelScope.launch {  
            \_uiState.value \= DashboardUiState.Loading  
              
            val authResult \= authRepository.authenticate(username, password)  
            authResult.onSuccess {  
                // Auth successful \-\> Start listening to Firestore real-time stream  
                telemetryRepository.streamTelemetry("WORKSTATION-MAIN").collect { telemetry \-\>  
                    if (telemetry \!= null) {  
                        \_uiState.value \= DashboardUiState.Success(telemetry)  
                    } else {  
                        \_uiState.value \= DashboardUiState.Error("No telemetry data found for device.")  
                    }  
                }  
            }.onFailure { exception \-\>  
                \_uiState.value \= DashboardUiState.Error(exception.localizedMessage ?: "Authentication failed")  
            }  
        }  
    }  
}

## **8\. Verification & Test Workflow**

> 1. Ensure python3 auth\_server.py is running on Linux on port 8080\.  
> 2. Run the Android app in the emulator.  
> 3. Trigger performLoginAndStream().  
> 4. Confirm signInWithCustomToken() succeeds and the UI receives real-time updates pushed to the /telemetry/WORKSTATION-MAIN Firestore document.
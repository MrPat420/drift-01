# gemini-conversation-selection
Exported on: 8/11/2026, 1:28:54 PM

---

**Gemini:**
Yes, **you need to execute them on your workstation terminal**.

Since I can't run code directly on your local machine, you'll paste these commands into your shell to write the file, launch the auth service, and test token generation.

Here is the step-by-step sequence to execute right now:

### Step 1: Write `auth_server.py`

Copy and paste this entire block into your terminal prompt to generate the microservice file:

```
cat << 'EOF' > auth_server.py
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import firebase_admin
from firebase_admin import credentials, auth

SERVICE_ACCOUNT_FILE = "service_account.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)

class AuthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/login":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                username = data.get("username")
                password = data.get("password")

                # Credential check
                if username == "admin" and password == "secret123":
                    uid = f"user_{username}"
                    custom_claims = {
                        "role": "admin",
                        "monitored_devices": ["WORKSTATION-MAIN"]
                    }
                    
                    # Mint Firebase Custom Token
                    token_bytes = auth.create_custom_token(uid, custom_claims)
                    custom_token = token_bytes.decode('utf-8')

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    response = {"status": "success", "token": custom_token, "uid": uid}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AuthHandler)
    print(f"[AUTH SERVER] Running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
EOF

```

### Step 2: Start the Auth Microservice

Run the auth server in the background:

```
python3 auth_server.py &

```

*(You will see `[AUTH SERVER] Running on port 8080...` printed to the console.)*

### Step 3: Test Token Minting with `curl`

Send a test authentication request from your terminal:

```
curl -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}'

```

If successful, it will return a JSON object containing your newly minted, cryptographically signed Firebase JWT `token`!

Want to deploy this Auth Provider as a serverless Cloud Function on GCP?Yes

---


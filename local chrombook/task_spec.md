

### **task\_spec.md (Payload 01\)**

Markdown  
\# TASK SPECIFICATION: Payload 01 (Core Gateway Scaffold)  
**\*\*TARGET ARCHITECTURE:\*\*** GCP Cloud Run (simian420) / FastAPI / Firebase  
**\*\*OBJECTIVE:\*\*** Stand up the \`/platform/core/\` directory, define the \`BaseModule\` abstract contract, and build the initial API Gateway with Firebase Auth middleware.

\#\# Execution Steps for Cline:  
1\. Create the base directory structure:  
   \- \`platform/\`  
   \- \`platform/core/\`  
   \- \`platform/modules/\`  
2\. Create the following files with the exact code provided below.  
3\. Initialize a virtual environment in \`platform/\`, activate it, and install \`requirements.txt\`.  
4\. Run a syntax check to verify the build. Do not start the server yet.

\---

\#\#\# File 1: \`platform/requirements.txt\`  
\`\`\`text  
fastapi\>=0.103.0  
uvicorn\>=0.23.2  
firebase-admin\>=6.2.0  
google-cloud-firestore\>=2.11.0  
pydantic\>=2.4.2

### **File 2: platform/core/module.py**

Python  
from abc import ABC, abstractmethod  
from fastapi import APIRouter

class BaseModule(ABC):  
    """  
    Abstract contract for all plug-and-play modules in the C2 Gateway.  
    Any new tool (Web2MD, Telemetry, etc.) MUST inherit from this class.  
    """  
      
    @property  
    @abstractmethod  
    def name(self) \-\> str:  
        """The canonical name of the module (e.g., 'web2md')"""  
        pass

    @property  
    @abstractmethod  
    def firestore\_collections(self) \-\> list\[str\]:  
        """List of Firestore collections this module manages."""  
        pass

    @abstractmethod  
    def router(self) \-\> APIRouter:  
        """Returns the FastAPI APIRouter containing the module's endpoints."""  
        pass

### **File 3: platform/core/auth.py**

Python  
from fastapi import Depends, HTTPException, status  
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
import firebase\_admin  
from firebase\_admin import credentials, auth

\# Initialize Firebase Admin SDK  
\# Note: On GCP Cloud Run, default service accounts handle authentication automatically.  
\# For local dev, ensure GOOGLE\_APPLICATION\_CREDENTIALS is set in the environment.  
if not firebase\_admin.\_apps:  
    firebase\_admin.initialize\_app()

security \= HTTPBearer()

def verify\_token(credentials: HTTPAuthorizationCredentials \= Depends(security)):  
    """  
    Middleware to intercept Firebase JWTs, verify them, and inject the user payload.  
    """  
    token \= credentials.credentials  
    try:  
        decoded\_token \= auth.verify\_id\_token(token)  
        return decoded\_token  
    except Exception as e:  
        raise HTTPException(  
            status\_code=status.HTTP\_401\_UNAUTHORIZED,  
            detail="Invalid or expired authentication credentials",  
            headers={"WWW-Authenticate": "Bearer"},  
        )

### **File 4: platform/core/gateway.py**

Python  
from fastapi import FastAPI, Depends  
from core.auth import verify\_token

\# Initialize the main C2 Gateway App  
app \= FastAPI(  
    title="C2 Unified Gateway",   
    version="1.0.0",  
    description="Modular Plug-and-Play API Gateway for simian420 Architecture."  
)

@app.get("/api/health")  
def health\_check():  
    return {"status": "operational", "node": "simian420-gateway"}

\# NOTE FOR LATER: Modules will be dynamically mounted here.  
\# Example:   
\# from modules.web2md.module import Web2MDModule  
\# web2md \= Web2MDModule()  
\# app.include\_router(web2md.router(), prefix=f"/api/{web2md.name}", dependencies=\[Depends(verify\_token)\])

\---

Run that through the bench tech. If Cline kicks back any dependency errors or pathing issues, dump the raw error log here and I'll RCA it. If the build goes green, give me the nod and we'll rack the Web2MD/Gemini pipeline as Module 01\.

\<FollowUp label="Build is green. Prep Payload 02 for Web2MD?" query="Cline executed Payload 01 successfully. The build is green. Generate Payload 02 to port the Web2MD/Gemini script into the new BaseModule structure."/\>  

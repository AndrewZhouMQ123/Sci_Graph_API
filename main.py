from fastapi import FastAPI, Depends, Header, HTTPException, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from routers.plot_router import plot_router
from routers.fit_router import fit_router
from google.cloud import iam_v3
import os
from dotenv import load_dotenv
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

if os.getenv("CI") != "true":
    load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
REQUIRED_ROLE = "roles/run.invoker"
RESOURCE = f"projects/{GCP_PROJECT_ID}/sciencegraphapi"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://andrewsonlinenotes.vercel.app"],
    allow_methods=["*"],
    allow_headers=["Authorization"],  # Only allow the Authorization header
)

# --- Authentication & Authorization Dependencies ---

async def get_current_user(request: FastAPIRequest, authorization: str = Header(None)):
    """Verifies Google ID token and extracts the user's email."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split("Bearer ")[1]
    try:
        request = google_requests.Request()
        idinfo = id_token.verify_oauth2_token(token, request, GOOGLE_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(status_code=401, detail="Invalid token issuer")
        user_email = idinfo['email']
        if not user_email:
            raise HTTPException(status_code=401, detail="Could not retrieve user email from token")
        return {"email": user_email}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")
    except Exception as e:
        print(f"Error verifying token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during token verification")

async def authorize_action(user: dict = Depends(get_current_user)):
    """Checks if the authenticated user has the required IAM role."""
    try:
        client = iam_v3.PolicyBindingsClient()
        request = iam_v3.ListPolicyBindingsRequest(parent=RESOURCE)
        response = client.list_policy_bindings(request=request)
        for binding in response.policy_bindings:
            if binding.role == REQUIRED_ROLE and f"user:{user['email']}" in binding.principals:
                return user
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")

    except Exception as e:
        print(f"IAM v3 check failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during authorization")

# --- Routes ---

@app.get("/")
async def main_route():
    return {"msg": "Hello World"}

# Routers
app.include_router(plot_router, dependencies=[Depends(authorize_action)])
app.include_router(fit_router, dependencies=[Depends(authorize_action)])
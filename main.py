from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.plot_router import plot_router
from routers.fit_router import fit_router
from google.cloud import iam_v3
import os
from dotenv import load_dotenv

# Load .env when not in CI
if os.getenv("CI") != "true":
    load_dotenv()

# Constants
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REQUIRED_ROLE = "roles/run.invoker"
RESOURCE = f"projects/{GCP_PROJECT_ID}/sciencegraphapi"

# FastAPI instance
app = FastAPI()

# CORS Middleware (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Authentication & Authorization Dependencies ---

async def get_current_user(request: Request):
    """Extracts the authenticated user's email from Cloud Run headers."""
    user_header = request.headers.get("x-goog-authenticated-user-email")
    if not user_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        email = user_header.split(":")[-1]
        return {"email": email}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid user header format")

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
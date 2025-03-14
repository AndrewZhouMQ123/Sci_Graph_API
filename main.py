from fastapi import FastAPI, Depends, Request, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from routers.plot_router import plot_router
from routers.fit_router import fit_router
from routers.imageTransform_router import imageTransform_router
from routers.solver_router import solver_router
from mydb import APIKey, save_api_key, verify_api_key, get_db, mark_expired_keys_inactive, sweep_expired_keys, init_db
import datetime
import secrets
from fastapi.middleware.cors import CORSMiddleware

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
engine, SessionLocal = init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
  try:
    with engine.connect() as connection:
      print("Database connection successful")
    yield
  except Exception as e:
    print(f"Failed to connect: {e}")
    raise Exception(f"Database connection failed: {e}")
  finally:
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plot_router, dependencies=[Depends(verify_api_key)])
app.include_router(fit_router, dependencies=[Depends(verify_api_key)])
app.include_router(imageTransform_router, dependencies=[Depends(verify_api_key)])
app.include_router(solver_router, dependencies=[Depends(verify_api_key)])

@app.get("/")
async def read_main():
  return {"msg": "Hello World"}

@app.post("/generate_api_key")
async def generate_new_key(request: Request, db: Session = Depends(get_db)):
  # data = await request.json()
  # token = data.get("token")
  # if not token:
  #   raise HTTPException(status_code=400, detail="Missing payment token")
  # Call the cleanup on each key generation
  mark_expired_keys_inactive(db)
  sweep_expired_keys(db)

  new_api_key = secrets.token_hex(32)
  save_api_key(new_api_key, db)
  return {"api_key": new_api_key}

@app.post("/endAPIsession")
def endAPIsession(api_key: str, db: Session = Depends(get_db)):
  api_key_record = db.query(APIKey).filter_by(key=api_key, active=True).first()
  if not api_key_record:
    raise HTTPException(status_code=401, detail="Invalid API Key")
  if api_key_record.session_active:
    session_duration = datetime.datetime.now() - api_key_record.session_start
    hours_used = session_duration.total_seconds() / 3600
    api_key_record.hours_remaining -= int(hours_used)
    api_key_record.session_active = False
    db.commit()
  return {"message": "Session ended successfully", "hours_remaining": api_key_record.hours_remaining}
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from routers.plot_router import plot_router
from routers.fit_router import fit_router
from routers.imageTransform_router import imageTransform_router
from routers.solver_router import solver_router
from mydb import save_api_key, verify_api_key, generate_api_key, get_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
  try:
    with engine.connect() as connection:
      print("Connection successful!")
  except Exception as e:
    print(f"Failed to connect: {e}")
    raise Exception(f"Database connection failed: {e}")
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(plot_router, dependencies=[Depends(verify_api_key)])
app.include_router(fit_router, dependencies=[Depends(verify_api_key)])
app.include_router(imageTransform_router, dependencies=[Depends(verify_api_key)])
app.include_router(solver_router, dependencies=[Depends(verify_api_key)])

@app.get("/")
async def read_main():
  return {"msg": "Hello World"}

@app.post("/generate_api_key")
def generate_new_key(token: str, db: Session = Depends(get_db)):
  if token:
    api_key = generate_api_key()
    save_api_key(api_key, db)
    return {"api_key": api_key}
  else:
    raise Exception("Unauthorized access")
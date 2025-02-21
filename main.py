from fastapi import FastAPI, Depends, Request, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from routers.plot_router import plot_router
from routers.fit_router import fit_router
from routers.imageTransform_router import imageTransform_router
from routers.solver_router import solver_router
from mydb import save_api_key, verify_api_key, generate_api_key, get_db, mark_expired_keys_inactive, sweep_expired_keys, engine
import stripe

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

stripe.api_key = "your_stripe_secret_key"

app.include_router(plot_router, dependencies=[Depends(verify_api_key)])
app.include_router(fit_router, dependencies=[Depends(verify_api_key)])
app.include_router(imageTransform_router, dependencies=[Depends(verify_api_key)])
app.include_router(solver_router, dependencies=[Depends(verify_api_key)])

@app.get("/")
async def read_main():
  return {"msg": "Hello World"}

@app.post("/create-checkout-session")
def create_checkout_session():
  try:
    session = stripe.checkout.Session.create(
      payment_method_types=["card"],
      mode="payment",
      success_url="https://yourwebsite.com/success?session_id={CHECKOUT_SESSION_ID}",
      cancel_url="https://yourwebsite.com/cancel",
      line_items=[{
        "price_data": {
          "currency": "usd",
          "product_data": {"name": "API Access"},
          "unit_amount": 1000,  # $10.00
        },
        "quantity": 1,
      }])
    return {"sessionId": session.id}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_api_key")
async def generate_new_key(request: Request, db: Session = Depends(get_db)):
  data = await request.json()
  token = data.get("token")
  # Call the cleanup on each key generation
  mark_expired_keys_inactive(db)
  sweep_expired_keys(db)
  if not token:
    raise HTTPException(status_code=400, detail="Missing payment token")
  try:
    # Verify the session ID with Stripe
    session = stripe.checkout.Session.retrieve(token)
    if session.payment_status == "paid":
      api_key = generate_api_key()
      save_api_key(api_key, db)
      return {"api_key": api_key}
    else:
      raise HTTPException(status_code=403, detail="Payment not completed")
  except stripe.error.StripeError:
    raise HTTPException(status_code=400, detail="Invalid payment token")

@app.get("/endAPIsession")
def endAPIsession():
  # set session active to false
  # subtract datetime now from session_start to get time
  # update hours_remaining by subtracting time
  # db commit changes 
  return
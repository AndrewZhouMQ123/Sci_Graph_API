from sqlalchemy import Integer, create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os
import datetime
from fastapi import HTTPException, Depends, Header

Base = declarative_base()

def init_db():
  if os.getenv('CI') == 'true':
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"
  else:
    load_dotenv()
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    DATABASE_URL = (f"postgresql+psycopg2://postgres:{PASSWORD}@{HOST}:5432/postgres?sslmode=require")
  engine = create_engine(DATABASE_URL, echo=True)
  Base.metadata.create_all(bind=engine)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  return engine, SessionLocal

engine, SessionLocal = init_db()

class APIKey(Base):
  __tablename__ = "api_keys"
  id = Column(Integer, primary_key=True, index=True)
  key = Column(String, unique=True, nullable=False)
  active = Column(Boolean, default=True)
  expire = Column(DateTime, nullable=False)
  hours_remaining = Column(Integer, nullable=False)
  session_start = Column(DateTime, default=None)
  session_active = Column(Boolean, default=False)

  def is_expired(self):
    return datetime.datetime.now() >= self.expire

def get_db():
  if not engine:
    raise RuntimeError("Database not initialized! Call init_db() first.")
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def save_api_key(api_key: str, db: Session):
  expire_date = datetime.datetime.now() + datetime.timedelta(days=30)
  db_key = APIKey(key=api_key, active=True, expire = expire_date, hours_remaining = 100)
  db.add(db_key)
  db.commit()

# Headers for testing, use JWT tokens in the future
def verify_api_key(api_key: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)) -> bool:
  db_api_key = db.query(APIKey).filter_by(key=api_key, active=True).first()
  if not db_api_key.key:
    raise HTTPException(status_code=401, detail="Invalid API Key")
  if db_api_key.expire < datetime.datetime.now():
    raise HTTPException(status_code=403, detail="API key has expired")
  if db_api_key.hours_remaining <= 0:
    raise HTTPException(status_code=403, detail="API key usage limit has been reached")
  db_api_key.session_active = True
  db_api_key.session_start = datetime.datetime.now()
  db.commit()
  return True

def mark_expired_keys_inactive(db: Session):
  # Get all keys where the expiration date has passed and set them to inactive
  expired_keys = db.query(APIKey).filter(APIKey.expire < datetime.datetime.now(), APIKey.active == True).all()
  for key in expired_keys:
    key.active = False
    db.commit()  # Commit the change to the database

def sweep_expired_keys(db: Session):
  # Sweep (delete) keys that are inactive
  expired_keys = db.query(APIKey).filter(APIKey.active == False).all()
  for key in expired_keys:
    db.delete(key)
  db.commit()  # Commit the delete operations
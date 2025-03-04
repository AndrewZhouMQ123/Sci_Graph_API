from sqlalchemy import Integer, create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os
import datetime
from fastapi import HTTPException, Depends
import secrets

Base = declarative_base()
engine = None
SessionLocal = None

def init_db():
  global engine, SessionLocal
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

def generate_api_key():
  return secrets.token_hex(32)

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
    return datetime.now() >= self.expire

def get_db():
  if not engine:
    raise RuntimeError("Database not initialized! Call init_db() first.")
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def save_api_key(api_key: str, db: Session):
  expire_date = datetime.now() + datetime.timedelta(days=30)
  db_key = APIKey(key=api_key, active=True, expire = expire_date, hours_remaining = 100)
  db.add(db_key)
  db.commit()

def verify_api_key(api_key: str, db: Session = Depends(get_db)):
  api_key_record = db.query(APIKey).filter_by(key=api_key, active=True).first()
  if not api_key_record.key:
    raise HTTPException(status_code=401, detail="Invalid API Key")
  if api_key.expire < datetime.now():
    raise HTTPException(status_code=403, detail="API key has expired")
  if api_key.hours_remaining <= 0:
    raise HTTPException(status_code=403, detail="API key usage limit has been reached")
  api_key_record.session_active = True
  api_key_record.session_start = datetime.now()
  db.commit()
  return True

def mark_expired_keys_inactive(db: Session):
  # Get all keys where the expiration date has passed and set them to inactive
  expired_keys = db.query(APIKey).filter(APIKey.expire < datetime.now(), APIKey.active == True).all()
  for key in expired_keys:
    key.active = False
    db.commit()  # Commit the change to the database

def sweep_expired_keys(db: Session):
  # Sweep (delete) keys that are inactive
  expired_keys = db.query(APIKey).filter(APIKey.active == False).all()
  for key in expired_keys:
    db.delete(key)
  db.commit()  # Commit the delete operations
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import datetime
from fastapi import HTTPException, Header, Depends
import secrets

Base = declarative_base()
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class APIKey(Base):
  __tablename__ = "api_keys"
  key = Column(String, primary_key=True, index=True)
  active = Column(Boolean, default=True)
  expires_at = Column(DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(days=30))

Base.metadata.create_all(bind=engine)

def generate_api_key():
  return secrets.token_hex(32)

def save_api_key(api_key: str, db: Session):
  expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
  db_key = APIKey(key=api_key, active=True, expires_at=expires_at)
  db.add(db_key)
  db.commit()

def verify_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
  api_key = db.query(APIKey).filter_by(key=x_api_key, active=True).first()
  if not api_key:
      raise HTTPException(status_code=401, detail="Invalid API Key")
  return True
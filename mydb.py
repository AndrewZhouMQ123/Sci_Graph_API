from sqlalchemy import Integer, create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os
import datetime
from fastapi import HTTPException, Header, Depends
import secrets

Base = declarative_base()
load_dotenv()
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
DATABASE_URL = f"postgresql+psycopg2://postgres:{PASSWORD}@{HOST}:{5432}/postgres?sslmode=require"
engine = create_engine(
  DATABASE_URL,
  pool_size=10,
  max_overflow=5,
  pool_pre_ping=True,
  pool_recycle=3600
)

def generate_api_key():
  return secrets.token_hex(32)

class APIKey(Base):
  __tablename__ = "api_keys"
  id = Column(Integer, primary_key=True, index=True)
  key = Column(String, unique=True, nullable=False)
  active = Column(Boolean, default=True)
  expires_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30))

def init_db():
  Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

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
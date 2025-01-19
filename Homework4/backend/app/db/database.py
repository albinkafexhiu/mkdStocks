from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()

# Get DATABASE_URL from Heroku or build from individual vars
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Handle Heroku's postgres:// vs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # Local development configuration
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Add SSL requirement for Heroku
if os.getenv('DATABASE_URL'):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=30,
        max_overflow=40,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
            "sslmode": "require"
        }
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=30,
        max_overflow=40,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=3600
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
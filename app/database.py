import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Railway provides MYSQL_URL, DATABASE_URL, or MYSQLPRIVATEURL
raw_db_url = (
    os.getenv("DATABASE_URL")
    or os.getenv("MYSQL_URL")
    or os.getenv("MYSQLPRIVATEURL")
)

if raw_db_url:
    # Ensure pymysql driver is used for MySQL URLs
    if raw_db_url.startswith("mysql://"):
        database_url = raw_db_url.replace("mysql://", "mysql+pymysql://", 1)
    else:
        database_url = raw_db_url
else:
    # Local fallback to SQLite if MySQL is not configured
    database_url = "sqlite:///./naviora.db"

# SQLite requires check_same_thread=False
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration - Azure SQL Server
DB_HOST = os.getenv('DB_HOST', '172.190.157.142')
DB_PORT = os.getenv('DB_PORT', '1433')
DB_NAME = os.getenv('DB_NAME', 'dbNPS')
DB_USER = os.getenv('DB_USER', 'user-nps')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Create connection string for SQL Server
# Usando pyodbc para SQL Server
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to False in production
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

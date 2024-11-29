# services/recipe_service/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os

# Database configuration
DB_USER = os.getenv("MYSQL_USER", "recipe_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "recipe_password")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "recipe_db")
MYSQL_ALLOW_EMPTY_PASSWORD=os.getenv("MYSQL_ALLOW_EMPTY_PASSWORD", "yes")

# Create MySQL URL (with proper password encoding)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# print("Database string: ", SQLALCHEMY_DATABASE_URL)
# Create engine with MySQL-specific configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", 10)),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 10)),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", 300)),
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", 3600)),
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    pool_pre_ping=True,  # Enables connection health checks
    connect_args={
        'charset': 'utf8mb4',  # Support full UTF-8 character set
        'connect_timeout': 30,  # Connection timeout in seconds
    }
)


try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

# # Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Create base class for declarative models
Base = declarative_base()

Base.metadata.schema_translate_map = {
    None: "recipe_db"  # Default schema
}

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
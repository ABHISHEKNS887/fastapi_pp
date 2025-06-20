from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_ALCH_DB_URL = "sqlite:///./tweet.db"
# This is the database URL for SQLite. You can change it to connect to a different database.
# For example, you can use PostgreSQL or MySQL by changing the URL accordingly.
# For PostgreSQL: "postgresql://user:password@localhost/dbname"

engine = create_engine(SQL_ALCH_DB_URL, connect_args={"check_same_thread": False})
# Create the SQLAlchemy engine. The `connect_args` is used to allow SQLite to work with threads.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a session factory that will be used to create new sessions.
# The `autocommit` and `autoflush` options are set to False to control transaction behavior.

Base = declarative_base()

# This function is used to create a new database session for each request.
# It ensures that the session is closed after the request is completed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
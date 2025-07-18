import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# This is the database URL for SQLite. You can change it to connect to a different database.
# For example, you can use PostgreSQL or MySQL by changing the URL accordingly.
# For PostgreSQL: "postgresql://user:password@localhost/dbname"

from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv('db_username'),
    password=os.getenv('db_pass'),  # can contain @
    host="localhost",
    port=3306,
    database=os.getenv('db_name')
)

engine = create_engine(connection_url)
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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import OperationalError

DB_URL="postgresql://mr.junaid.ca:Of8jtYhgeH4C@ep-red-thunder-428017.us-east-2.aws.neon.tech/adj?sslmode=require"

if not DB_URL:
    raise Exception("DB_URL environment variable is not set")

# Enable connection pooling with pessimistic testing
engine = create_engine(DB_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency with retry mechanism for OperationalError
def get_db():
        db = SessionLocal()
        try:
            yield db
        except OperationalError as e:
            print(f"SSL connection error occurred: {e}, retrying...")
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
        finally:
            db.close()
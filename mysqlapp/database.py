from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username="Harlequin"
password="Quinlehar0179"
database="userapi"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://"+username+":"+password+"@localhost:3306/"+database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)


# Session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# Classe de base déclarative SQLAlchemy
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



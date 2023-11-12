from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''while True:
    try:
        conn = psycopg.connect(host='localhost',
                                dbname='fastapi',
                                user='postgres',
                                password='supergres1702*')
        cursor = conn.cursor(row_factory=dict_row)
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
        '''
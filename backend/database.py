from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
DATABASE_URL = "postgresql://postgres:teste123@localhost:5432/uaifestas_db?client_encoding=utf8"
=======
DATABASE_URL = "postgresql://postgres:teste1234@localhost:5432/uaifestas_db?client_encoding=utf8"
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
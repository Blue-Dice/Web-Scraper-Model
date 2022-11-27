from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.orm import sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from decouple import config

engine = create_engine(
    config('DATABASE_URI'),
    convert_unicode=True,
    echo=False
)

Model = declarative_base(name='Model')

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def initialize_database():
    Model.metadata.create_all(engine)

class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User: {self.email}>'
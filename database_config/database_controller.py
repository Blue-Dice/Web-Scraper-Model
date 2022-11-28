from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base
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
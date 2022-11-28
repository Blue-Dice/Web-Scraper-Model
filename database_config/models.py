from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from database_controller import Model

class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User: {self.email}>'
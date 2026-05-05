from sqlalchemy import Column, String, Integer, Boolean, DateTime

# - ORM model 的共同父類別。
from app.config.database import Base

class user_data(Base):
    __tablename__ = 'Tim5_test'

    call_id = Column(String(100), primary_key=True)
    ID = Column(String(10))
    acc = Column(String(20))
    phone = Column(String(10))
    birthday = Column(String(8))
    pwd_verified = Column(Boolean)
    is_loaded = Column(Boolean)
    write_time = Column(DateTime)

    def __repr__(self):
        return f"call_id={self.call_id}, ID={self.ID}, acc={self.acc}, phone={self.phone}, birthday={self.birthday}, pwd_verified={self.pwd_verified}"
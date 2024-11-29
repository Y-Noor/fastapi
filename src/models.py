from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Data(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, index=True)
    dataText = Column(String, index=True)
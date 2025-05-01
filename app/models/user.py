from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,unique=True,primary_key=True,index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)
    #skills = relationship("Skill", back_populates="user", cascade="all, delete")


    #creating a table where all users are going to be stored in
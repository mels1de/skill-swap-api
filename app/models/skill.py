from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class Skill(Base):
    __tablename__  = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="skills")
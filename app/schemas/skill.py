from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str

class SkillCreate(BaseModel):
    user_Id: int

class SkillOut(SkillBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
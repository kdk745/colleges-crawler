from pydantic import BaseModel
from typing import Optional

class CollegeBase(BaseModel):
    school_name: str
    school_city: Optional[str]
    school_state: Optional[str]
    college_board_code: Optional[str]

class CollegeCreate(CollegeBase):
    pass

class College(CollegeBase):
    id: int

    class Config:
        orm_mode = True

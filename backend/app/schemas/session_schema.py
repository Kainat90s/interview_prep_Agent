# from pydantic import BaseModel
# from typing import Optional
# import datetime


# class SessionCreate(BaseModel):
#     user_id: str


# class SessionOut(BaseModel):
#     id: int
#     user_id: str
#     started_at: datetime.datetime

#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from typing import Optional


class StartSessionResponse(BaseModel):
    session_id: str
    question_number: int
    question: str


class NextQuestionResponse(BaseModel):
    question_number: int
    question: str
    is_complete: bool

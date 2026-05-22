# from pydantic import BaseModel


# class AnswerCreate(BaseModel):
#     question: str
#     answer: str


# class AnswerOut(AnswerCreate):
#     id: int

#     class Config:
#         orm_mode = True
from pydantic import BaseModel
from typing import Optional

from app.schemas.session_schema import NextQuestionResponse


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_number: int
    user_answer: str


class FeedbackScore(BaseModel):
    clarity_score: int
    relevance_score: int
    star_score: int
    feedback: str


class SubmitAnswerResponse(BaseModel):
    evaluation: FeedbackScore
    next_question: Optional[NextQuestionResponse]
    overall_session_score: Optional[float]
# from sqlalchemy import Column, Integer, String, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from .session_model import Base


# class QA(Base):
#     __tablename__ = "qas"
#     id = Column(Integer, primary_key=True, index=True)
#     session_id = Column(Integer, ForeignKey("sessions.id"))
#     question = Column(Text)
#     answer = Column(Text)

#     session = relationship("Session")


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    ForeignKey
)

from app.core.database import Base


class QA(Base):
    __tablename__ = "qa_table"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        String,
        ForeignKey("sessions.session_id")
    )

    question_number = Column(Integer)

    question = Column(Text)

    user_answer = Column(Text)

    clarity_score = Column(Integer)

    relevance_score = Column(Integer)

    star_score = Column(Integer)

    overall_score = Column(Float)

    feedback = Column(Text)
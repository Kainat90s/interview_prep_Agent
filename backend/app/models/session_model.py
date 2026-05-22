# # from sqlalchemy import Column, Integer, String, DateTime
# # from sqlalchemy.ext.declarative import declarative_base
# # import datetime

# # Base = declarative_base()


# # class Session(Base):
# #     __tablename__ = "sessions"
# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(String, index=True)
# #     started_at = Column(DateTime, default=datetime.datetime.utcnow)

# from sqlalchemy import Column, String, Text, DateTime, Float, Boolean
# from sqlalchemy.sql import func
# import uuid

# from app.core.database import Base


# class Session(Base):
#     __tablename__ = "sessions"

#     session_id = Column(
#         String,
#         primary_key=True,
#         default=lambda: str(uuid.uuid4())
#     )

#     job_role = Column(String, nullable=False)

#     job_description = Column(Text)

#     resume_text = Column(Text)

#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     overall_score = Column(Float, default=0)

#     is_complete = Column(Boolean, default=False)

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    job_role = Column(String, nullable=False)

    job_description = Column(Text)

    resume_text = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    overall_score = Column(Float, default=0)

    is_complete = Column(Boolean, default=False)
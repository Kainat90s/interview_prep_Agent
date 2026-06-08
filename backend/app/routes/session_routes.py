from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import datetime

from app.core.database import get_db
from app.models.session_model import Session as SessionModel
from app.models.qa_model import QA as QAModel
from app.services import ai_service, resume_parser

router = APIRouter(tags=["sessions"])


@router.get("/sessions/")
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).order_by(SessionModel.created_at.desc()).all()
    # Format to match the frontend expectation of Home.jsx (which uses s.id and s.job_role)
    return {
        "sessions": [
            {
                "id": s.session_id,
                "session_id": s.session_id,
                "job_role": s.job_role,
                "job_description": s.job_description,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "overall_score": s.overall_score,
                "is_complete": s.is_complete
            }
            for s in sessions
        ]
    }


@router.post("/api/start-session")
async def start_session(
    job_role: str = Form(...),
    user_email: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    resume_text = ""
    if resume:
        file_bytes = await resume.read()
        resume_text = resume_parser.parse_resume(resume.filename, file_bytes)

    # 1. Generate 10 questions using Groq
    questions = ai_service.generate_questions(job_role, job_description, resume_text)

    # 2. Create session in DB
    db_session = SessionModel(
        job_role=job_role,
        user_email=user_email,
        job_description=job_description,
        resume_text=resume_text,
        is_complete=False,
        overall_score=0.0
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    # 3. Create QA records for the generated questions
    for i, question_text in enumerate(questions, start=1):
        db_qa = QAModel(
            session_id=db_session.session_id,
            question_number=i,
            question=question_text,
            user_answer=None,
            clarity_score=0,
            relevance_score=0,
            star_score=0,
            overall_score=0.0,
            feedback=""
        )
        db.add(db_qa)
    db.commit()

    # 4. Get first question
    first_q = db.query(QAModel).filter(
        QAModel.session_id == db_session.session_id,
        QAModel.question_number == 1
    ).first()

    return {
        "session_id": db_session.session_id,
        "first_question": {
            "question_number": 1,
            "question": first_q.question if first_q else "Tell me about yourself."
        }
    }

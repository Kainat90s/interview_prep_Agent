from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.models.session_model import Session as SessionModel
from app.models.qa_model import QA as QAModel
from app.services import pdf_service

router = APIRouter(tags=["reports"])


@router.get("/api/download-report/{session_id}")
def download_report(session_id: str, db: Session = Depends(get_db)):
    # 1. Fetch Session
    session_record = db.query(SessionModel).filter(
        SessionModel.session_id == session_id
    ).first()

    if not session_record:
        raise HTTPException(status_code=404, detail="Session not found")

    # 2. Fetch QAs
    qa_list = db.query(QAModel).filter(
        QAModel.session_id == session_id
    ).order_by(QAModel.question_number).all()

    # 3. Format session data
    session_data = {
        "session": {
            "session_id": session_record.session_id,
            "job_role": session_record.job_role,
            "created_at": session_record.created_at.strftime("%Y-%m-%d %H:%M:%S") if session_record.created_at else "",
            "overall_score": session_record.overall_score
        },
        "qa_list": [
            {
                "question_number": qa.question_number,
                "question": qa.question,
                "user_answer": qa.user_answer,
                "clarity_score": qa.clarity_score,
                "relevance_score": qa.relevance_score,
                "star_score": qa.star_score,
                "feedback": qa.feedback
            }
            for qa in qa_list
        ]
    }

    # 4. Generate PDF report
    pdf_path = pdf_service.generate_pdf_report(session_data)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"Interview_Report_{session_id}.pdf"
    )


@router.get("/reports/summary")
def report_summary():
    return {"summary": {}}

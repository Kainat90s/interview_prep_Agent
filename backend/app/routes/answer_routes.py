from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.session_model import Session as SessionModel
from app.models.qa_model import QA as QAModel
from app.schemas.answer_schema import SubmitAnswerRequest, SubmitAnswerResponse, FeedbackScore
from app.schemas.session_schema import NextQuestionResponse
from app.services import ai_service

router = APIRouter(tags=["answers"])


def process_submit_answer(req: SubmitAnswerRequest, db: Session) -> dict:
    # 1. Fetch QA record
    qa_record = db.query(QAModel).filter(
        QAModel.session_id == req.session_id,
        QAModel.question_number == req.question_number
    ).first()

    if not qa_record:
        raise HTTPException(status_code=404, detail="Question not found")

    # 2. Fetch job role from session
    session_record = db.query(SessionModel).filter(
        SessionModel.session_id == req.session_id
    ).first()

    if not session_record:
        raise HTTPException(status_code=404, detail="Session not found")

    job_role = session_record.job_role

    # 3. Evaluate answer with Groq
    scores = ai_service.evaluate_answer(job_role, qa_record.question, req.user_answer)

    # 4. Save evaluation and answer to DB
    qa_record.user_answer = req.user_answer
    qa_record.clarity_score = scores['clarity_score']
    qa_record.relevance_score = scores['relevance_score']
    qa_record.star_score = scores['star_score']
    
    overall_q_score = (scores['clarity_score'] + scores['relevance_score'] + scores['star_score']) / 3.0
    qa_record.overall_score = overall_q_score
    qa_record.feedback = scores['feedback']

    db.commit()

    # 5. Check if next question exists
    next_q_num = req.question_number + 1
    next_qa_record = db.query(QAModel).filter(
        QAModel.session_id == req.session_id,
        QAModel.question_number == next_q_num
    ).first()

    overall_session_score = None
    next_question_resp = None

    if next_qa_record:
        next_question_resp = {
            "question_number": next_q_num,
            "question": next_qa_record.question,
            "is_complete": False
        }
    else:
        # Session complete - calculate overall score
        all_qas = db.query(QAModel).filter(
            QAModel.session_id == req.session_id,
            QAModel.user_answer.isnot(None)
        ).all()

        if all_qas:
            total_score = sum(qa.overall_score for qa in all_qas)
            overall_session_score = total_score / len(all_qas)
        else:
            overall_session_score = 0.0

        # Update session
        session_record.overall_score = overall_session_score
        session_record.is_complete = True
        db.commit()

    return {
        "evaluation": scores,
        "next_question": next_question_resp,
        "overall_session_score": overall_session_score
    }


@router.post("/api/submit-answer", response_model=SubmitAnswerResponse)
def submit_answer_api(req: SubmitAnswerRequest, db: Session = Depends(get_db)):
    return process_submit_answer(req, db)


@router.post("/answers/", response_model=SubmitAnswerResponse)
def submit_answer_legacy(req: SubmitAnswerRequest, db: Session = Depends(get_db)):
    return process_submit_answer(req, db)

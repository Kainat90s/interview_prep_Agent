from fpdf import FPDF
import os


# -----------------------------
# CLEAN PDF TEXT
# -----------------------------
def clean_pdf_text(text):
    if not text:
        return ""
    text = str(text)
    # Remove unsupported unicode characters
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text


# -----------------------------
# GENERATE PDF REPORT
# -----------------------------
def generate_pdf_report(session_data: dict) -> str:
    session_info = session_data['session']
    qa_list = session_data['qa_list']

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # -----------------------------
    # TITLE
    # -----------------------------
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(
        190,
        10,
        "Interview Session Report",
        ln=True,
        align='C'
    )
    pdf.ln(5)

    # -----------------------------
    # SESSION DETAILS
    # -----------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(
        190,
        8,
        f"Job Role: {clean_pdf_text(session_info['job_role'])}",
        ln=True
    )

    pdf.set_font("Arial", '', 10)
    pdf.cell(
        190,
        6,
        f"Date: {clean_pdf_text(session_info['created_at'])}",
        ln=True
    )

    pdf.cell(
        190,
        6,
        f"Overall Score: {session_info['overall_score']:.1f} / 5.0",
        ln=True
    )
    pdf.ln(10)

    # -----------------------------
    # QUESTIONS & ANSWERS
    # -----------------------------
    for qa in qa_list:
        if not qa['user_answer']:
            continue

        question = clean_pdf_text(qa['question'])
        answer = clean_pdf_text(qa['user_answer'])
        feedback = clean_pdf_text(qa['feedback'])

        # Question
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(
            180,
            8,
            f"Q{qa['question_number']}: {question}"
        )
        pdf.ln(2)

        # Answer
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(
            180,
            6,
            f"Answer: {answer}"
        )
        pdf.ln(2)

        # Feedback Title
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(
            180,
            6,
            "Feedback & Scores:",
            ln=True
        )

        # Scores
        pdf.set_font("Arial", '', 10)
        pdf.cell(
            180,
            6,
            f"Clarity: {qa['clarity_score']}/5 | "
            f"Relevance: {qa['relevance_score']}/5 | "
            f"STAR: {qa['star_score']}/5",
            ln=True
        )

        # Feedback
        pdf.multi_cell(
            180,
            6,
            f"Tip: {feedback}"
        )
        pdf.ln(8)

    # -----------------------------
    # SAVE PDF
    # -----------------------------
    reports_dir = os.path.join(
        os.path.dirname(__file__),
        "reports"
    )
    os.makedirs(reports_dir, exist_ok=True)

    file_path = os.path.join(
        reports_dir,
        f"report_{session_info['session_id']}.pdf"
    )
    pdf.output(file_path)

    return file_path

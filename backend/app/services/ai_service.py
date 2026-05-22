import os
import json
from groq import Groq
from app.core.config import settings

# Initialize Groq client using settings
GROQ_API_KEY = settings.GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"


def clean_text(text):
    if not text:
        return ""
    try:
        # Remove broken unicode / emoji characters
        text = text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    except Exception:
        text = str(text)
    return text.strip()


def generate_questions(
    job_role: str,
    job_description: str = "",
    resume_text: str = ""
) -> list[str]:
    # Clean incoming text
    job_role = clean_text(job_role)
    job_description = clean_text(job_description)
    resume_text = clean_text(resume_text)

    prompt = f"""
    You are an expert technical interviewer.

    Generate EXACTLY 10 interview questions for a candidate applying for the role of '{job_role}'.

    Job Description:
    {job_description if job_description else "Not provided"}

    Candidate Resume:
    {resume_text if resume_text else "Not provided"}

    CRITICAL INSTRUCTIONS:

    1. FIRST 5 questions MUST be general HR/personal behavioral questions (e.g., "Tell me about yourself", "Strengths/weaknesses").
    
    2. LAST 5 questions MUST be deep Technical & Role-specific questions.
       - IF a resume is provided, you MUST specifically reference the candidate's actual projects, skills, or past experience from the text above. 
       - Do not ask generic technical questions. You MUST tailor them!
       - Start at least 3 of these technical questions with phrases like "I noticed in your resume that you used...", "Can you explain your work on [Project Name]...", or "How did you apply [Skill] at [Company]..."

    Return ONLY a valid JSON array of strings.

    Example Output:
    [
      "Tell me about yourself.",
      "What are your greatest strengths?",
      "Why do you want to work here?",
      "Describe a time you overcame a challenge.",
      "Where do you see yourself in 5 years?",
      "I noticed in your resume you built a FastAPI app. Can you explain its architecture?",
      "Your resume mentions PostgreSQL. How did you optimize slow queries in your last project?",
      "Can you explain how you implemented JWT authentication in your recent work?",
      "What design patterns do you frequently use in Python?",
      "How would you scale the microservices you built to handle 10x traffic?"
    ]
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful JSON-only outputting assistant."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=2048,
        )

        content = response.choices[0].message.content
        if not content:
            raise Exception("Empty response from Groq")

        content = content.strip()

        # Remove markdown wrappers if model misbehaves
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        questions = json.loads(content.strip())

        # Ensure exactly 10 questions
        if not isinstance(questions, list):
            raise Exception("Invalid JSON format")

        if len(questions) != 10:
            # Pad or trim to 10
            fallback_hr = [
                "Tell me about yourself.",
                "What are your greatest strengths?",
                "Describe a time you overcame a challenge.",
                "Why should we hire you?",
                "What motivates you?"
            ]
            fallback_tech = [
                f"What is your experience with {job_role}?",
                "How do you handle debugging and troubleshooting?",
                "What tools do you use daily?",
                "How do you keep up with new technologies?",
                "Can you describe a challenging project you worked on?"
            ]
            combined = questions + (fallback_hr + fallback_tech)
            return combined[:10]

        return questions

    except Exception as e:
        print("Error parsing Groq response:", e)
        # Fallback questions
        return [
            "Tell me about yourself.",
            "What are your greatest strengths?",
            "Describe a time you overcame a challenge.",
            "Why should we hire you?",
            "What motivates you?",
            f"What is your experience with {job_role}?",
            "How do you handle debugging and troubleshooting?",
            "What tools do you use daily?",
            "How do you keep up with new technologies?",
            "Can you describe a challenging project you worked on?"
        ]


def evaluate_answer(
    job_role: str,
    question: str,
    user_answer: str
) -> dict:
    # Clean text
    job_role = clean_text(job_role)
    question = clean_text(question)
    user_answer = clean_text(user_answer)

    prompt = f"""
    You are an expert technical interviewer evaluating a candidate for a '{job_role}' role.

    Question:
    {question}

    Candidate Answer:
    {user_answer}

    Evaluate the candidate's answer based on these criteria.
    Score each out of 5:

    1. clarity_score
       How clear and articulate is the answer?

    2. relevance_score
       Does it directly answer the question?

    3. star_score
       Does it demonstrate practical experience or use the STAR method?

    Also provide one concise feedback string with an actionable improvement tip.

    Respond ONLY with valid JSON.

    Example:
    {{
      "clarity_score": 4,
      "relevance_score": 5,
      "star_score": 3,
      "feedback": "Try structuring your answer using the STAR method."
    }}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict JSON-only outputting API."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
            temperature=0.3,
            max_tokens=512,
        )

        content = response.choices[0].message.content
        if not content:
            raise Exception("Empty response from Groq")

        content = content.strip()

        # Remove markdown wrappers
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        evaluation = json.loads(content.strip())

        return {
            "clarity_score": int(evaluation.get("clarity_score", 3)),
            "relevance_score": int(evaluation.get("relevance_score", 3)),
            "star_score": int(evaluation.get("star_score", 3)),
            "feedback": str(
                evaluation.get(
                    "feedback",
                    "Good effort. Try to be more specific next time."
                )
            )
        }

    except Exception as e:
        print("Error parsing Groq evaluation:", e)
        return {
            "clarity_score": 3,
            "relevance_score": 3,
            "star_score": 3,
            "feedback": "Could not evaluate properly due to a system error."
        }

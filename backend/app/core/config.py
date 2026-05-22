from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Interview Prep API"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/interview_db"
    )

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

settings = Settings()
print(settings.DATABASE_URL)

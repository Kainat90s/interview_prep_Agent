from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routes import session_routes, answer_routes, report_routes


app = FastAPI(title="AI Interview Prep API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://interviewfrontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(session_routes.router)
app.include_router(answer_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def home():
    return {"message": "AI Interview Prep Backend Running"}

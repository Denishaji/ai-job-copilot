# app/routers/jobs.py
from fastapi import APIRouter
from app.models import JobAnalysisRequest, JobAnalysisResponse
from app.services import analyze_job_with_llm


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(request: JobAnalysisRequest) -> JobAnalysisResponse:
    """Analyze a job description against a candidate profile."""

    result = analyze_job_with_llm(request)

    return JobAnalysisResponse(
        parsed_job=result["parsed_job"],
        analysis=result["analysis"],
    )

# app/models/job.py
from pydantic import BaseModel
from typing import List, Optional


class ParsedJob(BaseModel):
    """Structured fields extracted from the job description."""

    job_title: Optional[str] = None
    seniority: Optional[str] = None
    location: Optional[str] = None
    must_have_skills: List[str] = []
    nice_to_have_skills: List[str] = []
    sponsorship_hint: Optional[str] = None
    analysis: Optional[str] = None

    match_score: int = 0
    match_level: str = "unknown"

    ats_score: int = 0
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    extra_resume_keywords: List[str] = []

    # New: concrete suggestions to edit/improve resume for this JD
    resume_suggestions: List[str] = []


class JobAnalysisRequest(BaseModel):
    """Input body for job analysis."""

    job_description: str
    candidate_profile: str  # paste resume text or detailed profile here


class JobAnalysisResponse(BaseModel):
    """Output body for job analysis."""

    parsed_job: ParsedJob
    analysis: str

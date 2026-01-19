# app/services/job_service.py
from typing import Dict, Any
import json
import re

from app.models import JobAnalysisRequest, ParsedJob
from app.services.llm_service import get_llm


def analyze_job_basic(request: JobAnalysisRequest) -> Dict[str, Any]:
    """Very simple placeholder analysis logic.

    Kept for comparison once LLM logic is added.
    """
    parsed_job = {
        "job_title": "Unknown (LLM not wired yet)",
        "seniority": None,
        "location": None,
        "must_have_skills": [],
        "nice_to_have_skills": [],
        "sponsorship_hint": None,
        "analysis": "Placeholder analysis.",
    }

    analysis_text = (
        "This is a placeholder analysis. "
        "In the next steps, this will be replaced by LLM + RAG logic."
    )

    return {
        "parsed_job": parsed_job,
        "analysis": analysis_text,
    }


def _extract_json_block(text: str) -> str:
    """Extract the JSON part from a ```json ... ``` block or return original."""

    # Try to find ```json ... ``` or ``` ... ``` and extract inside.
    code_block_pattern = r"```json\s*(\{.*\})\s*```"
    match = re.search(code_block_pattern, text, flags=re.DOTALL)

    if match:
        return match.group(1).strip()

    # Fallback: try generic ``` ... ```
    generic_pattern = r"```(.*)```"
    match_generic = re.search(generic_pattern, text, flags=re.DOTALL)
    if match_generic:
        return match_generic.group(1).strip()

    # If no code block, assume the whole text is JSON
    return text.strip()


def analyze_job_with_llm(request: JobAnalysisRequest) -> Dict[str, Any]:
    """Use an OpenAI LLM to parse the job and give a short analysis."""

    llm = get_llm()

    system_prompt = (
    "You are an expert hiring assistant for many professional roles "
    "(software, data, product, marketing, finance, etc.). "
    "Given a job description and a candidate profile (resume text), "
    "you will extract a structured summary and give a brief fit analysis. "
    "Respond in JSON with these fields:\n"
    "- job_title\n"
    "- seniority\n"
    "- location\n"
    "- must_have_skills (list of strings)\n"
    "- nice_to_have_skills (list of strings)\n"
    "- sponsorship_hint\n"
    "- match_score (integer 0-100)\n"
    "- match_level ('low' | 'medium' | 'high')\n"
    "- ats_score (integer 0-100, based mainly on keyword overlap between job and resume)\n"
    "- matched_skills (subset of must_have_skills that appear in the resume text)\n"
    "- missing_skills (subset of must_have_skills that do NOT appear in the resume text)\n"
    "- extra_resume_keywords (other strong keywords from the resume relevant to this job)\n"
    "- resume_suggestions (list of 3-6 short bullet-style suggestions on how to edit the resume "
    "to better match this job, including specific skills/phrases to add or emphasize)\n"
    "- analysis (2-3 sentence explanation)\n"
    "Use must_have_skills coverage, seniority alignment, and obvious location/visa hints "
    "for match_score and match_level. Use keyword overlap between resume and job description "
    "for ats_score and for matched_vs_missing skills."
    )

    user_prompt = (
        f"Job description:\n{request.job_description}\n\n"
        f"Candidate profile:\n{request.candidate_profile}\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = llm.invoke(messages)
    raw_text = response.content

    json_text = _extract_json_block(raw_text)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        # If parsing fails, fall back gracefully
        parsed_job = ParsedJob(
            job_title=None,
            seniority=None,
            location=None,
            must_have_skills=[],
            nice_to_have_skills=[],
            sponsorship_hint=None,
            analysis=raw_text,
            match_score=0,
            match_level="unknown",
            ats_score=0,
            matched_skills=[],
            missing_skills=[],
            extra_resume_keywords=[],
            resume_suggestions=[],
        )
        return {
            "parsed_job": parsed_job.dict(),
            "analysis": raw_text,
        }

    parsed_job = ParsedJob(**data)

    return {
        "parsed_job": parsed_job.dict(),
        "analysis": parsed_job.analysis or raw_text,
    }

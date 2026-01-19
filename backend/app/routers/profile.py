# app/routers/profile.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import io
import pdfplumber

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    """
    Upload a PDF resume and return extracted text.

    For now, this endpoint just returns the text so you can paste it into
    /jobs/analyze as candidate_profile. Later you can store it per user.
    """
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")

    file_bytes = await file.read()

    try:
        pdf_file = io.BytesIO(file_bytes)
        with pdfplumber.open(pdf_file) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {e}")

    full_text = "\n".join(pages_text).strip()

    if not full_text:
        raise HTTPException(status_code=400, detail="Could not extract any text from the PDF.")

    return {"resume_text": full_text}

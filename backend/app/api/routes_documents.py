from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.ocr_service import check_document_readiness, SAMPLE_DOCUMENTS

router = APIRouter(prefix="/api/documents", tags=["Document Readiness Checker"])

class DocumentSampleItem(BaseModel):
    id: str
    title_en: str
    title_ta: str
    scheme_id: str

class DocumentReadinessResponse(BaseModel):
    readiness_score: int
    is_ready: bool
    language: str
    scheme_id: str
    extracted_text_preview: str
    identified_items: List[str]
    missing_items: List[str]
    voice_summary: str
    disclaimer: str

@router.get("/samples", response_model=List[DocumentSampleItem])
async def list_document_samples():
    """
    Returns the catalog of pre-loaded document test scenarios so citizens
    and evaluators can test the OCR verification without needing physical documents.
    """
    return [
        DocumentSampleItem(
            id=sample["id"],
            title_en=sample["title_en"],
            title_ta=sample["title_ta"],
            scheme_id=sample["scheme_id"]
        )
        for sample in SAMPLE_DOCUMENTS.values()
    ]

@router.post("/check", response_model=DocumentReadinessResponse)
async def check_document_readiness_endpoint(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    scheme_id: str = Form(default="old_age_pension"),
    language: str = Form(default="ta")
):
    """
    Scans uploaded citizen document image / PDF or runs instant analysis
    on pre-loaded test samples against scheme requirements.
    Uploaded bytes are processed strictly in-memory and discarded without disk storage.
    """
    try:
        file_bytes: Optional[bytes] = None

        if file and file.filename:
            file_bytes = await file.read()

        # If neither a file nor a sample_id is provided, default to sample_valid_oap
        if (not file_bytes or len(file_bytes) == 0) and not sample_id:
            sample_id = "sample_valid_oap"

        result = check_document_readiness(
            file_bytes=file_bytes,
            sample_id=sample_id,
            scheme_id=scheme_id,
            lang=language
        )
        return DocumentReadinessResponse(**result)

    except Exception as err:
        print(f"Error checking document readiness: {err}")
        raise HTTPException(status_code=500, detail="Failed to process document OCR analysis.")

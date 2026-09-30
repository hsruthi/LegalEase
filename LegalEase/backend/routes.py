from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from document_utils import generate_docx, generate_pdf

from backend.models import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            additional_instructions=request.additional_instructions,
        )

        return {
            "success": True,
            "document": document,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {error}",
        )


@router.post("/generate/docx")
def generate_docx_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            additional_instructions=request.additional_instructions,
        )

        file_path = generate_docx(
            title=request.document_type,
            content=document,
        )

        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {error}",
        )


@router.post("/generate/pdf")
def generate_pdf_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            additional_instructions=request.additional_instructions,
        )

        file_path = generate_pdf(
            title=request.document_type,
            content=document,
        )

        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type="application/pdf",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {error}",
        )
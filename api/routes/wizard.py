"""
Field Mapping Wizard API Routes

Provides REST endpoints for PDF field detection functionality.
This is the initial building block for the Field Mapping Wizard.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
from src.field_detector import PDFFieldDetector

router = APIRouter(prefix="/wizard", tags=["wizard"])
detector = PDFFieldDetector()


@router.post("/detect-fields")
async def detect_pdf_fields(pdf_file: UploadFile = File(...)):
    """
    Extract form fields and coordinates from an uploaded PDF.
    
    This endpoint analyzes PDF templates to identify all interactive form fields,
    their types, positions, and metadata. This information can be used to build
    visual field mapping interfaces or automated form processing systems.
    
    Args:
        pdf_file: Uploaded PDF template file
        
    Returns:
        JSON response containing all detected fields with their metadata
        
    Raises:
        HTTPException: If file is not PDF or processing fails
    """
    # Validate file type
    if not pdf_file.filename or not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="File must be a PDF document"
        )

    # Save uploaded file temporarily for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        try:
            content = await pdf_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save uploaded file: {str(e)}"
            )

    try:
        # Process PDF and extract field information
        result = detector.detect_fields(tmp_path)
        
        # Add original filename to response
        result["original_filename"] = pdf_file.filename
        
        return result
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing PDF: {str(e)}"
        )
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass  # File already deleted or doesn't exist
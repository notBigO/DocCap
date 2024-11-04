from venv import logger
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.document_validator import DocumentValidator
from services.ocr_service import perform_ocr


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        validator = DocumentValidator()

        extracted_text = perform_ocr(contents)
        document_details = validator.validate_document_details(extracted_text)

        return {
            "status": "success",
            "details": document_details,
        }
    except Exception as e:
        logger.error(f"Document processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

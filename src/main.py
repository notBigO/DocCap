from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from server.src.services.document_validator import validate_document_details
from server.src.services.ocr_service import perform_ocr

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

        extracted_text = perform_ocr(contents)
        document_details = validate_document_details(extracted_text)

        return {
            "status": "success",
            "details": document_details,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

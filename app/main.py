from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()


class PresignRequest(BaseModel):
    filename: str


class AnalyzeRequest(BaseModel):
    uploadId: str
    s3Key: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/presign")
async def presign(req: PresignRequest):
    upload_id = str(uuid.uuid4())
    return {
        "uploadId": upload_id,
        "s3Key": f"uploads/{upload_id}/{req.filename}",
        "presigned": {
            "url": "https://example.com/upload-placeholder",
            "fields": {}
        }
    }


@app.post("/api/v1/analyze")
async def analyze(req: AnalyzeRequest):
    if not req.uploadId:
        raise HTTPException(status_code=400, detail="uploadId required")
    # फिलहाल fake jobId = uploadId ही रख रहे हैं
    return {"jobId": req.uploadId}


@app.get("/api/v1/analyze/status/{upload_id}")
async def analyze_status(upload_id: str):
    # अभी के लिए हमेशा ready मानेंगे
    return {
        "status": "done",
        "highlights": [],
        "previewUrl": "https://placehold.co/600x400?text=Preview"
    }

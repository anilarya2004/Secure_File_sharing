from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from db.mongo import files_collection, users_collection
from auth.utils import decode_token
from config import ENCRYPTION_KEY
from cryptography.fernet import Fernet
from datetime import datetime
import os

router = APIRouter()
fernet = Fernet(ENCRYPTION_KEY.encode())

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_user_from_token(token: str):
    try:
        return decode_token(token)
    except:
        raise HTTPException(status_code=403, detail="Invalid token")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), token: str = Depends(get_user_from_token)):
    if token["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only Ops can upload files")
    ext = file.filename.split(".")[-1]
    if ext not in ["pptx", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    await files_collection.insert_one({
        "filename": file.filename,
        "path": path,
        "uploaded_by": token["email"],
        "uploaded_at": datetime.utcnow()
    })
    return {"message": "File uploaded"}

@router.get("/files")
async def list_files(token: str = Depends(get_user_from_token)):
    if token["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can list files")
    files = await files_collection.find().to_list(None)
    result = []
    for f in files:
        encrypted = fernet.encrypt(f["_id"].binary).decode()
        result.append({
            "filename": f["filename"],
            "download_url": f"http://localhost:8000/download/{encrypted}"
        })
    return result

@router.get("/download/{enc_id}")
async def download_file(enc_id: str, token: str = Depends(get_user_from_token)):
    if token["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can download files")
    try:
        file_id = ObjectId(fernet.decrypt(enc_id.encode()).decode())
    except:
        raise HTTPException(status_code=400, detail="Invalid download link")

    file = await files_collection.find_one({"_id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse({"download_path": file["path"]})

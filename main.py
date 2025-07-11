from fastapi import FastAPI , File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from transformers import pipeline
import os
import uuid
import ffmpeg

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

whisper = pipeline('automatic-speech-recognition',model= "openai/whisper-tiny",device = 0)

app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def homePage():
    return {"message": "Hi welcome to fastapi"}

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file received"}

    ext = file.filename.split('.')[-1]
    file_id = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        result = whisper(file_path, return_timestamps=True)
        return {"text": result["text"]}
    finally:
        os.remove(file_path)




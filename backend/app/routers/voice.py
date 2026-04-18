import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.whisper_service import whisper_service

router = APIRouter(prefix="/api/voice", tags=["voice"])


class TranscriptionResponse(BaseModel):
    text: str
    language: str | None = None


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text using Whisper.

    Accepts: audio/mpeg, audio/wav, audio/mp4, audio/x-m4a, etc.
    """
    # Validate file type
    allowed_types = [
        "audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a",
        "audio/ogg", "audio/webm", "audio/flac"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type: {file.content_type}"
        )

    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename or ".mp3")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        content = await file.read()
        f.write(content)
        temp_path = f.name

    try:
        # Transcribe
        text = await whisper_service.transcribe(temp_path)
        return TranscriptionResponse(text=text, language=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/transcribe-text", response_model=TranscriptionResponse)
async def transcribe_text(text: str):
    """
    Process text input (for voice-to-text from mobile or similar).
    """
    # For text input, just return as-is (already transcribed)
    return TranscriptionResponse(text=text, language=None)

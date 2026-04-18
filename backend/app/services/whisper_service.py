import os
import tempfile
from typing import Optional
from app.config import get_settings

settings = get_settings()


class WhisperService:
    """Service for audio transcription using Whisper."""

    def __init__(self):
        self.model_name = settings.WHISPER_MODEL
        self._model = None

    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to the audio file

        Returns:
            Transcribed text
        """
        # Check if OpenAI Whisper is available
        try:
            import whisper
            if self._model is None:
                self._model = whisper.load_model(self.model_name)
            result = self._model.transcribe(audio_path)
            return result["text"]
        except ImportError:
            # Fallback to mock transcription for development
            return await self._mock_transcribe(audio_path)

    async def _mock_transcribe(self, audio_path: str) -> str:
        """Mock transcription for development without Whisper installed."""
        # Return a sample transcription for testing
        return "Mock transcription: User mentioned expense of $50 for office supplies."

    async def transcribe_from_bytes(self, audio_bytes: bytes, filename: str) -> str:
        """Transcribe audio from bytes."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as f:
            f.write(audio_bytes)
            temp_path = f.name

        try:
            return await self.transcribe(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


whisper_service = WhisperService()

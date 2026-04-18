from app.routers.voice import router as voice_router
from app.routers.documents import router as documents_router
from app.routers.entries import router as entries_router
from app.routers.transactions import router as transactions_router

__all__ = ["voice_router", "documents_router", "entries_router", "transactions_router"]

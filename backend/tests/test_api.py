import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Voice-Driven SaaS MVP API"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_create_entry(client: AsyncClient):
    """Test creating a new entry."""
    entry_data = {
        "type": "text",
        "content": "Test entry content",
        "metadata": {"source": "test"}
    }
    response = await client.post("/api/entries/", json=entry_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "text"
    assert data["content"] == "Test entry content"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_entries(client: AsyncClient):
    """Test listing entries."""
    # Create an entry first
    entry_data = {
        "type": "voice",
        "content": "Voice entry"
    }
    await client.post("/api/entries/", json=entry_data)

    response = await client.get("/api/entries/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_entry_by_id(client: AsyncClient):
    """Test getting a single entry by ID."""
    # Create an entry
    entry_data = {
        "type": "document",
        "content": "Document entry"
    }
    create_response = await client.post("/api/entries/", json=entry_data)
    entry_id = create_response.json()["id"]

    # Get by ID
    response = await client.get(f"/api/entries/{entry_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == entry_id
    assert data["content"] == "Document entry"


@pytest.mark.asyncio
async def test_update_entry(client: AsyncClient):
    """Test updating an entry."""
    # Create an entry
    entry_data = {
        "type": "text",
        "content": "Original content"
    }
    create_response = await client.post("/api/entries/", json=entry_data)
    entry_id = create_response.json()["id"]

    # Update it
    update_data = {"content": "Updated content"}
    response = await client.put(f"/api/entries/{entry_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated content"


@pytest.mark.asyncio
async def test_delete_entry(client: AsyncClient):
    """Test deleting an entry."""
    # Create an entry
    entry_data = {
        "type": "text",
        "content": "To be deleted"
    }
    create_response = await client.post("/api/entries/", json=entry_data)
    entry_id = create_response.json()["id"]

    # Delete it
    response = await client.delete(f"/api/entries/{entry_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = await client.get(f"/api/entries/{entry_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient):
    """Test creating a transaction."""
    # First create an entry
    entry_data = {"type": "text", "content": "Transaction source"}
    entry_response = await client.post("/api/entries/", json=entry_data)
    entry_id = entry_response.json()["id"]

    # Create transaction
    transaction_data = {
        "entry_id": entry_id,
        "amount": 100.50,
        "category": "expense",
        "description": "Test transaction",
        "date": "2024-01-15"
    }
    response = await client.post("/api/transactions/", json=transaction_data)
    assert response.status_code == 200
    data = response.json()
    assert float(data["amount"]) == 100.50
    assert data["category"] == "expense"


@pytest.mark.asyncio
async def test_list_transactions(client: AsyncClient):
    """Test listing transactions."""
    response = await client.get("/api/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_transaction_summary(client: AsyncClient):
    """Test transaction summary endpoint."""
    response = await client.get("/api/transactions/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_amount" in data
    assert "transaction_count" in data
    assert "by_category" in data
    assert "by_month" in data


@pytest.mark.asyncio
async def test_list_documents(client: AsyncClient):
    """Test listing documents."""
    response = await client.get("/api/documents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_voice_transcribe_text(client: AsyncClient):
    """Test text transcription endpoint."""
    response = await client.post("/api/voice/transcribe-text?text=Hello%20world")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
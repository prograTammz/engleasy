from unittest.mock import patch, MagicMock
from app.utils.mongo_client import users_collection, scores_collection

@patch("app.utils.mongo_client.AsyncIOMotorClient")
def test_mongo_client_initialization(mock_motor_client):
    mock_db = MagicMock()
    mock_motor_client.return_value = mock_db

    # Verify that the client and collections are set correctly
    assert users_collection.name == "users"
    assert scores_collection.name == "scores"

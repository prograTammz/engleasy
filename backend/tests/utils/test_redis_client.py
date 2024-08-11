import pytest
from unittest.mock import patch, MagicMock
from app.utils.redis_client import redis_client

@patch('app.utils.redis_client.redis.Redis')
def test_redis_client_initialization(mock_redis):
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance

    # Verify that the Redis client pings successfully
    assert redis_client.ping() is True

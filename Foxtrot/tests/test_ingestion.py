from unittest.mock import Mock, patch

from src.ingestion import fetch_data


@patch("nova.src.ingestion.requests.get")
def test_fetch_data_returns_carts(mock_get):

    mock_response = Mock()

    mock_response.json.return_value = {
        "carts": [
            {"id": 1},
            {"id": 2}
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetch_data("https://dummyjson.com/carts")

    assert len(result) == 2
    assert result[0]["id"] == 1
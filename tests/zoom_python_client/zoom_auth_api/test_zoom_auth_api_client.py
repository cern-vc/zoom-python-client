from time import time

import pytest

from zoom_python_client.zoom_auth_api.zoom_auth_api_client import (
    ZoomAuthApiClient,
    ZoomAuthApiClientError,
)


def test_zoom_auth_api_client():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    assert client.account_id == "aaa"
    assert client.client_id == "bbb"
    assert client.client_secret == "ccc"


def test_base64encode():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    result = client.base64_encode_auth()

    assert result == "YmJiOmNjYw=="


def test_access_token_expired_true(monkeypatch):
    monkeypatch.setenv("ZOOM_ACCESS_TOKEN_EXPIRE", str(int(time())))
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    result = client.is_zoom_access_token_expired()
    assert result


def test_access_token_expired_false(monkeypatch):
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")

    monkeypatch.setenv(
        "ZOOM_ACCESS_TOKEN_EXPIRE",
        str(int(time() + client.minimum_expire_time_seconds + 100)),
    )
    result = client.is_zoom_access_token_expired()
    assert not result


def test_extract_access_token():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    with pytest.raises(ZoomAuthApiClientError):
        client.extract_access_token({"access_token": "test"})
    with pytest.raises(ZoomAuthApiClientError, match="Unable to get access_token"):
        client.extract_access_token({"expires_in": "test"})
    with pytest.raises(ZoomAuthApiClientError, match="Unable to get access_token"):
        client.extract_access_token({"expires_in": 100})
    with pytest.raises(
        ZoomAuthApiClientError,
        match="Unable to set access_token expiration. expires_in is not an int",
    ):
        client.extract_access_token({"access_token": "test", "expires_in": "test"})
    result = client.extract_access_token({"access_token": "test", "expires_in": 100})
    assert result == "test"

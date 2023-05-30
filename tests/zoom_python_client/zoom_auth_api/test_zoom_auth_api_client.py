import os
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
    expire_time = str(int(time()))
    monkeypatch.setenv("ZOOM_ACCESS_TOKEN_EXPIRE", expire_time)
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    result = client.is_zoom_access_token_expired(expire_time)
    assert result


def test_access_token_expired_false(monkeypatch):
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    expire_time = str(int(time() + client.minimum_expire_time_seconds + 100))
    monkeypatch.setenv(
        "ZOOM_ACCESS_TOKEN_EXPIRE",
        expire_time,
    )
    result = client.is_zoom_access_token_expired(expire_time)
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


def test_use_path_none():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    with pytest.raises(ZoomAuthApiClientError):
        client.save_token_and_seconds_to_file({"access_token": "test"})


def test_save_token_to_file():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc", use_path=".")
    result = client.save_token_and_seconds_to_file(
        {"access_token": "test", "expires_in": "12345"}
    )
    assert result
    # with pytest.raises(ZoomAuthApiClientError, match="Unable to get access_token"):
    #     client.extract_access_token({"expires_in": "test"})
    # with pytest.raises(ZoomAuthApiClientError, match="Unable to get access_token"):
    #     client.extract_access_token({"expires_in": 100})
    # with pytest.raises(
    #     ZoomAuthApiClientError,
    #     match="Unable to set access_token expiration. expires_in is not an int",
    # ):
    #     client.extract_access_token({"access_token": "test", "expires_in": "test"})
    # result = client.extract_access_token({"access_token": "test", "expires_in": 100})
    # assert result == "test"


def test_extract_access_token_file():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc", use_path=".")
    result = client.extract_access_token(
        {"access_token": "test", "expires_in": "12345"}
    )
    assert result


def test_get_access_token_from_file_none():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    with pytest.raises(ZoomAuthApiClientError):
        client.get_access_token_from_file()


def test_get_file_not_found():
    # Delete the access token and expire_seconds files
    os.remove("access_token")
    os.remove("expire_seconds")
    client = ZoomAuthApiClient("aaa", "bbb", "ccc", use_path=".")
    result = client.get_access_token_from_file()
    assert result is None


def test_get_expire_seconds_from_file_none():
    client = ZoomAuthApiClient("aaa", "bbb", "ccc")
    with pytest.raises(ZoomAuthApiClientError):
        client.get_expire_seconds_from_file()

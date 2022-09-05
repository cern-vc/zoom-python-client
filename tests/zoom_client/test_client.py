from zoom_client.client import ZoomClient


def test_client():
    client = ZoomClient("aaa", "bbb", "ccc")
    assert client.account_id == "aaa"
    assert client.client_id == "bbb"
    assert client.client_secret == "ccc"


def test_init_from_env(monkeypatch):
    monkeypatch.setenv("ZOOM_ACCOUNT_ID", "aaa")
    monkeypatch.setenv("ZOOM_CLIENT_ID", "bbb")
    monkeypatch.setenv("ZOOM_SECRET_ID", "ccc")

    client = ZoomClient.init_from_env()
    assert client.account_id == "aaa"
    assert client.client_id == "bbb"
    assert client.client_secret == "ccc"

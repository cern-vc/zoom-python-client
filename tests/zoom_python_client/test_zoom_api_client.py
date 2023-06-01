import pytest
import requests
import responses

from tests.zoom_python_client.base_test_case import TestCaseWithAuth
from zoom_python_client.zoom_api_client import ZoomApiClient, ZoomClientEnvError


def test_init_from_env(monkeypatch):
    monkeypatch.setenv("ZOOM_ACCOUNT_ID", "aaa")
    monkeypatch.setenv("ZOOM_CLIENT_ID", "bbb")
    monkeypatch.setenv("ZOOM_CLIENT_SECRET", "ccc")

    client = ZoomApiClient.init_from_env()

    assert client is not None


@pytest.fixture(params=["ZOOM_ACCOUNT_ID", "ZOOM_CLIENT_ID", "ZOOM_CLIENT_SECRET"])
def env_variable(request):
    return request.param


def test_init_from_env_exception(env_variable, monkeypatch):
    monkeypatch.setenv(env_variable, "aaa")
    with pytest.raises(ZoomClientEnvError):
        ZoomApiClient.init_from_env()


def test_init_from_dotenv():
    client = ZoomApiClient.init_from_dotenv(custom_dotenv=".env.sample")
    assert client is not None


def test_init_with_use_path():
    client = ZoomApiClient.init_from_dotenv(custom_dotenv=".env.sample", use_path=".")
    assert client is not None


class TestZoomApiClient(TestCaseWithAuth):
    @responses.activate
    def test_get_request(self):
        responses.add(
            responses.GET,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient("AAA", "BBB", "CCC", api_endpoint="http://localhost")
        response = client.make_get_request("/test", {})
        assert response.status_code == 200

    @responses.activate
    def test_patch_request(self):
        responses.add(
            responses.PATCH,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient("AAA", "BBB", "CCC", api_endpoint="http://localhost")
        response = client.make_patch_request("/test", {})
        assert response.status_code == 200

    @responses.activate
    def test_post_request(self):
        responses.add(
            responses.POST,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient("AAA", "BBB", "CCC", api_endpoint="http://localhost")
        response = client.make_post_request("/test", {})
        assert response.status_code == 200


class TestZoomApiClientFromPath(TestCaseWithAuth):
    @responses.activate
    def test_get_request(self):
        responses.add(
            responses.GET,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.make_get_request("/test", {})
        assert response.status_code == 200

    @responses.activate
    def test_patch_request(self):
        responses.add(
            responses.PATCH,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.make_patch_request("/test", {})
        assert response.status_code == 200

    @responses.activate
    def test_post_request(self):
        responses.add(
            responses.POST,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.make_post_request("/test", {})
        assert response.status_code == 200


class TestZoomApiClientRetry(TestCaseWithAuth):
    @responses.activate
    def test_get_request(self):
        responses.add(
            responses.GET,
            "http://localhost/test",
            json={"response": "ok"},
            status=401,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        with pytest.raises(requests.exceptions.HTTPError):
            response = client.make_get_request("/test", {})
            assert response.status_code == 401

    @responses.activate
    def test_patch_request(self):
        responses.add(
            responses.PATCH,
            "http://localhost/test",
            json={"response": "ok"},
            status=401,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        with pytest.raises(requests.exceptions.HTTPError):
            response = client.make_patch_request("/test", {})
            assert response.status_code == 401

    @responses.activate
    def test_post_request(self):
        responses.add(
            responses.POST,
            "http://localhost/test",
            json={"response": "ok"},
            status=401,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        with pytest.raises(requests.exceptions.HTTPError):
            response = client.make_post_request("/test", {})
            assert response.status_code == 401


class TestZoomApiClientRetryMethods(TestCaseWithAuth):
    @responses.activate
    def test_retry_get_request(self):
        responses.add(
            responses.GET,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.retry_get_request("/test", "")
        assert response.status_code == 200

    @responses.activate
    def test_retry_patch_request(self):
        responses.add(
            responses.PATCH,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.retry_patch_request("/test", {})
        assert response.status_code == 200

    @responses.activate
    def test_retry_post_request(self):
        responses.add(
            responses.POST,
            "http://localhost/test",
            json={"response": "ok"},
            status=200,
        )
        client = ZoomApiClient(
            "AAA", "BBB", "CCC", api_endpoint="http://localhost", use_path="."
        )
        response = client.retry_post_request("/test", {})
        assert response.status_code == 200

import responses
from zoom_python_client.api_client import ApiClient


def test_api_client_build_headers():
    api_client = ApiClient("http://localhost")
    headers = api_client.build_headers()
    assert headers == {"Content-type": "application/json"}


def test_api_client_build_headers_extra():
    api_client = ApiClient("http://localhost")
    headers = api_client.build_headers({"Authentication": "Bearer 12345"})
    assert headers == {
        "Content-type": "application/json",
        "Authentication": "Bearer 12345",
    }


def test_api_client_build_headers_extra_no_duplicates():
    api_client = ApiClient("http://localhost")
    # pylint: disable=duplicate-key
    headers = api_client.build_headers(
        {
            "Authentication": "Bearer 12345",
            "Authentication": "Bearer 12345",
            "Content-type": "application/json",
        }
    )
    assert headers == {
        "Content-type": "application/json",
        "Authentication": "Bearer 12345",
    }


@responses.activate
def test_api_client_make_get_request():
    responses.add(
        responses.GET,
        "http://localhost/test",
        json={"response": "ok"},
        status=200,
    )
    api_client = ApiClient("http://localhost")
    headers = api_client.build_headers()
    response = api_client.make_get_request("/test", headers=headers)

    assert response.status_code == 200


@responses.activate
def test_api_client_make_post_request():
    responses.add(
        responses.POST,
        "http://localhost/test",
        json={"response": "ok"},
        status=200,
    )
    api_client = ApiClient("http://localhost")
    headers = api_client.build_headers()
    response = api_client.make_post_request("/test", headers=headers)

    assert response.status_code == 200

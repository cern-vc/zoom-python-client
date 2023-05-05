# Zoom Python client

[![Python tests](https://github.com/cern-vc/zoom-python-client/actions/workflows/python-tests.yml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/python-tests.yml) [![pre-commit](https://github.com/cern-vc/zoom-python-client/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/pre-commit.yaml) [![CodeQL](https://github.com/cern-vc/zoom-python-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/codeql-analysis.yml) [![codecov](https://codecov.io/gh/cern-vc/zoom-python-client/branch/main/graph/badge.svg?token=04EY0K0P2S)](https://codecov.io/gh/cern-vc/zoom-python-client)

> ⚠️ WIP: This project is a WIP and therefore may contain bugs. Use it at your own risk and keep this in mind if you decide to use it in production environments.


## Usage

### Defining your env variables

Define the following variables in your `env` or your `.env` file:

- ZOOM_ACCOUNT_ID
- ZOOM_CLIENT_ID
- ZOOM_CLIENT_SECRET

### Initialize the ZoomApiClient from environment variables

```python
from src.zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient.init_from_env()
```

### Initialize the ZoomApiClient from .env

```python
from src.zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient.init_from_dotenv()
```
### Initialize the ZoomApiClient manually

```python
from src.zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient(
        account_id="<YOUR ACCOUNT ID>",
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>")
```


## How to make API calls

```python
MEETING_ID = "12345"
USER_ID = "abcdfgh"

result = zoom_client.users.get_user(USER_ID)
print(result)

result = zoom_client.meetings.get_meeting(MEETING_ID)
print(result)
```
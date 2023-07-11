# Zoom Python client

[![Python tests](https://github.com/cern-vc/zoom-python-client/actions/workflows/python-tests.yml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/python-tests.yml) [![pre-commit](https://github.com/cern-vc/zoom-python-client/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/pre-commit.yaml) [![CodeQL](https://github.com/cern-vc/zoom-python-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cern-vc/zoom-python-client/actions/workflows/codeql-analysis.yml) [![codecov](https://codecov.io/gh/cern-vc/zoom-python-client/branch/main/graph/badge.svg?token=04EY0K0P2S)](https://codecov.io/gh/cern-vc/zoom-python-client)

Zoom API Python client with support for [Server to Server Oauth tokens](https://developers.zoom.us/docs/internal-apps/s2s-oauth/)

## Install

This package is [available on Pypi](https://pypi.org/project/zoom-python-client/)

```bash
pip install zoom-python-client
```

## Requirements

- Python >= 3.9

## Usage

### Defining your env variables

Define the following variables in your `env` or your `.env` file:

- ZOOM_ACCOUNT_ID
- ZOOM_CLIENT_ID
- ZOOM_CLIENT_SECRET

### Initialize the ZoomApiClient from environment variables

```python
from zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient.init_from_env()
```

### Initialize the ZoomApiClient from .env

```python
from zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient.init_from_dotenv()
```

### Initialize the ZoomApiClient manually

```python
from zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient(
        account_id="<YOUR ACCOUNT ID>",
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>")
```

### Use the file system to store the access token instead of environment

There are some cases where you might want to store the access token in the file system in order to share its value with other elements of the application (Ex. different pods on a Kubernetes/Openshift application).

You can define the path where the token will be stored, passing the `use_path` variable to the constructor:

```python
from zoom_python_client.zoom_api_client import ZoomApiClient

zoom_client = ZoomApiClient(
        account_id="<YOUR ACCOUNT ID>",
        client_id="<YOUR CLIENT ID>",
        client_secret="<YOUR CLIENT SECRET>",
        use_path="/path/to/token/folder")
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

## Optional: How to configure the logging

```python
from zoom_python_client.utils.logger import setup_logs

setup_logs(log_level=logging.DEBUG)
```

## Available endpoints

### **users**:

1. get user details
2. get user meetings

### **meetings**:

1. get meeting details
2. get meeting token

### **meeting live streams**:

1. get meeting live stream
2. update live stream
3. update livestream status

### **webinars**:

1. get webinar details

### **webinar live streams**:

1. get webinar live stream
2. update webinar live stream
3. update webinar livestream status

### **zoom rooms**:

1. get all zoom rooms
2. get zoom room details
3. get zoom room sensor data

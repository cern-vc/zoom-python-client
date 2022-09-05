import os


class ZoomClientError(Exception):
    pass


class ZoomClient:
    def __init__(self, account_id: str, client_id: str, client_secret: str):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret

    @staticmethod
    def init_from_env():
        account_id = os.getenv("ZOOM_ACCOUNT_ID", default=None)
        client_id = os.getenv("ZOOM_CLIENT_ID", default=None)
        client_secret = os.getenv("ZOOM_SECRET_ID", default=None)
        if account_id and client_id and client_secret:
            zoom_client = ZoomClient(account_id, client_id, client_secret)
            return zoom_client
        raise ZoomClientError(
            "ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID or ZOOM_SECRET_ID are not properly set in the environment variables"
        )

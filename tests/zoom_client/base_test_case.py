import unittest
import responses


class TestCaseWithAuth(unittest.TestCase):
    def setUp(self):
        # responses.get("https://example.com", body="within setup")
        # here go other self.responses.add(...)
        responses.add(
            responses.POST,
            "https://zoom.us/oauth/token",
            json={"access_token": "ok", "expires_in": 3600},
            status=200,
        )

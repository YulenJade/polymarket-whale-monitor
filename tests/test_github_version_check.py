"""Unit tests use mocks and do not access GitHub or trading services."""
import io
import json
import unittest
from unittest.mock import patch
from github_version_check import fetch_latest_commit


class GitHubVersionCheckTests(unittest.TestCase):
    def test_latest_commit(self):
        payload = json.dumps([{"sha": "abc123456", "html_url": "https://github.com/example/repo/commit/abc123456"}]).encode()
        response = io.BytesIO(payload)
        with patch("urllib.request.urlopen", return_value=response) as mocked:
            result = fetch_latest_commit("example/repo")
        self.assertEqual(result["sha"], "abc123456")
        self.assertIn("api.github.com/repos/example/repo/commits", mocked.call_args.args[0].full_url)
        self.assertNotIn("Authorization", mocked.call_args.args[0].headers)

    def test_invalid_repo(self):
        with self.assertRaises(ValueError):
            fetch_latest_commit("badrepo")

    def test_branch_is_encoded(self):
        payload = json.dumps([{"sha": "abc123"}]).encode()
        with patch("urllib.request.urlopen", return_value=io.BytesIO(payload)) as mocked:
            fetch_latest_commit("example/repo", branch="feature/test")
        self.assertIn("sha=feature%2Ftest", mocked.call_args.args[0].full_url)


if __name__ == "__main__":
    unittest.main()

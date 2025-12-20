#!/usr/bin/env python3
"""Client tests for client.py"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """It should return the organization payload."""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """It should return the repos_url from the organization payload."""
        payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=payload,
        ):
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """It should return a list of repo names and call dependencies once."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="http://fake-url.com",
        ) as mock_repos_url:
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(), ["repo1", "repo2", "repo3"])

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """It should return True if the repo has the given license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected,
        )

@parameterized_class(TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and return fixture payloads."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        org_url = "https://api.github.com/orgs/google"
        repos_url = cls.org_payload["repos_url"]

        def side_effect(url, *args, **kwargs):
            """Return correct mock response depending on URL."""
            mock_response = Mock()
            if url == org_url:
                mock_response.json.return_value = cls.org_payload
            elif url == repos_url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher for requests.get."""
        cls.get_patcher.stop()

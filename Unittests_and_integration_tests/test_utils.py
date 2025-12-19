#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from utils import memoize
from client import GithubOrgClient


class TestAccessNestedMap(unittest.TestCase):
    """Tests for Access Nested Map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """It should return the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """It should raise a KeyError when the given path does not exist."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(expected_msg))


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """It should return the expected JSON payload."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        """It should cache the result so a_method is called only once."""
        class TestClass:
            """A helper class used to test memoization."""
            def a_method(self):
                """Return a fixed number."""
                return 42

            @memoize
            def a_property(self):
                """Return the memoized value produced by a_method."""
                return self.a_method()

        obj = TestClass()

        with patch.object(obj, "a_method", return_value=42) as mock_method:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()

from anyapi import AnyAPI

import pytest


def test_params():
    """Test passing params to Session"""
    httpbin = AnyAPI("http://httpbin.org", auth=("user", "password"))

    assert httpbin("basic-auth").user.password.GET().json()["authenticated"]


def test_passing_url():
    """Test passing URL directly"""
    httpbin = AnyAPI("http://httpbin.org")

    assert (
        httpbin.GET(url="http://httpbin.org/anything").json()["url"]
        == "https://httpbin.org/anything"
    )

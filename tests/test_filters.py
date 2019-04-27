from anyapi import AnyAPI

import pytest


@pytest.fixture
def httpbin():
    return AnyAPI("http://httpbin.org")


def add_header(kwargs):
    kwargs["headers"]["Test-Header"] = "Test-Value"


def test_filter_request(httpbin):
    """Test filter_request by setting header (It is enough to test against only headers)"""

    httpbin._filter_request.append(add_header)
    assert httpbin.anything.GET().json()["headers"]["Test-Header"] == "Test-Value"


def test_filter_response(httpbin):
    """Test filter_response by responses to json automatically"""

    httpbin._filter_response.append(lambda _, response: response.json())
    assert isinstance(httpbin.anything.GET(), dict)


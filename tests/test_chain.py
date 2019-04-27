from anyapi import AnyAPI
from anyapi.chain import Chain, _HTTP_METHODS

import pytest


@pytest.fixture
def httpbin():
    return AnyAPI("http://httpbin.org")


def test_chain(httpbin):
    """Test if chain works"""

    assert isinstance(httpbin.anything, Chain)


def test_deep_chain(httpbin):
    """Test if chain works"""

    assert isinstance(httpbin.anything.also_anything, Chain)


def test_chain_methods(httpbin):
    """Test if chain returns methods when called"""

    # To test __getattr__
    for method in _HTTP_METHODS:
        assert callable(getattr(httpbin.anything, method))

    # To test __new__
    for method in _HTTP_METHODS:
        assert callable(getattr(httpbin, method))


def test_path_and_ref(httpbin):
    """Test if paths are correct"""

    assert httpbin.anything._Chain__path == "/anything"
    assert httpbin.anything.also_anything._Chain__path == "/anything/also_anything"
    assert httpbin.anything("also_anything")._Chain__path == "/anything/also_anything"
    assert httpbin("anything")._Chain__path == "/anything"

    assert httpbin.anything._Chain__parent_api is httpbin

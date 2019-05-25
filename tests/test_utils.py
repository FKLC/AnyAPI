from anyapi import AnyAPI
from anyapi.utils import retry

from requests.exceptions import MissingSchema
import pytest


def test_retry():
    """Test retry utility"""
    # I know that I should test retry and retry_until separately
    # But I couldn't find any idea to test retry_until separately
    try:
        invalid_api = AnyAPI("invalidurl", scoped_calls=[retry(2)])
        invalid_api.GET()
    except MissingSchema:
        assert True
    else:
        assert False

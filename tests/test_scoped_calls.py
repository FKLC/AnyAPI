from anyapi import AnyAPI
from requests import ConnectTimeout


def parent_call(request, out):
    try:
        request()
    except Exception as e:
        out.append(e)


def test_scoped_call():
    exception = []

    httpbin = AnyAPI(
        "http://httpbin.org",
        scoped_calls=[lambda request: parent_call(request, exception)],
    )
    httpbin.GET(timeout=1e-10)

    assert isinstance(exception[0], ConnectTimeout)


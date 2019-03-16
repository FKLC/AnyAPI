from urllib.parse import urlparse

import requests

from .chain import Chain
from .proxy_handlers import NoProxy


class AnyAPI:
    def __init__(
        self,
        base_url,
        default_params={},
        default_headers={},
        default_auth=(),
        proxy_configuration={},
        proxy_handler=NoProxy,
        scoped_call=None,
    ):
        self._base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self._filter_request = []
        self._filter_response = []

        self.__session = requests.Session()
        self.__session.params = default_params
        self.__session.headers = default_headers
        self.__session.auth = default_auth

        self.__proxy_handler = proxy_handler(**proxy_configuration)
        self.__scoped_call = scoped_call

    def __getattr__(self, path):
        return Chain(self, path)

    def __call__(self, *paths):
        return Chain(self, "/".join(paths))

    def _make_request(self, method, path, *args, **kwargs):
        if not kwargs.get("auth"):
            kwargs["auth"] = ""
            del kwargs["auth"]

        if kwargs.get("url"):
            url = kwargs.get("url")
            path = urlparse(url).path
            del kwargs["url"]
        else:
            url = self._base_url + path

        for field in ["params", "headers", "data", "json"]:
            kwargs.setdefault(field, {})

        for function in self._filter_request:
            function({**kwargs, "path": path, "url": url})

        self.__session.proxies = self.__proxy_handler.get(kwargs)

        if self.__scoped_call is not None:
            response = self.__scoped_call(
                lambda: getattr(self.__session, method.lower())(
                    url=url, *args, **kwargs
                )
            )
        else:
            response = getattr(self.__session, method.lower())(url=url, *args, **kwargs)

        for function in self._filter_response:
            response = function({**kwargs, "path": path, "url": url}, response=response)

        return response

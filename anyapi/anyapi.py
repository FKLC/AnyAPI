import re
from collections import defaultdict
from functools import reduce
from urllib.parse import urlparse

import requests
from attribute_router import Router

from .proxy_handlers import NoProxy


class AnyAPI(Router):
    def __init__(
        self,
        base_url,
        proxy_configuration={},
        proxy_handler=NoProxy,
        scoped_calls=[],
        **kwargs
    ):
        self._base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self._filter_request = []
        self._filter_response = []

        self.__session = requests.Session()
        for attribute, value in kwargs.items():
            setattr(self.__session, attribute, value)

        self.__proxy_handler = proxy_handler(**proxy_configuration)
        self.__scoped_calls = scoped_calls

        super(AnyAPI, self).__init__(
            routes={
                re.compile(
                    "(.*)/(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH)$"
                ): self._make_request
            }
        )

    def _make_request(self, _match, *args, **kwargs):
        path = _match.group(1)
        method = _match.group(2)

        if kwargs.get("url"):
            url = kwargs.get("url")
            path = urlparse(url).path
            del kwargs["url"]
        else:
            url = self._base_url + path

        kwargs = defaultdict(dict, **kwargs, path=path, url=url)

        for function in self._filter_request:
            function(kwargs)

        self.__session.proxies = self.__proxy_handler.get(kwargs)

        del kwargs["path"]

        response = reduce(
            lambda old_function, new_function: lambda: new_function(old_function),
            [
                lambda: getattr(self.__session, method.lower())(*args, **kwargs),
                *self.__scoped_calls,
            ],
        )()

        for function in self._filter_response:
            response = function({**kwargs, "path": path}, response=response)

        return response

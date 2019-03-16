_HTTP_METHODS = ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH"]


class Chain:
    def __new__(cls, parent_api, path):
        if path in _HTTP_METHODS:
            return lambda *args, **kwargs: parent_api._make_request(
                method=path, path="", *args, **kwargs
            )
        self = object.__new__(cls)
        self.__parent_api = parent_api
        self.__path = f"/{path}"

        return self

    def __getattr__(self, path):
        if path in _HTTP_METHODS:
            return lambda *args, **kwargs: self.__parent_api._make_request(
                method=path, path=self.__path, *args, **kwargs
            )
        self.__path += f"/{path}"

        return self

    def __call__(self, *paths):
        self.__path += "/" + "/".join(paths)

        return self

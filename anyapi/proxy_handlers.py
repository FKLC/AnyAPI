class NoProxy:
    def get(self, _):
        return None


class RateLimitProxy:  # pragma: no cover
    def __init__(self, proxies, paths, default=None):
        self.proxies = proxies
        self.proxy_count = len(proxies)
        self.access_counter = {
            path: {"limit": paths[path], "count": 0} for path in paths.keys()
        }
        self.default = {"http": default, "https": default}

    def get(self, keyword_arguments):
        counter = self.access_counter.get(keyword_arguments["path"])
        if counter is not None:
            proxy = self.proxies[
                (counter["count"] // counter["limit"] - self.proxy_count)
                % self.proxy_count
            ]
            counter["count"] += 1
            return {"http": proxy, "https": proxy}

        return self.default

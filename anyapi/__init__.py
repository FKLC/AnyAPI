from urllib.parse import urlparse
import copy
import requests


class AnyAPI:
    HTTP_METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']

    def __init__(self,
                 base_url,
                 default_params={},
                 default_headers={},
                 default_data={},
                 default_json={},
                 default_auth=(),
                 proxy_configration={},
                 scoped_call=None):

        self._base_url = base_url[:-1] if base_url.endswith('/') else base_url
        self._recursive_path = ''
        # since we can't pass data and json we have to store them in class
        self._default_data = default_data
        self._default_json = default_json

        self._session = requests.Session()
        self._session.params = default_params
        self._session.headers = default_headers
        self._session.auth = default_auth

        # Init empty filters list
        self._filter_params = []
        self._filter_headers = []
        self._filter_data = []
        self._filter_json = []
        self._filter_response = []

        if proxy_configration:
            proxy_default = proxy_configration.get('default')
            proxy_paths = proxy_configration.get('paths')
            proxy_proxies = proxy_configration.get('proxies')

            if proxy_default:
                self._default_proxy = {
                    'http': proxy_default,
                    'https': proxy_default,
                }
            if proxy_paths and proxy_proxies:
                for path in proxy_paths.keys():
                    proxy_paths[path] = {
                        'limit': proxy_paths[path],
                        'count': 0
                    }
                self._limited_paths = proxy_paths
                self._proxies = proxy_proxies
                self._proxy_count = len(proxy_proxies)
        self._is_proxies_set = isinstance(self._proxies, list)
        self._is_default_proxy_set = isinstance(self._default_proxy, dict)

        if scoped_call:
            self._scoped_call = scoped_call
        self._scoped_call_set = bool(scoped_call)

    def _make_request(self, path, method, **kwargs):
        """Return a requests.response

        Actual called method when any method call happens
        """
        # passing auth will override default_auth
        if not kwargs.get('auth'):
            # if make_request called directly auth may not exist
            kwargs['auth'] = ''
            del kwargs['auth']

        # if url passed, export path from it, then delete to prevent passing
        # url two times which causes error
        if kwargs.get('url'):
            url = kwargs.get('url')
            path = urlparse(url).path
            del kwargs['url']
        else:
            url = self._base_url + path

        # merge default and user passed data and json
        kwargs['data'] = {**self._default_data, **kwargs.get('data', {})}
        kwargs['json'] = {**self._default_json, **kwargs.get('json', {})}

        # keyword_arguments to pass filter functions
        keyword_arguments = {
            'params': kwargs.get('params', {}),
            'headers': kwargs.get('headers', {}),
            'data': kwargs.get('data', {}),
            'json': kwargs.get('json', {}),
            'path': path,
            'url': url
        }
        # apply all filter functions
        for function in self._filter_params:
            kwargs['params'] = function(**keyword_arguments)
        for function in self._filter_headers:
            kwargs['headers'] = function(**keyword_arguments)
        for function in self._filter_data:
            kwargs['data'] = function(**keyword_arguments)
        for function in self._filter_json:
            kwargs['json'] = function(**keyword_arguments)

        # delete empty kwargs
        for key in list(kwargs.keys()):
            if not kwargs[key]:
                del kwargs[key]

        if self._is_proxies_set and path in self._limited_paths:
            use_count = self._limited_paths[path]['count']
            limit = self._limited_paths[path]['limit']
            proxy_to_use = self._proxies[
                (use_count // limit - self._proxy_count) % self._proxy_count]
            self._limited_paths[path]['count'] += 1
            self._session.proxies = {
                'http': proxy_to_use,
                'https': proxy_to_use,
            }
        else:
            if self._is_default_proxy_set:
                self._session.proxies = self._default_proxy
            else:
                self._session.proxies = None

        # call requests.Session.{method}(url, **kwargs)
        if self._scoped_call_set:
            response = self._scoped_call(lambda: getattr(self._session, method.lower())(url, **kwargs))
        else:
            response = getattr(self._session, method.lower())(url, **kwargs)
        # apply filters for filter_response
        for function in self._filter_response:
            response = function(**keyword_arguments, response=response)

        return response

    def __getattr__(self, path):
        """Return a function or a AnyAPI

        When any class attribute called this method called so modifying
        __getattr__ to return make_request will make all attributes equal as
        calling make_request.
        """
        if path.startswith('__'):
            raise AttributeError(path)

        if path in AnyAPI.HTTP_METHODS:
            return (lambda  params={},
                            headers={},
                            data={},
                            json={},
                            auth=(),
                            url='':
                            self._make_request(path=self._recursive_path,
                                              method=path,
                                              params=params,
                                              headers=headers,
                                              data=data,
                                              auth=auth,
                                              json=json,
                                              url=url))
        elif path == 'P':

            def make_copy(path):
                self_copy = copy.copy(self)
                self_copy._recursive_path = self._recursive_path + '/' + path
                return self_copy

            return (lambda path: make_copy(path))
        else:
            self_copy = copy.copy(self)
            self_copy._recursive_path = self._recursive_path + '/' + path
            return self_copy

from urllib.parse import urlparse
import requests


class AnyAPI:
    def __init__(self,
                 base_url,
                 default_params={},
                 default_headers={},
                 default_data={},
                 default_json={},
                 default_auth=()):
        # add slash at the end to avoid putting double underscores for no reason
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        # since we can't pass data and json we have to store them in class
        self.default_data = default_data
        self.default_json = default_json

        self.session = requests.Session()
        self.session.params = default_params
        self.session.headers = default_headers
        self.session.auth = default_auth

        # Init empty filters list
        self.filter_params = []
        self.filter_headers = []
        self.filter_data = []
        self.filter_json = []
        self.filter_response = []

    def make_request(self, path, method, **kwargs):
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
            url = self.base_url + path

        # if url passed or make_request called directly strip slash
        if path.startswith('/'):
            path = path[1:]

        # merge default and user passed data and json
        kwargs['data'] = {**self.default_data, **kwargs.get('data', {})}
        kwargs['json'] = {**self.default_json, **kwargs.get('json', {})}

        # keyword_arguments to pass filter functions
        keyword_arguments = {'params': kwargs.get('params', {}),
                            'headers': kwargs.get('headers', {}),
                            'data': kwargs.get('data', {}),
                            'json': kwargs.get('json', {}),
                            'path': path,
                            'url': url}
        # apply all filter functions
        for function in self.filter_params:
            kwargs['params'] = function(**keyword_arguments)
        for function in self.filter_headers:
            kwargs['headers'] = function(**keyword_arguments)
        for function in self.filter_data:
            kwargs['data'] = function(**keyword_arguments)
        for function in self.filter_json:
            kwargs['json'] = function(**keyword_arguments)

        # delete empty kwargs
        for key in list(kwargs.keys()):
            if not kwargs[key]:
                del kwargs[key]

        # call request.session.{method}(url, **kwargs)
        response = getattr(self.session, method)(url, **kwargs)
        # apply filters for filter_response
        for function in self.filter_response:
            response = function(**keyword_arguments, response=response)

        return response

    def __getattr__(self, path):
        """Return a function

        When any class attribute called this method called so modifying
        __getattr__ to return make_request will make all attributes equal as
        calling make_request. Also I used lambda instead of creating another
        method because it would limit calls.
        """
        path, method = path.split('___')
        path = path.replace('__', '/')
        method = method.lower()
        return (lambda  params={},
                        headers={},
                        data={},
                        json={},
                        auth=(),
                        url='':
                        self.make_request(path,
                                          method,
                                          params=params,
                                          headers=headers,
                                          data=data,
                                          auth=auth,
                                          json=json,
                                          url=url))

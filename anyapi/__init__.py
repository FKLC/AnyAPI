import requests


class AnyAPI:
    def __init__(self,
                 base_url,
                 default_params={},
                 default_headers={},
                 default_data={},
                 default_json={},
                 default_auth=()):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.default_data = default_data
        self.default_json = default_json

        self.session = requests.Session()
        self.session.params = default_params
        self.session.headers = default_headers
        self.session.auth = default_auth

        self.filter_params = []
        self.filter_headers = []
        self.filter_data = []
        self.filter_json = []
        self.filter_response = []

    def make_request(self, path, method, **kwargs):
        if not kwargs.get('auth', ()):
            kwargs['auth'] = ''
            del kwargs['auth']
        kwargs['data'] = {**kwargs.get('data', {}), **self.default_data}
        kwargs['json'] = {**kwargs.get('json', {}), **self.default_json}

        keyword_arguments = {'params': kwargs.get('params', {}),
                            'headers': kwargs.get('headers', {}),
                            'data': kwargs.get('data', {}),
                            'json': kwargs.get('json', {}),
                            'path': path}
        for function in self.filter_params:
            kwargs['params'] = function(**keyword_arguments)
        for function in self.filter_headers:
            kwargs['headers'] = function(**keyword_arguments)
        for function in self.filter_data:
            kwargs['data'] = function(**keyword_arguments)
        for function in self.filter_json:
            kwargs['json'] = function(**keyword_arguments)

        for key in list(kwargs.keys()):
            if not kwargs[key]:
                del kwargs[key]

        response = getattr(self.session, method)(self.base_url + path,
                                                 **kwargs)
        for function in self.filter_response:
            response = function(**keyword_arguments, response=response)

        return response

    def __getattr__(self, path):
        path, method = path.split('___')
        path = path.replace('__', '/')
        method = method.lower()
        return (lambda  params={},
                        headers={},
                        data={},
                        json={},
                        auth=():
                        self.make_request(path,
                                          method,
                                          params=params,
                                          headers=headers,
                                          data=data,
                                          auth=auth,
                                          json=json))

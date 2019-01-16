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

    def make_request(self, path, method, **kwargs):
        if not kwargs.get('auth', ()):
            kwargs['auth'] = ''
            del kwargs['auth']
        kwargs['data'] = {**kwargs.get('data', {}), **self.default_data}
        kwargs['json'] = {**kwargs.get('json', {}), **self.default_json}
        for key in list(kwargs.keys()):
            if not kwargs[key]:
                del kwargs[key]

        return getattr(self.session, method)(self.base_url + path,
                                                 **kwargs)

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

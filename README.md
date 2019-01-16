# AnyAPI
AnyAPI is a package that I developed for myself to have a better looking code instead putting urls to everywhere I used dynamic method calls to access a endpoint.

For Examle if I want to make request to https://httpbin.org/anything/endpoint
```python
from anyapi import AnyAPI

base_url = 'https://httpbin.org'
api = AnyAPI(
    base_url,
    default_params={},
    default_headers={},
    default_data={},
    default_json={},
    default_auth=())
api.anything__endpoint___get(params={}, headers={}, data={}, json={}, auth=())
```
As you can see double underscores are pretended as slash and at the end you should put three underscores and HTTP method you want to use.

Since this package built on to [requests](https://github.com/requests/requests) you can use all auth libraries such as [requests-oauthlib](https://github.com/requests/requests-oauthlib), [requests-kerberos](https://github.com/requests/requests-kerberos), [requests-ntlm](https://github.com/requests/requests-ntlm).

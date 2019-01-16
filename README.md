# AnyAPI
AnyAPI is a package that I developed for myself to have a better looking code instead putting urls to everywhere I used dynamic method calls to access a endpoint.

For example if I want to make request to https://httpbin.org/anything/endpoint
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

## (Not) Frequently asked questions:
#### What if I need to access a endpoint which have dots inside url
Due that most of the APIs doesn't use dots at their endpoints I didn't thought a way for this instead use `make_request` method directly. For example
```python
from anyapi import AnyAPI

api = AnyAPI('https://httpbin.org')
api.make_request(path='anything/file_extension_on_api_endpoint_but_why.json',
                method='get',
                params={},
                headers={},
                data={},
                json={},
                auth=())
```

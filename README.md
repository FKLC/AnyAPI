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


## (Not) Frequently asked questions:

#### What is filter_{attribute} ?
If you want to set headers, params, data, json automatically before request you append your function to set them. For example
```python
import datetime
from anyapi import AnyAPI


def set_date_as_header(headers, **kwargs):
    now = datetime.datetime.now()
    return {**headers,
            'date': now.strftime('%B %d %Y')}


api = AnyAPI('https://httpbin.org')
api.filter_headers.append(set_date_as_header)

print(api.anything__endpoint___get().json())

# output
{
   'args': {},
   'data': '',
   'files': {},
   'form': {},
   'headers': {
      'Accept-Encoding': 'identity',
      'Connection': 'close',
      'Date': 'January 16 2019',
      'Host': 'httpbin.org'
   },
   'json': None,
   'method': 'GET',
   'origin': 'XX.XX.XX.XX',
   'url': 'https://httpbin.org/anything/endpoint'
}
```

#### What is filter_response ?
Lets suppose you want to raise error if response isn't what you expected for or you want to log it or some action after you get response and this is what is filter_response stands for. For Example:
```python
from anyapi import AnyAPI


def check_http_status_code(response, **kwargs):
    if response.status_code != 200:
      raise Exception(f'API returned {response.status_code}')
    return response


api = AnyAPI('https://httpbin.org')
api.filter_response.append(check_http_status_code)

api.status__500___get()
```

#### What can I use for auth attribute?
Since this package built on to [requests](https://github.com/requests/requests) you can use all auth libraries such as [requests-oauthlib](https://github.com/requests/requests-oauthlib), [requests-kerberos](https://github.com/requests/requests-kerberos), [requests-ntlm](https://github.com/requests/requests-ntlm).

#### What if I need to access a parent path?
If you only going to need it once or twice in your code you can pass `url` directly but if you going to use it many times you can may think to change `base_url` to make your code look better.
###### NOTE: if you pass url `path` is not going to be processed.


#### What if I need to access a endpoint which have dots inside url?
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

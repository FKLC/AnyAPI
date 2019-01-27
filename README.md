# AnyAPI
AnyAPI is a library that I developed for myself to have better looking code instead putting URLs to everywhere I used dynamic method calls to access a endpoint.

### Features
* Have better looking code using dynamic method calls
* Filters to help you to modify request, raise errors or log requests instead of writing functions everywhere.
* Automatically changing proxy according to rate limits specified by you for every path


***

### Examples
Making GET request to https://httpbin.org/anything/endpoint
```python
from anyapi import AnyAPI


base_url = 'https://httpbin.org'
api = AnyAPI(base_url)

api.anything.endpoint.GET()
```
As you can see dots are pretended as slash and at the end you should put dot and HTTP method you want to use in capital letters.

***

Setting header before every request
```python
import datetime
from anyapi import AnyAPI


def set_date_as_header(headers, **kwargs):
    now = datetime.datetime.now()
    return {**headers,
            'date': now.strftime('%B %d %Y')}

api = AnyAPI('https://httpbin.org')
api._filter_headers.append(set_date_as_header)

print(api.anything.endpoint.GET().json())
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
As you can see filter worked as expected and set `Date` header.

***

Changing proxy automatically after they reach their rate limit
```python
from anyapi import AnyAPI

proxy_configration = {
  'default': proxy0,
  'proxies': [proxy0, proxy1, proxy2,....], # don't forget to add default proxy!
  'paths': {
    '/anything': rate_limit0,
    '/anything/endpoint': rate_limit1
  }
}

api = AnyAPI('https://httpbin.org', proxy_configration=proxy_configration)

for i in range(10):
  print(api.anything.endpoint.GET().json())
```
If you check output of the all them you can see proxy changes when it reaches limit.

### This library is not a new thing
There is a lot of libraries you can find out there for example [Uplink](https://github.com/prkumar/uplink/), [Hammock](https://github.com/kadirpekel/hammock) and many more

***

## Installation
Library is avaible on PyPi so just run

```
pip install anyapi
```


# To learn more about AnyAPI check [wiki page](https://github.com/FKLC/AnyAPI/wiki/)

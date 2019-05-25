# AnyAPI

![Travis (.org)](https://img.shields.io/travis/FKLC/AnyAPI.svg?style=flat-square)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/FKLC/AnyAPI.svg?style=flat-square)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/FKLC/AnyAPI.svg?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/anyapi.svg?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/AnyAPI.svg?style=flat-square)

AnyAPI is a library that helps you to write any API wrappers with ease and in pythonic way.

### Features

- Have better looking code using dynamic method calls.
- Filters to help you to modify request, raise errors or log requests instead of writing functions everywhere.
- Scoped calls to raise errors and take action if necessary.
- Automatic retrying if the condition met with what you passed.
- Built-in rate limit proxy changer. (you can write your own proxy handler)
- Since it is built on top of requests anything compatible with it is compatible with AnyAPI.

But most importantly in AnyAPI almost everything is modular!

---

### Examples

Making GET request to https://httpbin.org/anything/endpoint

```python
from anyapi import AnyAPI


base_url = 'https://httpbin.org'
api = AnyAPI(base_url)

api.anything.endpoint.GET()
```

As you can see dots are pretended as slash and at the end you should put dot and HTTP method you want to use in capital letters.

---

Setting header before every request

```python
import datetime
from anyapi import AnyAPI


def set_date_as_header(kwargs):
    now = datetime.datetime.now()
    kwargs['headers'].update({'date': now.strftime('%B %d %Y')})

    return kwargs

api = AnyAPI('https://httpbin.org')
api._filter_request.append(set_date_as_header)

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

---

Changing proxy automatically after they reach their rate limit

```python
from anyapi import AnyAPI
from anyapi.proxy_handlers import RateLimitProxy

proxy_configuration = {
  'default': proxy0,
  'proxies': [proxy0, proxy1, proxy2,....], # don't forget to add default proxy!
  'paths': {
    '/anything': rate_limit0,
    '/anything/endpoint': rate_limit1
  }
}

api = AnyAPI('https://httpbin.org', proxy_configuration=proxy_configuration, proxy_handler=RateLimitProxy)

for i in range(10):
  print(api.anything.endpoint.GET().json())
```

If you check output of the all them you can see proxy changes when it reaches limit.

### This library is not a new thing

There is a lot of libraries you can find out there for example [Uplink](https://github.com/prkumar/uplink/), [Hammock](https://github.com/kadirpekel/hammock) and many more...

---

## Installation

Library on PyPI so just run

```console
pip install anyapi
```

# To learn more about AnyAPI check [wiki page](https://github.com/FKLC/AnyAPI/wiki/)

# AnyAPI
AnyAPI is a library that I developed for myself to have better looking code instead putting URLs to everywhere I used dynamic method calls to access a endpoint. Also this library provides `filters` to help you to modify request, raise errors or log requests instead of writing them everywhere to make your code more manageable.

For example if I want to make request to https://httpbin.org/anything/endpoint
```python
from anyapi import AnyAPI


base_url = 'https://httpbin.org'
api = AnyAPI(base_url)

api.anything__endpoint___get()
```
As you can see double underscores are pretended as slash and at the end you should put three underscores and HTTP method you want to use.

***

For example if I want to set header before every request I have to do the following
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
As you can see filter worked as expected and set `Date` header.

## Installion
Library is avaible on PyPi so just run

```
pip install anyapi
```

### For Advanced Users
After publishing this in [r/Python](https://www.reddit.com/r/Python/) [preslavrachev](https://www.reddit.com/user/preslavrachev) made a [comment](https://www.reddit.com/r/Python/comments/ahlqau/announcement_of_anyapi_a_python_library_to_help/eegcc8o) about [Uplink library](https://github.com/prkumar/uplink/) which is definitely a better library than mine. You should definitely check it out.


# To learn more about AnyAPI check [wiki page](https://github.com/FKLC/AnyAPI/wiki/)

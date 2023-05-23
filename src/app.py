from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from os import environ
from functools import reduce
import re, json, requests

load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = False
limiter = Limiter(app, key_func=get_remote_address)

WHITELIST = json.loads(environ.get("WHITELIST"))
HEADERS = json.loads(environ.get("HEADERS"))
PORT = int(environ.get("PORT"))
ENCODING = "UTF-8"


def get_error(error, description, status_code):
    return {
        "success": False,
        "error": error,
        "description": description,
    }, status_code


def process(url: str, res_headers: "list[str]", req_headers):
    if not reduce(lambda a, b: bool(re.match(b, url)) or a, WHITELIST, False):
        return get_error(
            "not_in_whitelist", "Provided url is not defined in current whitelist", 400
        )

    print(req_headers)

    url_response = requests.get(url, allow_redirects=True, headers=req_headers)
    response = Response(url_response.content.decode(ENCODING), url_response.status_code)

    for header in res_headers:
        if header not in HEADERS:
            return get_error(
                "not_in_headers",
                "Provided header is not defined in current headers",
                400,
            )
        header_kv = HEADERS[header]
        response.headers[header_kv[0]] = header_kv[1]

    return response


@app.route("/")
@limiter.limit("1/second")
def get():
    args = request.args
    url: str = args.get("url")
    req_headers = request.headers
    res_headers: list[str] = (
        args.get("headers").split(",") if args.get("headers") != None else []
    )

    if url == None or url.isspace():
        return get_error("missing_parameter", "Missing url parameter", 400)

    return process(url, res_headers, req_headers)


def main():
    app.run(host="0.0.0.0", port=PORT, threaded=True, use_reloader=True)


if __name__ == "__main__":
    main()

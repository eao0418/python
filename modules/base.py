import urllib
from urllib.request import Request
from http.client import HTTPResponse

class ApiHandler():
    def __init__(self):
        pass

    def make_http_request(self,
                          url: str,
                          method: str,
                          body: dict = None,
                          headers: dict = None) -> HTTPResponse:

        response = None

        req = Request(url=url)

        if (None != body):
            req.data = body

        if (None != headers):

            for k, v in headers:
                req.add_header(k, headers[k])

        response = urllib.request.urlopen(req)

        return response

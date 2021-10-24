import urllib
from urllib.request import Request
import json


class ApiHandler():
    def __init__(self):
        pass

    def make_http_request(self,
                          url: str,
                          method: str,
                          body: dict = None,
                          headers: dict = None):

        response = None

        req = Request(url=url)

        if (None != body):
            req.data = body

        if (None != headers):

            for k, v in headers:
                req.add_header(k, headers[k])

        # print("sending request to " + url)
        response = json.load(urllib.request.urlopen(req))
        # print(response)
        return response

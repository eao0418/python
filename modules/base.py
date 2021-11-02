#!/usr/bin/python
import urllib
from json import dumps
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

        req = Request(url=url, method=method)

        if (None != body):
            req.data = bytes(dumps(body), encoding='utf8')

        if (None != headers):

            for k, v in headers.items():
                req.add_header(k, v)

        response = urllib.request.urlopen(req)

        return response

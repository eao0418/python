import urllib.request
import urllib.error
from json import load, dumps
import logging
from time import sleep

from modules.base import ApiHandler


class ScanClient(ApiHandler):
    """A class to handle the API requests to urlscan.io

    Written by Aaron eao0418
    """

    _logger = logging.getLogger(__name__)
    _key: str
    baseURL = "https://urlscan.io/api/v1/"

    def __init__(self, api_key: str):
        """Initializes a new instance of urlscan_client. 
        
        Keyword arguments:
        api_key -- Provide a valid API key.

        returns -- A new instance of urlscan_client.
        """
        self._key = api_key
        super()

    def submit_url(self, url: str, public: bool = True) -> object:
        """Submits a URL for scanning.

        The urlscan API allows non-public submissions. 
        Any URL that is submitted as non-public cannot have results retrieved via the API.

        Keyword arguments:
        url -- The URL to submit a scan request for.
        public -- A boolean value to specify whether a scan result is public (default True).
        
        returns -- JSON-formatted response.
        """
        self._logger.debug("submit_url: entering method")
        request_url = "{}{}".format(self.baseURL, "scan/")
        self._logger.debug('SubmitURL was: {}'.format(request_url))

        result = None

        if public:
            data = {
                'url': url,
                'public': 'on'
            }
        else:
            data = {'url': url}

        headers = {
            'API-Key': self._key,
            'Content-Type': 'application/json'
        }

        try:
            result = load(self.make_http_request(url=request_url,
                          body=data, headers=headers, method='POST'))
        except Exception:
            self._logger.exception(
                'submit_url: Caught an exception sending the request.')

        self._logger.debug("submit_url: exiting method")

        return result

    def retrieve_scan_results(self, uuid: str) -> object:
        """Retrieves a scan result for a given UUID.

        Requests to the URL will respond with 'HTTP 404' until the scan is done.
        
        Keyword arguments:
        
        uuid -- The unique identifier returned from the scan request.
        
        returns -- JSON-formatted response.
        """
        self._logger.debug("retrieve_scan_results: entering method")

        request_url = "{}result/{}/".format(self.baseURL, uuid)

        self._logger.debug('Request URL was: {}'.format(request_url))

        counter = 0
        result = None

        while True:

            if counter == 5:
                break
            else:
                counter += 1

            try:
                result = load(self.make_http_request(
                    url=request_url, method="GET"))
                self._logger.debug('Scan results returned.')

                break
            except urllib.error.HTTPError as e:
                self._logger.exception("exception while scanning for results")
                code = e.getcode()

                if code == 404:
                    self._logger.debug('Waiting for scan results.')
                    sleep(10)

        self._logger.debug('Return value was: {}'.format(dumps(result)))
        self._logger.debug("retrieve_scan_results: exiting method")

        return result
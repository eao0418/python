from modules.base import ApiHandler


class GeolocationClient(ApiHandler):
    _base_url = "https://api.ipgeolocation.io"
    _api_key = ""

    def __init__(self, api_key: str):
        """Creates a new instance of GeolocationClient
        Keyword Arguments:
        api_key -- The key used to make requests to the ipgeolocaiton API
        """
        super()
        if None == api_key or not api_key:
            raise Exception("api_key does not accept a None or empty str")
        else:
            self._api_key = api_key

    def lookup_ip_address(self, ip: str):
        """Gets the details for an IP address
        
        Keyword Arguments:
        ip -- The IP address to look up.
        
        Returns -- A formatted JSON object
        """

        if None == ip or not ip:
            raise Exception("ip is a required argument")

        endpoint_url = "ipgeo"

        url = "{}/{}?apiKey={}&ip={}".format(self._base_url, endpoint_url,
                                             self._api_key, ip)

        response = None
        response = self.make_http_request(url=url,
                                          method='GET',
                                          body=None,
                                          headers=None)
        return response

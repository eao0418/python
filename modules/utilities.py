from modules.base import ApiHandler
import socket
import re


class HeaderChecker(ApiHandler):
    _base_url = "https://api.ipgeolocation.io"
    _api_key = ""

    def __init__(self):
        """Creates a new instance of GeolocationClient
        Keyword Arguments:
        None
        """
        super()

    def get_address_headers(self, url: str, method: str = None, headers: dict = None, body: dict = None):
        """Gets the details for an IP address
        
        Keyword Arguments:
        url -- The URL to get the headers from.
        method -- The HTTP method to use
        headers -- Headers to use in the request
        body -- The body to use in the request.
        
        Returns -- A formatted JSON object
        """

        if None == url or not url:
            return []

        if None == method or not method:
            method = 'GET'

        is_insecure = False

        if (re.match(r"http://", url)):
            is_insecure = True

        response = None
        output = []
        host = re.sub("(?i).com[a-z0-9/\-_?=&.]+", ".com",
                      re.sub("www.", "", re.sub("https://|http://", "", url)))

        try:
            response = self.make_http_request(url=url,
                                              method=method,
                                              body=body,
                                              headers=headers)
        except Exception as e:
            print("ERROR: could not perform the request to {}, {}".format(host, e))
            output.extend([host, "", "", "", "", "", "{}".format(e)])

        if None != response:

            strict_transport_header = None
            content_security_header = None
            x_frame_header = None
            server_header = None

            if not is_insecure:
                strict_transport_header = response.getheader(
                    "Strict-Transport-Security")

            content_security_header = response.getheader(
                "Content-Security-Policy")
            x_frame_header = response.getheader("X-Frame-Options")
            server_header = response.getheader("Server")

            try:
                # check to see if the host is an IP address or hostname
                if re.match(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", host):
                    ip_address = host
                    host = socket.gethostbyaddr(ip_address)
                else:
                    ip_address = socket.gethostbyname(host)

                output.append(host)
                output.append(ip_address)
                headers_present = 0

                if None != strict_transport_header and strict_transport_header:
                    output.append(strict_transport_header)
                    headers_present += 1
                elif is_insecure:
                    output.append("")
                else:
                    output.append("MISSING")

                if None != content_security_header and content_security_header:
                    output.append(content_security_header)
                    headers_present += 1
                else:
                    output.append("MISSING")

                if None != x_frame_header and x_frame_header:
                    output.append(x_frame_header)
                    headers_present += 1
                else:
                    output.append("MISSING")

                if None != server_header and server_header:
                    output.append(server_header)
                else:
                    output.append("")

                if is_insecure:
                    output.append(
                        "Non-secure protocol used, Strict-Transport-Security not evaluated")
                else:
                    output.append("")

                if headers_present == 3 and (server_header == None and not server_header):
                    output = []

            except Exception as e:
                print("ERROR: caught an exception {}".format(e))

            response.close()
        return output

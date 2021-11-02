import logging
import socket
import re
import csv
from datetime import datetime
from json import dump

from modules.base import ApiHandler


class HeaderChecker(ApiHandler):

    _logger = logging.getLogger(__name__)

    def __init__(self):
        """Creates a new instance of GeolocationClient
        Keyword arguments:
        None
        """
        super()

    def get_address_headers(self, url: str, method: str = None, headers: dict = None, body: dict = None):
        """Gets the details for an IP address
        
        Keyword arguments:
        url -- The URL to get the headers from.
        method -- The HTTP method to use
        headers -- Headers to use in the request
        body -- The body to use in the request.
        
        Returns -- A formatted JSON object
        """
        self._logger.debug("get_address_headers: entering method")
        if None == url or not url:
            return []

        if None == method or not method:
            method = 'GET'

        is_insecure = False

        if (re.match(r"http://", url)):
            is_insecure = True

        response = None
        output = []

        host = url.split("/")[2]
        try:
            response = self.make_http_request(url=url,
                                              method=method,
                                              body=body,
                                              headers=headers)
        except Exception as e:
            self._logger.error(
                "get_address_headers: could not perform the request to {}".format(host), e)
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

                if None != strict_transport_header and strict_transport_header:
                    output.append(strict_transport_header)
                elif is_insecure:
                    output.append("")
                else:
                    output.append("MISSING")

                if None != content_security_header and content_security_header:
                    output.append(content_security_header)
                else:
                    output.append("MISSING")

                if None != x_frame_header and x_frame_header:
                    output.append(x_frame_header)
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

            except Exception as e:

                self._logger.error(
                    "get_address_headers: caught an exception", e)

            response.close()

        self._logger.debug("get_address_headers: exiting method")

        return output


class Util:
    """A class of random utilities
    
    Written by Aaron eao0418
    """
    _util_logger = logging.getLogger(__name__)

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'custom': {
                'format': '%(levelname)s %(asctime)s %(module)s %(name)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'custom'
            },
            'file_handler': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'custom',
                'filename': 'default_log.log'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file_handler'],
                'level': 'INFO',
                'formatter': 'custom'
            }
        }
    }

    def __init__(self):
        """Initializes a new instance of Util. 

        returns -- A new instance of Util.
        """

    @staticmethod
    def export_json(dict_val: str, export_path: str, export_name: str, timestamp=True) -> None:
        """Initializes a new instance of Util. 
        
        Keyword arguments:
        dict_val -- A dictionary object to dump out to a json file.
        export_path -- The file path to export the file to.
        export_name -- The name of the file.
        timestamp: A flag to add the timestamp to the end of the file

        returns -- None.
        """
        # Windows file path assumption
        if "\\" in export_path:
            if not export_path.endswith("\\"):
                # Add that ending backslash for the user.
                export_path += "\\"
        # *nix assumption
        elif "/" in export_path:
            if not export_path.endswith("/"):
                # Add that ending forwardslash for the user
                export_path += "/"

        if export_path:
            path = "{}{}.json".format(export_path, export_name)
        else:
            path = "{}.json".format(export_name)
        if timestamp:
            path = "{}_{}.json".format(path, datetime.utcnow().timestamp())

        try:
            with open(path, 'w') as outfile:

                dump(dict_val, outfile)

        except Exception as fe:
            print("ERROR: Exception caught when exporting file to {}. Message: {}".format(
                path, fe))

    @staticmethod
    def write_results_to_file(rows: list, header: list, file_name: str, timestamp=True) -> None:
        """Writes a list of list results to a file
        
        Keyword arguments:
        rows: The `list` of results to write to the csv
        header: The headers to write to the csv
        file_name: The name of the file, including directory path. 
        timestamp: A flag to add the timestamp to the end of the file

        returns -- None.
        """
        if timestamp:
            f_name = "{}_{}.csv".format(
                file_name, datetime.utcnow().timestamp())
        else:
            f_name = "{}.csv".format(file_name)

        with open(f_name, 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if rows != None and rows != []:

                writer.writerow(header)

                for row in rows:
                    writer.writerow(row)

        print("file exported with name {}".format(f_name))
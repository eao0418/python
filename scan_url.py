import logging
import logging.config
import argparse
import configparser
from os import path

from modules.urlscan import ScanClient
from modules.utilities import Util


def main():

    logger = logging.getLogger(__name__)
    logging.info("Starting Script {}".format(path.basename(__file__)))
    config = configparser.ConfigParser()
    config.read("conf.ini")
    key = config["UrlScan"]["key"]

    if None == key or not key:
        raise Exception("Key must be provided in conf.ini")

    parser = argparse.ArgumentParser(description='Process inputs.')
    parser.add_argument('--url', '-u', type=str,
                        help='The URL being analyzed.')
    parser.add_argument('--output_directory', '-oD', type=str,
                        help='The directory to place results files.')
    args = parser.parse_args()
    # argument variables
    input_url = args.url
    output_directory = args.output_directory

    logger.debug("main: entering function")

    scan_host = input_url.split("/")[2]

    client = ScanClient(api_key=key)
    submission = client.submit_url(url=input_url)

    if None != submission:
        uuid = submission.get('uuid')
        logger.debug("UUID from request is [ {} ]".format(uuid))

        if None != uuid and uuid:

            logger.debug("main: getting scan results")

            this_scan = client.retrieve_scan_results(uuid=uuid)

            if None != this_scan:
                scan_data = this_scan.get('data')
                Util.export_json(dict_val=scan_data, export_path=output_directory,
                                 export_name="{}_scan_data".format(scan_host))

                scan_task = this_scan.get('task')
                Util.export_json(dict_val=scan_task, export_path=output_directory,
                                 export_name="{}_scan_task".format(scan_host))

                scan_page = this_scan.get('page')
                Util.export_json(dict_val=scan_page, export_path=output_directory,
                                 export_name="{}_scan_page".format(scan_host))

                scan_lists = this_scan.get('lists')
                Util.export_json(dict_val=scan_lists, export_path=output_directory,
                                 export_name="{}_scan_lists".format(scan_host))

                scan_meta = this_scan.get('meta')
                Util.export_json(dict_val=scan_meta, export_path=output_directory,
                                 export_name="{}_scan_meta".format(scan_host))

                scan_stats = this_scan.get('stats')
                Util.export_json(dict_val=scan_stats, export_path=output_directory,
                                 export_name="{}_scan_stats".format(scan_host))

    logger.info("End of script.")


if __name__ == '__main__':
    from logging import config
    from modules.utilities import Util

    # Use the standard logging we have in the Util class
    config.dictConfig(Util.LOGGING_CONFIG)
    main()

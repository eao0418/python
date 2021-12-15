import multiprocessing
import configparser
import argparse
import csv
import ipaddress

from datetime import datetime
from functools import partial
from multiprocessing import Pool
from contextlib import closing

from modules.ipgeolocation import GeolocationClient
from modules.utilities import Util

# ip_scanner
# author: Aaron

def main():

    """
    Store sensitive information in a configuration file so that we don't 
    accidentally commit it to github
    """
    config = configparser.ConfigParser()
    config.read("conf.ini")
    key = config["Geolocation"]["key"]

    ip_help = "scans a single IP address"
    scan_file_help = "provides a text file of IP addresses to scan. "
    scan_file_help += "Cannot provide a file and a single IP"
    write_to_file_help = "tells the script to write output to a file "
    write_to_file_help += "rather than the console. Valid values for true "
    write_to_file_help += "are y, t, yes, true. Everything else is considered false"

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        help=ip_help,
                        type=str,
                        default=None,
                        required=False)
    parser.add_argument("--scan_file",
                        help=scan_file_help,
                        type=str,
                        required=False,
                        default=None)
    parser.add_argument("--write_to_file",
                        dest='write_to_file',
                        default=False,
                        help=write_to_file_help)
    args = parser.parse_args()

    ip = args.ip
    scan_file = args.scan_file
    write_output = False
    if args.write_to_file:
        arg_val = args.write_to_file
        if arg_val.lower() in ['y', 't', 'true', 'yes']:
            write_output = True

    ips = []

    if ip and scan_file:
        raise Exception("ip and scan_file cannot be used at the same time")

    if None != ip and None == scan_file:

        if "/" in ip:
            try:
                ip_objects = list(ipaddress.ip_network(ip))
            except ValueError:
                print("ERROR: the provided value is not valid CIDR notation: {}".format(ip))
            
            for object in ip_objects:
                if not object.is_private:
                    ips.append(format(object))
        else:
            ip_object = None
            try:
                ip_object = ipaddress.ip_address(ip)
            except ValueError:
                print("ERROR: the provided value is not a valid IP address: {}".format(ip))
                exit(1)

            if None != ip_object and not ip_object.is_private:
                ips.append(format(ip_object))
            else:
                print("Warn: {} is a private address and will not be scanned".format(
                    ip_object))
    elif None != scan_file:

        with open(scan_file, 'r') as f:

            for line in f:
            
                line = line.replace("\n", "").rstrip()
                if "/" in line:
                    try:
                        ip_objects = list(ipaddress.ip_network(line))
                    except ValueError as ve:
                        print("ERROR: the provided value is not valid CIDR notation: {}".format(line))
                    
                    for object in ip_objects:
                        if not object.is_private:
                            ips.append(format(object))
                else:
                    ip_object = None
                    try:
                        ip_object = ipaddress.ip_address(line)
                    except ValueError as ve:
                        print("ERROR: the provided value is not a valid IP address: {}".format(line))
                    
                    if None != ip_object and not ip_object.is_private:
                        ips.append(format(ip_object))
    else:
        raise Exception("ip or scan_file must be provided")

    if ips != []:
        results = []
        print("scanning provided non-private IPs")
        results = scan_ips(k = key, ip_list = ips)

        if results != []:
            
            if write_output:
                header = [
                    "ip_address", "organization", "isp", "country",
                    "state/province", "city"
                ]
                Util.write_results_to_file(results, header, "scan_result")
            else:
                for result in results:
                    print(
                        "ip_address: {}\norganization: {}\nisp: {}\ncountry {}\nstate/province: {}\ncity: {}\n{}"
                        .format(result[0], result[1], result[2], result[3],
                                result[4], result[5], "---------------"))
    else:
        raise Exception(
            "no ip addresses provided to scan or all addresses provided were private"
        )


def scan_ips(k: str, ip_list: list) -> list:

    output = []
    # in my past experience, if you use all cpus, you lose results
    usable_cpu = multiprocessing.cpu_count() - 1

    with closing(Pool(usable_cpu)) as pool:
        output = pool.map(partial(scan_single_ip, k), ip_list)

    return output


def scan_single_ip(key: str, search_ip: str) -> list:

    client = GeolocationClient(api_key = key)

    scan_result = None

    scan_result = client.lookup_ip_address(ip = search_ip)
    result = []

    if None != scan_result and scan_result:
        res_country = ""
        res_state = ""
        res_city = ""
        res_organization = ""
        res_isp = ""

        res_organization = scan_result["organization"]
        res_isp = scan_result["isp"]
        res_country = scan_result["country_name"]
        res_state = scan_result["state_prov"]
        res_city = scan_result["city"]

        result.extend([
            search_ip, res_organization, res_isp, res_country, res_state,
            res_city
        ])

    return result

if __name__ == '__main__':
    main()
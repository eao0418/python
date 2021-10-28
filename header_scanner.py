#!/usr/bin/python
import argparse
import csv
import multiprocessing
from contextlib import closing
from datetime import datetime
# Custom modules
from modules.utilities import HeaderChecker


def main():

    url_help = "reports on one URL"
    scan_file_help = "provides a text file of urls to scan. "
    scan_file_help += "Cannot provide a file and a single url"
    write_to_file_help = "tells the script to write output to a file rather "
    write_to_file_help = "than the console. Valid values for true are y, t, yes, "
    write_to_file_help = "true. Everything else is considered false"

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",
                        help=url_help,
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

    url = args.url
    scan_file = args.scan_file
    write_output = False
    if args.write_to_file:
        arg_val = args.write_to_file
        if arg_val.lower() in ['y', 't', 'true', 'yes']:
            write_output = True

    urls = []
    scan_result = []

    if url and scan_file:
        raise Exception(
            "url and scan_file cannot both be used at the same time")

    if None != url and url:
        urls.append(url)

    if None != scan_file and scan_file:
        with open(scan_file, 'r') as f:

            for line in f:
                urls.append(line.replace("\n", "").rstrip())

    if urls != []:

        print("INFO: Starting evaluation of URLs \n")
        
        file_header = ["Host Scanned", "IP Address", "Strict-Transport-Security",
                       "Content-Security-Policy", "X-Frame-Options", "Notes"]

        # in my past experience, if you use all cpus, you lose results
        usable_cpu = multiprocessing.cpu_count() - 1

        if len(urls) == 1:
            scan_result.append(check_headers(urls[0]))
        else:
            with closing(multiprocessing.Pool(usable_cpu)) as pool:
                try:
                    scan_result = pool.map(check_headers, urls)
                except Exception as e:
                    print(
                        "ERROR: caught an exception while running the header check {}".format(e))

    else:
        print("ERROR: no results were available to scan.")
        exit(1)

    if len(scan_result) > 0:

        if write_output:
            write_results_to_file(scan_result, file_header)
        else:
            print_formatted_results(scan_result, file_header)
    else:
        print("ERROR: No results were obtained from the assessment.")
        exit(1)


def write_results_to_file(rows: list, header: list):

    file_name = "{}_site_assessment.csv".format(datetime.utcnow().timestamp())
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if rows != None and rows != []:

            writer.writerow(header)

            for row in rows:
                writer.writerow(row)

    print("file exported with name {}".format(file_name))


def print_formatted_results(rows: list, headers: list) -> None:

    print("\nScan Results: \n")
    for row in rows:
        print("{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}".format(
            headers[0], row[0],
            headers[1], row[1],
            headers[2], row[2],
            headers[3], row[3],
            headers[4], row[4],
            headers[5], row[5],
            "\n"))


def check_headers(url: str) -> list:

    print("Checking url {}".format(url))
    header_checker = HeaderChecker()
    return header_checker.get_address_headers(url)


if __name__ == '__main__':
    main()

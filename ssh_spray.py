#!/usr/bin/python
import logging
import argparse
import multiprocessing
import configparser

from csv import DictWriter
from csv import QUOTE_ALL
from time import sleep
from argparse import ArgumentError
from paramiko import SSHClient
from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from paramiko import AutoAddPolicy
from functools import partial
from multiprocessing import Pool
from contextlib import closing

log = logging.getLogger(__name__)


def main():

    epilog = """
    View the project's README file for additional information on using the script.
    """
    parser = argparse.ArgumentParser(
        description="A simple script to spray SSH credentials", epilog=epilog)

    parser.add_argument("-th", "--host", required=False,
                        help="Use a single host target", type=str)
    parser.add_argument("-hf", "--host_file", required=False,
                        help="A file of hosts to test", type=str)
    parser.add_argument("-pf", "--password_file", required=False,
                        help="A file of passwords to use", type=str)
    parser.add_argument("-u", "--user_name", required=False,
                        type=str, help="A single username to use with the password list")
    parser.add_argument("-uf", "--user_file", required=False,
                        type=str, help="A file of usernames to use with the password list.")
    parser.add_argument("-c", "--chunk_size", type=int, required=False,
                        help="The number of requests to perform before waiting")
    parser.add_argument("-t", "--wait_time", type=int,
                        required=False, help="The number of seconds to pause for")
    parser.add_argument("-p", "--port", required=False,
                        help="The port to scan. Default is 22.", type=int)

    args = parser.parse_args()

    host = args.host
    host_file_path = args.host_file
    password_file_path = args.password_file
    target_user = args.user_name
    user_file_path = args.user_file
    chunk_size = args.chunk_size
    wait_time = args.wait_time
    port = args.port

    if None == port or port == 0:
        port = 22

    if None == chunk_size:
        chunk_size = 0

    if None == wait_time:
        wait_time = 0

    spray_results = []

    users = []
    passwords = []
    hosts = []

    usable_cpu = multiprocessing.cpu_count() - 4

    # Users
    if None != user_file_path and user_file_path:

        with open(user_file_path, 'r') as uf:

            for line in uf:

                users.append(line.replace("\n", "").rstrip())

    elif None != target_user and target_user:
        users.append(target_user)
    
    else:
        raise ArgumentError("Either --user_name or --user_file must be specified.")

    # Hosts
    if None != host_file_path and host_file_path:

        with open(host_file_path, 'r') as hf:

            for line in hf:
                hosts.append(line.replace("\n", "").rstrip())
    elif None != host and host:
        hosts.append(host)
    
    else:
        raise ArgumentError("Either --host or --host_file must be specified.")

    # Passwords
    if None != password_file_path and password_file_path:

        with open(password_file_path, 'r') as f:

            for line in f:
                passwords.append(line.replace("\n", "").rstrip())

    if len(hosts) > 0 and len(users) > 0 and len(passwords) > 0:

        if len(hosts) == 1:

            try:

                spray_results = test_ssh(
                    host, users, passwords, 22, chunk_size, wait_time)

            except Exception as e:

                log.exception("caught an exception spraying the host")

        else:
            multiprocess_results = []
            with closing(Pool(usable_cpu)) as pool:

                multiprocess_results = []

                try:

                    multiprocess_results = pool.map(partial(test_ssh, user_names=users, passwords=passwords,
                                            port=port, request_size=chunk_size, wait_time=wait_time), hosts)

                except KeyboardInterrupt:

                    log.exception("Keyboard interrupt detected")
                    exit(1)

            if len(multiprocess_results) > 0:

                for result in multiprocess_results:
                    spray_results.extend(result)

    if None != spray_results and len(spray_results) > 0:

        with open("ssh_credential_test_results.csv", 'w', newline='') as oF:

            fields = list(spray_results[0].keys())

            writer = DictWriter(oF, fieldnames=fields, quoting = QUOTE_ALL)

            writer.writeheader()

            for row in spray_results:

                writer.writerow(row)

def test_ssh(host: str, user_names: list, passwords: list,
              port: int = 22, request_size: int = 0,
              wait_time: int = 0) -> dict:
    """Tests the host with the provided user names and passwords
    
    Keyword arguments:
    host -- The host to try to log into
    user_names -- The list of user names to use on the login attempt
    passwords -- The list of passwords to try
    port -- The port to try to ssh to
    request_size -- The number of chunks to break requests into, with pauses between. 
    wait_time -- The time in seconds to pause after request sets

    returns -- A list of results
    """
    logging.debug("test_ssh: entering function")

    results = []

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)

    request_counter = 0

    request_total = len(user_names) * len(passwords)

    for user in user_names:

        for password in passwords:

            request_counter += 1

            result = dict()
            result["host"] = host
            result["user_name"] = user
            result["password"] = password

            try:

                client.connect(hostname=host, port=port,
                               username=user, password=password)

                result["login_result"] = "Success"
                client.close()

            except AuthenticationException:

                result["login_result"] = "Failure"

            except SSHException:
                logging.exception("test_ssh: caught an exception logging into {}".format(host))
                # sleep because the ssh server might be overwhelmed
                result["login_result"] = "SSHException"
                sleep(20)
            except Exception:

                result["login_result"] = "Unhandled Error"
                logging.exception(
                    "test_ssh: caught an exception while logging into {}".format(host))

            results.append(result)

            if request_size != 0 and wait_time != 0:

                if request_counter % request_size == 0 and request_counter < request_total:

                    logging.info("sleeping for {} seconds".format(wait_time))
                    sleep(wait_time)

    logging.debug("test_ssh: entering function")

    return results

if __name__ == '__main__':

    from logging import config
    from modules.utilities import Util

    # Use the standard logging we have in the Util class
    config.dictConfig(Util.LOGGING_CONFIG)
    main()

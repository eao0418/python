# ip_scanner
A small script that allows the user to get information about an IP address from ipgeolocation.io
### Prerequisites
None, this uses the standard library and custom code is all included.
### How to run the script
The script can be run in several modes. 
#### Scan one IP
Runs the script against one address
```shell
    ./ip_scanner.py --ip 131.253.12.5
```
#### Scan IPs from a file
Scans one or more IP addresses from a file 
```shell
    ./ip_scanner.py --scan_file ./ips.txt
```
#### Write the scan output to a file
```shell
    ./ip_scanner.py --scan_file ./ips.txt --write_to_file true
```

# header_scanner
A script that evaluates the presence of the following headers:

    - Strict-Transport-Security
    - Content-Security-Policy
    - X-Frame-Options
If any of the listed headers are missing, the output will indicate "MISSING," otherwise the value will be returned. The result can be printed to the screen or exported to a CSV file.
### Prerequisites
None, this uses the standard library and custom code is all included.
### How to run the script
The script can be run in several modes. 
#### Evaluate one url
Runs the script against one address
```shell
    ./header_scanner.py --url www.redsiege.com
```
#### Evaluate URLs from a file
Scans one or more IP addresses from a file 
```shell
    ./header_scanner.py --scan_file ./urls.txt
```
#### Write the output to a file
```shell
    ./header_scanner.py --scan_file ./urls.txt --write_to_file true
```

# ssh_spray
A script to test hosts for valid ssh credentials
### Prerequisits 
paramkio is required.
### How to run the script
The script can be run using a single host or a file of hosts, a single user name or a file of user names
#### Test multiple hosts with users from a file with a list of passwords
```shell
    ./ssh_spray.py -hf ./hosts.txt -pf ./passwords.txt -uf ./users.txt -c 5 -t 10
```
#### Test one host with one user name with a list of passwords
```shell
    ./ssh_spray.py -th 192.168.0.25 -pf ./passwords.txt -u root -c 5 -t 10
```

## *Author Name*
Aaron
eao0418
https://github.com/eao0418
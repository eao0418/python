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
    * Strict-Transport-Security
    * Content-Security-Policy
    * X-Frame-Options
If any of the listed headers are missing, a result will be generated. The result can be printed to the screen or exported to a CSV file.
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

## *Author Name*
Aaron
eao0418
https://github.com/eao0418
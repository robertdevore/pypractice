# :mag_right: Subdomain scanner

Enter a domain name to receive a list of all subdomains attached the parent domain

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

```
parameters:
-domain         : (-d) specify a domain name to scan.
-output         : (-o) optionally specify the output type - `file` or `print` (default)
```

### :computer: How to use

**Default**

`$ python3 SubdomainScanner.py -d domain.com`

**Print results in the terminal (same as default)**

`$ python3 SubdomainScanner.py -d domain.com -o print`

**Save results to file**

`$ python3 SubdomainScanner.py -d domain.com -o file`

### :pray: Thanks

w3w3w3 on YouTube put out [this tutorial](hhttps://www.youtube.com/watch?v=97YeadibQac) that I followed to create the orginal base version of this script.

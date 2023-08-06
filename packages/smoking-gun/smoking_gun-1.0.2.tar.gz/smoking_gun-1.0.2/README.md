# The Smoking Gun

[![Build Status](https://travis-ci.org/dopstar/smoking-gun.svg?branch=master)](https://travis-ci.org/dopstar/smoking-gun)
[![codecov](https://codecov.io/gh/dopstar/smoking-gun/branch/master/graph/badge.svg)](https://codecov.io/gh/dopstar/smoking-gun)
[![Python Version](https://img.shields.io/pypi/pyversions/smoking-gun.svg)](https://pypi.python.org/pypi/smoking-gun)
[![PyPI Status](https://img.shields.io/pypi/v/smoking-gun.svg)](https://pypi.python.org/pypi/smoking-gun)
[![Licence](https://img.shields.io/github/license/dopstar/smoking-gun.svg)](https://raw.githubusercontent.com/dopstar/smoking-gun/master/LICENSE)

This is a python library that has basic tools for log capturing.

## Installation

```shell
pip install smoking-gun
```


## Example

```python
import logging
import sys

import requests

from smoking_gun.logs import CapturedLogging


log_format = '[%(asctime)s][%(levelname)s][%(name)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

response = requests.get('http://github.com', allow_redirects=True)

# sample output:
# [2020-01-08 02:35:10,467][DEBUG][urllib3.connectionpool] Starting new HTTP connection (1): github.com:80
# [2020-01-08 02:35:11,023][DEBUG][urllib3.connectionpool] http://github.com:80 "GET / HTTP/1.1" 301 0
# [2020-01-08 02:35:11,027][DEBUG][urllib3.connectionpool] Starting new HTTPS connection (1): github.com:443
# [2020-01-08 02:35:11,938][DEBUG][urllib3.connectionpool] https://github.com:443 "GET / HTTP/1.1" 200 None

with CapturedLogging() as cl:
    response = requests.get('http://github.com', allow_redirects=True)

# no output

print(cl.logs)
# [2020-01-08 02:35:10,467][DEBUG][urllib3.connectionpool] Starting new HTTP connection (1): github.com:80
# [2020-01-08 02:35:11,023][DEBUG][urllib3.connectionpool] http://github.com:80 "GET / HTTP/1.1" 301 0
# [2020-01-08 02:35:11,027][DEBUG][urllib3.connectionpool] Starting new HTTPS connection (1): github.com:443
# [2020-01-08 02:35:11,938][DEBUG][urllib3.connectionpool] https://github.com:443 "GET / HTTP/1.1" 200 None
```

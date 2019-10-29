
# Gravity Housekeeper

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)

## About <a name = "about"></a>

The purpose of this project is to simplified the amount of blocklist in the `pihole` itself. It was believed that multiple file that rewrite daily gonna reduce the longevity of the flash media (sd card)

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

1. python 3.6   `because the use of f-string`

### Virtual Environment Initialization & Dependencies Installation

To avoid dependency conflict, it's advised to setup virtual environment using `venv`. This tutorial use on`Ubuntu` environment. 

0. Clone this repository `git clone https://github.com/aspartam206/gravity_housekeeper.git`
1. Install venv `sudo apt-get install python3-venv`
2. Create a new virtual environment inside project folder `python3 -m venv venv`, a new virtual environment will be generated inside `venv` folder
3. Activate venv, for UNIX OS (Linux, MacOS, etc...) use: `source ./venv/bin/activate`
	a. For Windows use `activate` script inside `./venv/Scripts`

### Installing Requirements
you should be able to running with just installing `requests`
```
pip install requests
```
or, if you use `pip-tools`
```
pip-compile
pip-sync
```
or, for recommended way by community standard, use `requirements.txt`
```
pip install -r requirements.txt
```
### Usages

If you just average user just copy these link to your `pihole` blocklist.
```
https://raw.githubusercontent.com/aspartam206/gravity_housekeeper/master/blocklist/ordered.txt
```



A step by step series how to get the compiled blocklist by yourself.
```
python3 download.py
```
or if you are under venv
```
python download.py
```
the blocklist would be generated on `./blocklist/ordered.txt`

### Project Structure
```
gravity_housekeeper/
├── LICENSE.md
├── README.md
├── blocklist         # dist folder for the compiled blocklist
│   ├── ignore.md
│   └── ordered.txt   # the compiled blocklist
├── download.py       # the python script to run
├── dwl               # temp folder for all blocklist that downloaded
│   ├── *.txt
│   └── ignore.md
├── package.json
├── requirements.in   # base requirements
└── requirements.txt  # static(stable) requirements
```
### License

```
Copyright (c) 2019 Mochammad Rizki(cyber.light52@gmail.com). All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

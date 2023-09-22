[![PyPI - Version](https://img.shields.io/pypi/v/hatch-fancy-pypi-readme.svg)](https://pypi.org/project/ddge)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-fancy-pypi-readme.svg)](https://pypi.org/project/ddge)

# DuckDuckGo Email Protection CLI
install via pip by doing

`pip install ddge`

```
usage: ddge [-h] [-c CONFIG] {login,logout,generate,aliases,remove} ...

DuckDuckGo Email CLI

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Custom config path.

actions:
  {login,logout,generate,aliases,remove}
    login               Allows you to login using the OTP code and saves the credentials.
    logout              Deletes the locally saved credentials.
    generate            The default action. Generates an alias
    aliases             Lists the created aliases.
    remove              Delete the alias from the local storage.
```

so after logging in you can just run the program to generate a new alias.
```
$ ddge
r5kog234s@duck.com
```

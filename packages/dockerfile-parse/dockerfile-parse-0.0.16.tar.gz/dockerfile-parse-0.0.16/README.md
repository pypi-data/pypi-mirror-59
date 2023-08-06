dockerfile-parse
====

[![Build Status](https://travis-ci.org/containerbuildsystem/dockerfile-parse.svg?branch=master)](https://travis-ci.org/containerbuildsystem/dockerfile-parse)
[![Coverage Status](https://coveralls.io/repos/containerbuildsystem/dockerfile-parse/badge.svg?branch=master&service=github)](https://coveralls.io/github/containerbuildsystem/dockerfile-parse?branch=master)

Python library for parsing Dockerfile files.

## Installation

### from PyPI

```
$ pip install dockerfile-parse
```


### from git

Clone this git repo and install dockerfile-parse using python installer:

```shell
$ git clone https://github.com/containerbuildsystem/dockerfile-parse.git
$ cd dockerfile-parse
$ sudo pip install .
```

## Usage

```python
from pprint import pprint
from dockerfile_parse import DockerfileParser

dfp = DockerfileParser()
dfp.content = """\
From  base
LABEL foo="bar baz"
USER  me"""

# Print the parsed structure:
pprint(dfp.structure)
pprint(dfp.json)
pprint(dfp.labels)

# Set a new base:
dfp.baseimage = 'centos:7'

# Print the new Dockerfile with an updated FROM line:
print(dfp.content)
```

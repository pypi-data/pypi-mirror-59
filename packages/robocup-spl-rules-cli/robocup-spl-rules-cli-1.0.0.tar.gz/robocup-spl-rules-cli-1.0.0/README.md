# RoboCup SPL Rules CLI

Open RoboCup SPL Rules in your web browser!
You can open rules of a particular year or default to the most recent rules.
Rules are taken from [here](https://spl.robocup.org/downloads/).

The regex should work until we hit a five digit year.
If humanity is still around by the year 10000 someone please fit it.


### Installation

```
pip install robocup-spl-rules-cli
```


### Usage

```
usage: rules [-h] [year]

open RoboCup SPL rules in your browser

positional arguments:
  year        the year of which to fetch the rules; defaults to most recent if ommited

optional arguments:
  -h, --help  show this help message and exit
```

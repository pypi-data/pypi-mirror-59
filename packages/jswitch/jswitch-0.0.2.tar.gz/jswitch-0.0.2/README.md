# jswitch

[![PyPI version](https://badge.fury.io/py/jswitch.svg)](https://pypi.org/project/jswitch/)

Currently beta and should not be considered stable.

<!-- ![Works in Windows, Mac, Linux](screenshots/screenshot1.png) -->

## Install

Install from pypi.org using pip:

```bash
python -m pip install jswitch
```

Install from source by running this from
the root of the source code directory:

```bash
python setup.py install
```

## Usage

Simply run `jswitch` from the command line to launch the menu.

```bash
jswitch
```

Or invoke via Python:

```bash
python -m jswitch
```

To use the tool inside PYthon source code:

```python
from jswitch import Jswitch

jswitch = Jswitch()
jswitch.run()
```

## Controls

- `Esc` or `q`: Quit
- `Enter`, `l`, or `Right Arrow`: Connect
- `j` or `Down Arrow`: Down
- `k` or `Up Arrow`: Up
- `e`: Edit config file

When using the Edit (`e`) command, it tries to use
the editor defined in `EDITOR` environment variable,
otherwise attempts to default to a system editor. 

## Source code

[https://github.com/DevDungeon/jswitch](https://github.com/DevDungeon/jswitch)

## Author

NanoDano <nanodano@devdungeon.com>


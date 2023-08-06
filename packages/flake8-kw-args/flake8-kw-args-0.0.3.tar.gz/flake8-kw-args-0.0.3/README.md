Flake8 plugin to check explicitly passed arguments.

  * [Getting Started](#getting-started)
    * [Disclaimer](#disclaimer)
    * [Installation](#installation)
  * [Usage](#usage)
    * [Command line interface](#command-line-interface)
    * [Examples](#examples)
  * [Development](#development)
    * [Clone the project](#clone-the-project)
    * [Tests](#tests)

## Getting Started

### Disclaimer

* This plugin is an extension to [flake8](http://flake8.pycqa.org/).
* For testing purposes we use [tox](https://tox.readthedocs.io/en/latest/9).

### Installation

Install using `pip3`:

```bash
$ pip3 install flake8-kw-args
```
## Usage

### Command line interface

Run `flake8`: 

```bash
$ flake8 [options] file file ...
```

### Examples

If there is no error the output is empty:

```bash
$ cat example.py
def get_user(name, surname):
    pass

get_user(name='Daniel', surname='Jenkins')
$ flake8 example.py
```

If there is an error the output is has error message indicating the file, line and column where the error was found:

```bash
$ cat example.py
def get_user(name, surname):
    pass

get_user(name='Daniel', 'Jenkins')
$ flake8 example.py
example.py:4:24: KWA: argument not passed by keyword.
```

# Development 

## Clone the project

To start working with the project, clone it with the following commands.

```
$ git clone git@github.com:casafari/flake8-kw-args.git
$ cd flake-kw-args
```

## Tests

Install it with `pip3`:

```bash
$ pip3 install tox
```

Now you can run the tests by with `tox`.

```bash
$ tox
```

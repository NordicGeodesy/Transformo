# Installation

!!! note

    Once development advances the installation method will be streamlined and made
    simpler.

Transformo is a command line application. The initial setup and subsequent work with
Transformo will all be done from a terminal application. Some proficiency with the
command line is expected.

## Prerequisites

You'll need git and [uv](https://github.com/astral-sh/uv) to proceed with the installation.
If you haven't got either already, start by downloading and installing
[git](https://git-scm.com/install/windows) and
[uv](https://github.com/astral-sh/uv).

## Setup

Transformo is best run using uv. Clone the repository from GitHub
and run the following commands in a suitable location:

```sh
$ git clone https://github.com/NordicGeodesy/Transformo.git
$ cd Transformo
$ uv venv .venv
$ source .venv/bin/activate
$ uv pip install .
```

Verify the installation by running a transformo command:

```sh
$ transformo --version
```

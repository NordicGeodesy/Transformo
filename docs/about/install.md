# Installation

!!! note

    Once development advances the installation method will be streamlined and made
    simpler.

Transformo is a command line application. The initial setup and subsequent work with
Transformo will all be done from a terminal application. Some proficiency with the
command line is expected.

## Prerequisites

You'll need git and a working Conda setup to proceed with the installation.
If you haven't got either already, start på downloading and installing
[git](https://git-scm.com/install/windows) and
[Miniforge](https://conda-forge.org/download/).

## Setup

Transformo is best run in a Conda environment. Clone the repository from GitHub
and run the following commands in a suitable location:

```sh
$ git clone https://github.com/NordicGeodesy/Transformo.git
$ cd Transformo
$ mamba env create -f environment.yml
$ mamba activate transformo
$ pip install .
```

Verify the installation by running a transformo command:

```sh
$ transformo --version
```

# For developers

This section is only relevant for developers working on the software. The code
is kept in a git repository on GitHub under the Nordic Geodetic Commisions organisation.

Find the repository here:
[github.com/NordicGeodesy/Transformo](https://github.com/NordicGeodesy/Transformo).

## Installation

The installation process is similar to the one for regular users,
although the installed Python environment includes essential tools
for development as well:

```sh
uv sync --dev
```

On top of setting up a Python environment and installing the package
developers also need to set up pre-commit scripts for git:

```sh
pre-commit install
```

## Code quality

We strive to keep the code quality in Transformo as high as possible. A number of
measures has been put into place to support this. They are described in the sections
below.

### Tests

We do not accept code in the main-branch that is not sufficiently tested. The
Transformo code is tested in a Pytest test-suite. New code should come with
sufficient tests to ensure the long-term reliability of the software. All tests
should be passing before merging into the main branch.

### Type annotations

Type annotations in Python improves readability of the code immensely and as an added
bonus it helps IDE's improve developer workflows. In addition, Transformo relies
heavily on the Pydantic framework which leverages type annotations to validate
incoming data.

MyPy is used to check that the types in Transformo are consistent throughout the
code. This can at times be a bit painful but it comes with the added benefit that it
can uncover errors in the code that normally wouldn't be noticed when relying on
Pythons dynamic nature.

### Pydantic

Basic types in Transformo, such as `DataSource`'s and `Operators`'s, are Pydantic
`BaseModel`'s. Pydantic is used to validate user input in a simple way, in an
attempt to avoid problems caused by ill-formed input data. Transformo is built
on Pydantic's capability to serializee Python objects from a text source. In this
case the entire pipeline given in YAML format.

### Black

The code is formatted using Black. Formatting by black can be turned off in sections
of the code where alternative formatting can be used to express the code in more
clear terms. The most likely case for this is where mathematical formulas are turned
into code, for example when setting up a rotation matrix.

### Pre-commit hooks

Pre-commit hooks are used to enforce most of the above requirements to the code.

Remember to initialize the pre-commit hooks before committing your first code.

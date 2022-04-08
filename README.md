# climlab-emanuel-convection

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/climlab/climlab-emanuel-convection/build-and-test/main?logo=github&style=for-the-badge)

Brian Rose, University at Albany

## About

This is a stand-alone Python wrapper for the [Emanuel convection scheme](https://emanuel.mit.edu/problem-convective-moistening).

The primary use-case is to serve as the under-the-hood moist convection driver
for [climlab](https://climlab.readthedocs.io/), but it can be used as a
stand-alone model if you are familiar with [Fortran source code](https://emanuel.mit.edu/FORTRAN-subroutine-convect).
This is a lightweight wrapper that emulates the Fortran interface as closely as possible.
The original `convect43c` code is bundled here, courtesy of Kerry Emanuel.

## Installation

Pre-built binaries for many platforms will be available to install from conda-forge. Stay tuned.

For now, please build from source (instructions below).

## Example usage

You can import the Fortran driver into a Python session with
```
from climlab_emanuel_convection import emanuel_convection
```

Please see the directory `climlab_emanuel_convection/tests/` directory in this repository
for working examples that set up all the necessary input arrays and call the driver.

## Building from source

Here are instructions to create a build environment (including Fortran compiler)
with conda/mamba and build using f2py.
It should be possible to build using other Fortran compilers, but I haven't tested this.

To build *(example for Apple M1 machine, see `./ci/` for other environment files)*:
```
mamba create --name convect_build_env python=3.10 --channel conda-forge
mamba env update --file ./ci/requirements-macos-arm64.yml
conda activate convect_build_env
python -m pip install . --no-deps -vv
```

To run tests, do this from any directory other than the climlab_rrtmg repo:
```
pytest -v --pyargs climlab_emanuel_convection
```

## Version history

Version 0.2 is the first public release (April 2022).
The Python wrapper code has been extracted from
[climlab v0.7.13](https://github.com/brian-rose/climlab/releases/tag/v0.7.13).

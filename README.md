# climlab-emanuel-convection

![build-and-test workflow](https://github.com/climlab/climlab-emanuel-convection/actions/workflows/build-and-test.yml/badge.svg)

Brian Rose, University at Albany

## About

This is a stand-alone Python wrapper for the [Emanuel convection scheme](https://emanuel.mit.edu/problem-convective-moistening).

The primary use-case is to serve as the under-the-hood moist convection driver
for [climlab](https://climlab.readthedocs.io/), but it can be used as a
stand-alone model if you are familiar with [Fortran source code](https://emanuel.mit.edu/FORTRAN-subroutine-convect).
This is a lightweight wrapper that emulates the Fortran interface as closely as possible.
The original `convect43c` code is bundled here, courtesy of Kerry Emanuel.

## Installation

Pre-built binaries for many platforms are available from [conda-forge](https://conda-forge.org).

To install in the current environment:
```
conda install climlab-emanuel-convection --channel conda-forge
```
or create a self-contained environment:
```
conda create --name my_env python=3.10 climlab-emanuel-convection --channel conda-forge
conda activate my_env
```

See below for instructions on how to build from source.

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

To run tests, do this from any directory other than the climlab-emanuel-convection repo:
```
pytest -v --pyargs climlab_emanuel_convection
```

## Version history

Version 0.2 is the first public release (April 2022).
The Python wrapper code has been extracted from
[climlab v0.7.13](https://github.com/brian-rose/climlab/releases/tag/v0.7.13).

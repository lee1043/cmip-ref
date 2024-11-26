# CMIP Rapid Evaluation Framework


<!--- --8<-- [start:description] -->

**Status**: This project is in active development. We expect to be ready for beta releases in Q2 2025.

The CMIP Rapid Evaluation Framework is a Python application that provides the ability to rapidly process and
evaluate CMIP data against a set of reference data.
It is designed to be used as a CI/CD pipeline to provide a quick validation of CMIP data.

CMIP REF is a community project, and we welcome contributions from anyone.


[![CI](https://github.com/CMIP-REF/cmip-ref/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/CMIP-REF/cmip-ref/actions/workflows/ci.yaml)
[![Coverage](https://codecov.io/gh/CMIP-REF/cmip-ref/branch/main/graph/badge.svg)](https://codecov.io/gh/CMIP-REF/cmip-ref)
[![Docs](https://readthedocs.org/projects/cmip-ref/badge/?version=latest)](https://cmip-ref.readthedocs.io)

**PyPI :**
[![PyPI](https://img.shields.io/pypi/v/cmip-ref.svg)](https://pypi.org/project/cmip-ref/)
[![PyPI: Supported Python versions](https://img.shields.io/pypi/pyversions/cmip-ref.svg)](https://pypi.org/project/cmip-ref/)
[![PyPI install](https://github.com/CMIP-REF/cmip-ref/actions/workflows/install.yaml/badge.svg?branch=main)](https://github.com/CMIP-REF/cmip-ref/actions/workflows/install.yaml)

**Other info :**
[![Licence](https://img.shields.io/github/license/CMIP-REF/cmip-ref.svg)](https://github.com/CMIP-REF/cmip-ref/blob/main/LICENCE)
[![Last Commit](https://img.shields.io/github/last-commit/CMIP-REF/cmip-ref.svg)](https://github.com/CMIP-REF/cmip-ref/commits/main)
[![Contributors](https://img.shields.io/github/contributors/CMIP-REF/cmip-ref.svg)](https://github.com/CMIP-REF/cmip-ref/graphs/contributors)

## Getting started

### As a metrics provider

Metrics providers are the core of the REF.
They define the metrics that will be calculated and the data that will be used to calculate them,
by providing a consistent interface for the REF to interact with.


These metrics providers can be run as standalone applications or as part of the REF.
See

### As a modelling center

The REF is designed to enable Modelling Centers to quickly evaluate their data against a set of reference data.
The data under test here may not be published to ESGF yet,
but the REF can still be used to evaluate it.

TODO: Docs for that workflow

```bash
ref ingest {data_path} --solve
```

### As a devops engineer

The REF can also be deployed as a standalone set of services that don't require any user interaction.
This is useful for running the REF to automatically evaluate data as it is published to ESGF.

TODO: Docs for that workflow

Each service in the REF is designed to be run as a separate docker container.

<!--- --8<-- [end:description] -->

Full documentation can be found at:
[cmip-ref.readthedocs.io](https://cmip-ref.readthedocs.io/en/latest/).
We recommend reading the docs there because the internal documentation links
don't render correctly on GitHub's viewer.

## Installation

<!--- --8<-- [start:description] -->

CMIP Rapid Evaluation Framework can be installed with pip, mamba or conda:

The following commands don't work yet, but will be updated when we have a release.

```bash
pip install cmip-ref
mamba install -c conda-forge cmip-ref
conda install -c conda-forge cmip-ref
```

<!--- --8<-- [end:installation] -->

### For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [uv](https://docs.astral.sh/uv) for all our
dependency management. To get started, you will need to make sure that uv
is installed
([instructions here](https://docs.astral.sh/uv/getting-started/installation/)).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

If you wish to run the test suite,
some input data must be fetched from ESGF.
To do this, you will need to run `make fetch-data`.

The test suite can then be run using `make test`.
This will run the test suites for each package and finally the integration test suite.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the
[issue tracker](https://github.com/CMIP-REF/cmip-ref/issues).

For the rest of our developer docs, please see [](development-reference).

<!--- sec-end-installation-dev -->

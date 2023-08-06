
# jsfileupload

[![Build Status](https://travis-ci.org//jsfileupload.svg?branch=master)](https://travis-ci.org//jsfileupload)
[![codecov](https://codecov.io/gh//jsfileupload/branch/master/graph/badge.svg)](https://codecov.io/gh//jsfileupload)


FileUpload Widget using the Jupyter Notebook Server API.

## Installation

You can install using `pip`:

```bash
pip install jsfileupload
```
or from this GitLab directly
```bash
pip install git+https://gitlab.version.fz-juelich.de/jupyter4jsc/j4j_extras/jsfileupload.git

Or if you use jupyterlab:

```bash
pip install jsfileupload
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] jsfileupload
```

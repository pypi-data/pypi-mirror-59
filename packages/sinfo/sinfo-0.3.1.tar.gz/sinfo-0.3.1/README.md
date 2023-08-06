# sinfo

`sinfo` outputs version information for modules loaded in the current session,
Python, the OS, and the CPU. It is designed as a minimum measure to increase
reproducibility and provides similar information as `sessionInfo` in R. The
name is shortened to encourage regular usage through reduced typing =)

## Motivation

`sinfo` is particularly useful when conducting exploratory data analysis in
Jupyter notebooks. Listing the version numbers of all loaded modules after
importing them is a simple way to ensure a minimum level of reproducibility
while requiring little additional effort. This practice is useful both when
revisiting notebooks and when sharing them with colleagues. `sinfo` is meant to
complement more robust practices such as frozen virtual environments,
containers, and binder.

## Installation

`sinfo` can be installed via `pip install sinfo`. It does not depend on a package
manager to find version numbers since it fetches them from the module's version
string. Its only dependency is `stdlib_list`, which is used to distinguish
between standard library and third party modules.

## Usage

```python
import math

import natsort
import numpy
import pandas
from sinfo import sinfo


sinfo()
```


Output:

```

-----
natsort     5.3.3
numpy       1.17.3
pandas      0.25.1
sinfo       0.3.0
-----
Python 3.7.3 | packaged by conda-forge | (default, Dec  6 2019, 08:54:18) [GCC 7.3.0]
Linux-5.4.2-arch1-1-x86_64-with-arch
4 logical CPU cores
-----
Session information updated at 2019-12-14 16:14
```

The default behavior is to only output modules not in the standard library,
which is why the `math` module is omitted above (it can be included by
specifying `std_lib=True`). To include not only the explicitly imported
modules, but also any dependencies they import internally, specify `dependencies=True`.
The notebook output is concealed in `<details>` tags by default to not take up too much visual real estate.
When called from a notebook, `sinfo` writes the module dependencies
to a file called to `<notebook_name>-requirements.txt`, which is compatible with `pip install -r /path/to/requirements.txt`.
See the docstring for complete parameter info.

## Background

`sinfo` started as minor modifications of `py_session`, and as it grew it
became convenient to create a new package. `sinfo` was built with the help of
information provided in stackoverflow answers and existing similar packages,
including

- https://github.com/fbrundu/py_session
- https://github.com/jrjohansson/version_information
- https://stackoverflow.com/a/4858123/2166823
- https://stackoverflow.com/a/40690954/2166823
- https://stackoverflow.com/a/52187331/2166823

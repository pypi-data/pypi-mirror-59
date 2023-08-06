# simple_python_profiler

An early look at a _simple_ Python profiler, written in Python. Get started by typing `pip install simple_python_profiler`.

## Description
A profiler that times every function call and reports back the top 100 slowest functions.

_logs every function call means it's non-sampling, hence resource-intensive. If that's unsuitable, check out something like [py-spy](https://github.com/benfred/py-spy)._

Usage:
```python
# your-script.py

from simple_python_profiler import Profiler
if __name__ == '__main__':
    with Profiler():
        run_your_code()

```

This will decorate all your top-level functions in your modules. System (built-in) and pip-installed packages (those that go in `dist-packages`) are excluded.

Since the default behaviour is to not include nested functions, you can profile your nested functions too as follows:

```python
from simple_python_profiler import profile_recursive

# your-module.py

def top_level_function():

    @profile_recursive
    def inner_function():
        print('in inner fn')

```

This recursive feature relies on the [codetransformer](https://github.com/llllllllll/codetransformer) dependency. However, it has a few bugs in recent versions of Python. If you encounter runtime exceptions with `simple_python_profiler`, use the second, non-recursive decorator:

```python
from simple_python_profiler import profile

# your-module.py

def top_level_function():

    @profile
    def inner_function():
        print('in inner fn')

```

# Releasing on PyPI
- `pipenv shell`
- `flit build`
- `flit publish`

Enter password when prompted.

# TODO
- option to include system packages

Released under the MIT licence. See file named LICENCE for details.

# gexecute
A tool to generically execute any function with a unknown set of parameters!

Specify some set of parameters in a dictionary with the only restriction being that it must have all of the parameters with non-default values.

The function can either be a string representation or a function object.

If the function exists in another module; you must give either the module object or the package path and module name.

```
How to Install: pip install gexecute
```

<br>

```
PiPy https://pypi.org/project/gexecute/
```

<br>

<bold>How to use:</bold>
```
def test(a, b, c='test'):
    print(a, b, c)

> test(1, 2, 3)
1, 2, 3

> gexec({'a': 1, 'b': 2, 'c': 3}, test)
1, 2, 3

> gexec({'a': 1, 'b': 2}, test)
1, 2, test

# Function name can be an object or string
> gexec({'a': 1, 'b': 2}, 'test')
1, 2, test

> gexec({'a': 1, 'b': 2, 'd': 4}, test)
1, 2, test

# If test is in the directory C:\python\test_module.py
> gexec({'a': 1, 'b': 2, 'c': 3}, 'test', module='test_module', package_path='C:\python\')
1, 2, 3
```
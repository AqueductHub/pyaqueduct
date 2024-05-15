---
title: Using server plugins
summary: Covers how to use custom server functionality (plugins) with client library.
---

# What is a plugin in Aqueduct

Plugins are custom software features which may be added to an existing instance of the 
Aqueduct server by its administator. This may be, for example, data generation and processing, 
remote service usage, or image plotting. These features are available to Aqueduct users
in the web interface and through `pyaqueduct` client python library.

Each plugin is a collection of **functions**. One plugin may have one or more functions.
Functions of one plugin may perform different operations, but on the server side they share
settings and execution environment.

Plugin functions are expected to read data from exeperiments and record their results to experiments. Plugin execution logs are also persisted in the experiment, which plugin function was accessing.

# Plugins in `pyaqueduct` library

Python API allows to list and execute plugins from code. Classes of 
[`pyaqueduct.plugin`](api-reference.md#plugin) module represent plugins, their functions, 
and execution results.

## Which plugins are available

[`pyaqueduct.API.get_plugins`](api-reference.md#pyaqueduct.API.get_plugins) method is responsible
for listing plugins, available for execution. Here is an example of the code to access plugins, their
functions and function definitions:

```python
from pyaqueduct import API

api = API("http://localhost:8000", timeout=100)
plugins = api.get_plugins()  # list of plugins
for plugin in plugins:
    print(f"Plugin `{plugin.name}` by {plugin.authors}: {plugin.description}.")
    for function in plugin.functions:
        print(f"> Function {function.data.name}: {function.data.description}")
        for parameter in function.parameters:
            print(
                f"> > Parameter {parameter.displayName} ({parameter.name}, {parameter.dataType}):"
                f" {parameter.description}")
```

## Executing a plugin

As shown above, plugin functions accept named parameters. To run a plugin on a server,
the method [`PluginFunction.execute`](api-reference.md#pyaqueduct.plugin.PluginFunction.execute)
accepts a dictionary, where keys are parameter names, and values are arguments to pass.
Please note, that values may be of any simple type, to me passed to a server, they will be 
converted into strings. Data types allowed in plugins are:
- `str` and `texarea` — arbitrary strings.
- `experiment` — string with an experiment ID (EID).
- `file` — string with a file name inside and experiment.
- `select` — string, one of the listed options.
- `float`, `int` — numerical types.
- `bool` — `True` or `False`.

Here is the example of calling an example plugin:

```python
api = API("http://localhost:8000", timeout=100)
plugins = api.get_plugins()
# example plugin
plugin = [p for p in plugins if p.name == "Dummy plugin"][0]
function = plugin.functions[0]
result = function.execute({
    "var1": "string value",
    "var2": 1,
    "var3": .31415e+1,
    "var4": "20240531-1",  #experiment ID
    "var5": "text\nin\nmultiple\nstrings",
    "var6": True,
    "var7": "string1",  # one of the options
})
print(f"success: {result.returnCode == 0}")
print(f"output:\n{result.stdout}")
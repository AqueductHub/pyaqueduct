---
title: Using server extensions
summary: Covers how to use custom server actionality (extensions) with client library.
---

# What is an extension in Aqueduct

Extensions are custom software features which may be added to an existing instance of the 
Aqueduct server by its administator. This may be, for example, data generation and processing, 
remote service usage, or image plotting. These features are available to Aqueduct users
in the web interface and through `pyaqueduct` client python library.

Each extension is a collection of **actions**. One extension may have one or more actions.
Actions of one extension may perform different operations, but on the server side they share
settings and execution environment.

Extension actions are expected to read data from experiments and record their results to experiments.
Extension execution logs are also persisted in the experiment which extension action was accessing.

# Extensions in `pyaqueduct` library

Python API allows to list and execute extensions from code. Classes of 
[`pyaqueduct.extension`](api-reference.md#extensions) module represent extensions, their actions, 
and execution results.

## Which extensions are available

[`pyaqueduct.API.get_extensions`](api-reference.md#pyaqueduct.API.get_extensions) method is responsible
for listing extensions available for execution. Here is an example of the code to access extensions, their
actions and action definitions:

```python
from pyaqueduct import API

api = API("http://localhost:8000", timeout=100)
extensions = api.get_extensions()  # list of extensions
for extension in extensions:
    print(f"Extension `{extension.name}` by {extension.authors}: {extension.description}.")
    for action in extension.actions:
        print(f"> Action {action.name}: {action.description}")
        for parameter in action.parameters:
            print(
                f"> > Parameter {parameter.displayName} ({parameter.name}, {parameter.dataType}):"
                f" {parameter.description}")
```

## Executing an extension

As shown above, extension actions accept named parameters. Their definitions are given 
in `ExtensionAction.parameters` collection. Each definition includes name, type, display 
name, and may include description and default values.

To run an extension on a server, the method [`ExtensionAction.execute()`](api-reference.md#pyaqueduct.extension.ExtensionAction.execute)
accepts a dictionary, where keys are parameter names, and values are arguments to pass.
Please note, that values may be of any simple type, while being sent to a server, they are
converted into strings. Data types allowed in extensions are:
- `str` and `textarea` — arbitrary strings.
- `experiment` — string with an experiment ID (EID).
- `file` — string with a file name inside and experiment.
- `select` — string, one of the listed options.
- `float`, `int` — numerical types.
- `bool` — `True` or `False`.

Here is the example of calling an example extension. Logs of the execution 
(process return code, standard output and standard error streams) are saved to the experiment.

```python
api = API("http://localhost:8000", timeout=100)
exp = api.create_experiment(
            title="test experiment",
            description="testing extensions")

extensions = api.get_extensions()
# choose an example extension by name
extension = [p for p in extensions if p.name == "Dummy extension"][0]
action = extension.actions[0]

result = action.execute({
    "var1": "string value",
    "var2": 1,
    "var3": .31415e+1,
    "var4": exp.alias,
    "var5": "text\nin\nmultiple\nstrings",
    "var6": True,
    "var7": "string1",
})
print(f"success: {result.returnCode == 0}")

# download a log file into a current working directory
exp.download_file(file_name=result.logFile, destination_dir=".")
# print the log file content
with open("./" + result.logFile) as f:
    print(f.read())
```

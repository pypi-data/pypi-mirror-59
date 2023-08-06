# CommonBuild Dependency Manager

*A module to manage Java dependencies across multiple Python packages.*

## Introduction

When using multiple packages ([PyJapc], [PyTimber], etc) inside a single
script, they must share a single JVM instance. This means that the required
jars for *all* packages must be added to the class path of the JVM that is
started by the first instantiated package.

**cmmnbuild-dep-manager** provides a simple way to get a single list of jars
for all installed packages. As packages are added/removed it automatically
resolves and downloads the required jar files using the [CBNG web service]
(within the CERN network) or Gradle (in a public network).

[PyJapc]:           https://gitlab.cern.ch/scripting-tools/pyjapc
[PyTimber]:         https://github.com/rdemaria/pytimber
[CBNG web service]: https://wikis.cern.ch/display/DVTLS/CBNG+Web+service

## Usage

Packages should implement the variable `__cmmnbuild_deps__` in their
`__init__.py` containing a list of the required dependencies, for example:

```python
__cmmnbuild_deps__ = [
    'japc',
    'japc-value',
    'japc-ext-cmwrda',
    'japc-ext-cmwrda3',
    'japc-ext-dirservice',
    {'product': 'inca-client',   'version': 'PRO'},
    {'product': 'slf4j-log4j12', 'local':   'true'},
    {'product': 'slf4j-api',     'local':   'true'},
    {'product': 'log4j',         'local':   'true'}
]
```

Each item in the list can be either a string containing the product name,
or a dictionary with keys matching the CBNG `product.xml` file
([more info][DVTLS Configuration]).

[DVTLS Configuration]: https://wikis.cern.ch/display/DVTLS/Configuration

With the variable in place, packages can be registered with
**cmmnbuild-dep-manager** using the following steps:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> mgr.install('pyjapc')
```

The `install()` function registers the package and resolves the dependencies
automatically. It is recommended that this is done automatically during a
package's installation process, which can be achieved with a custom `setup.py`
`install()` function.  Examples can be seen in [PyJapc] and [PyTimber]. Note
that when distributing a package (via [PyPI], etc) it is important to make a
source distribution (`sdist`) instead of a binary distribution (`bdist_wheel`)
as the latter does not include the custom installation command.

[PyPI]: https://pypi.python.org/

Finally, from your code, you can start a JVM with the complete list of jars
using:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> jpype = mgr.start_jpype_jvm()
```

At this stage, JPype is ready to use.

## Advanced usage

### Re-downloading jars

The jars can be resolved and re-downloaded at any time by running the following
shell command:

```bash
$ python -m cmmnbuild_dep_manager resolve
```

### Jar inspection helper functions

Helper functions are provided to inspect the classes in the downloaded jars.

#### class_list()

Provides a listing of all classes contained within the jars:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> mgr.class_list()
['cern.accsoft.cals.extr.client.commandline.CommandLineException',
 'cern.accsoft.cals.extr.client.commandline.CommandLineServiceBuilder',
 'cern.accsoft.cals.extr.client.commandline.CommandMethod',
 'cern.accsoft.cals.extr.client.commandline.CommandOption',
 ...]
```

#### class_search()

Search for any class by name:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> mgr.class_search('ServiceBuilder')
['cern.accsoft.cals.extr.client.commandline.CommandLineServiceBuilder',
 'cern.accsoft.cals.extr.client.service.ServiceBuilder',
 'cern.cmw.rda3.client.service.ClientServiceBuilder',
 'cern.cmw.rda3.impl.client.service.ClientServiceBuilderImpl']
```

#### class_hints()

Provide a pasteable example of how to use a specific class from Python:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> mgr.class_hints('cern.accsoft.cals.extr.client.service.ServiceBuilder')
cern = jpype.JPackage('cern')
ServiceBuilder = cern.accsoft.cals.extr.client.service.ServiceBuilder

>>> jpype = mgr.start_jpype_jvm()
>>> cern = jpype.JPackage('cern')
>>> ServiceBuilder = cern.accsoft.cals.extr.client.service.ServiceBuilder
>>> ServiceBuilder
jpype._jclass.cern.accsoft.cals.extr.client.service.ServiceBuilder
```

### Command-line interface

**cmmnbuild-dep-manager** has a basic command-line interface that allows access
to any method of the class. It can be invoked with:

```bash
$ python -m cmmnbuild_dep_manager METHOD [ARG ...]
```

For example, to register the packages `pytimber` and `pyjapc` you could run:

```bash
$ python -m cmmnbuild_dep_manager register pytimber pyjapc
pytimber
pyjapc
```

Which is equivalent to the following Python code:

```python
>>> mgr = cmmnbuild_dep_manager.Manager()
>>> mgr.register('pytimber', 'pyjapc')
('pytimber', 'pyjapc')
```

You can also see from this example that the return value is automatically
split to one list item per line.

### Dealing with read-only Python installations

For a typical installation, **cmmnbuild-dep-manager** downloads jars into a
subdirectory of the global site-packages and this process happens when a
package is installed. However, in some situations, the global
site-packages is not writeable by the user (e.g. in a centrally managed
distribution, such as [SWAN]). In this case, jars can be downloaded to each
[user's local site-packages][PEP 370] instead.

To facilitate this, a package can automatically install itself by setting an
optional parameter of its `Manager()` instance. For example:

```python
class PyJapc:
    def __init__(self, ...):
        ...
        mgr = cmmnbuild_dep_manager.Manager('pyjapc')
        mgr.start_jpype_jvm()
        ...
```

Then the user executing:

```python
>>> import pyjapc
>>> japc = pyjapc.PyJapc()
```

will cause the jars to be downloaded if they aren't already existing on disk
or if the version of PyJapc has changed.

[SWAN]:    http://swan.web.cern.ch/
[PEP 370]: https://www.python.org/dev/peps/pep-0370/

## Usage outside of CERN
For deployments outside of the CERN network, packages should implement the variable
```__gradle_deps__``` in their `__init__.py` containing a list of the required dependencies.
In this case, **cmmnbuild-dep-manager** will use Gradle to query public Java product repositories:
Maven Central and JCenter.

Note that ```__cmmnbuild_deps__``` (see above) will be used within CERN and ```__gradle_deps__```
outside of CERN. Packages used in both scenarios must implement both variables, and ensure 
consistency within the two.

```python
__cmmnbuild_deps__ = [
    "accmodel-jmad-core",
    "accmodel-jmad-models-lhc",
    "accmodel-jmad-models-gsi",
    "accmodel-jmad-models-lhctransfer",
    "accsoft-steering-commons",
    "accmodel-jmad-gui",
    "slf4j-log4j12",
    "slf4j-api",
    "log4j"
]

__gradle_deps__ = [
    "jmad:jmad-core:+",
    "org.slf4j:slf4j-api:+",
    "org.slf4j:slf4j-log4j12:+",
    "log4j:log4j:1.2.17",
]
```

For ```__gradle_deps__```, the list should consist of strings in the Gradle syntax
`groupId:artifactId:version`, or a dictionary with keys `groupId`, `product` and
`version`.

## More information

For more information or to report problems, please contact
[T. Levens](mailto:tom.levens@cern.ch).

# Modules API as used by IOCBIO Kinetics

Data analysis and reading from different formats is supported via
modules. This allows to extend the functionality of the program via
defined APIs to cover specific experimental protocols.

Modules are written in Python and are loaded recursively from
`iocbio.kinetics.modules` and any other folder specified in
configuration of the program via `modules/folders` setting (string
with folders separated by `;`).

When modules are loaded, all `iocbio.kinetics` objects have to be
imported using absolute path (as in `from
iocbio.kinetics.handler.experiment_generic import
ExperimentGeneric`). All module-internal Python files, have to be
loaded using relative path (as in `from .experiment_spectro import
ABC`).

Modules can be of several types, as described below. Each Python file
can contain multiple APIs and cover several types as well. Its also
possible to have Python files that are just dependency of some module
file and, in that case, the type of that dependency file should be left
unspecified.

Module type is defined using global variable in that module -
`IocbioKineticsModule` as

```python
IocbioKineticsModule = ["args", "database_schema"]
```

where `IocbioKineticsModule` is a list with elements describing a
type.

Below, each type is described separately together with the function
API that is used in that module.


## Module type: analyzer

This module is used to provide analyzers for given data. For this
module, specify

```
IocbioKineticsModule = ["analyzer"]
```

and function

```python
def analyzer(database, data):
    ...
    return Analyzer, overall_plot, overall_stats
```

where the returned values of all analyzer modules will be combined
together to form the sets used to analyze the data. Any of the
returned tuple can be `None`. It is expected that if the data is not
analyzed by this module, return value will be `None, None, None`.

Out of returned values, `Analyzer` and `overall_plot` are
dictionaries, `overall_stats` is a list. See implementation for
details.


## Module type: args

This module is used to compose command line arguments of kinetics
program as well as its help text covering used protocols. For this
module, specify

```
IocbioKineticsModule = ["args"]
```

and function `args` with an argument that is of
`iocbio.io.arguments.Parser` type to add new arguments (if
needed). Return value should be either `None` or short description of
supported protocol types. Description should end with newline. Example
of implementation below:

```python
def args(parser):
    parser.add_argument(name='electro_condition', help='Electrophysiology experiment condition. For example: ttx, iso')
    return '''Electrophysiology:
------------------
ltcc - Voltage step prodocol to estimate LTCC current
kill - Fluorescence maximum from killing cardiomyocyte
srcontent_by_ncx - Caffeine induced calcium relase
srrecovery_by_ltcc - SR recovery after caffeine experiment
'''

```


## Module type: database_schema

This module is used to initialize database schema. For this module, specify

```
IocbioKineticsModule = ["database_schema"]
```

and function `database_schema(database)`. The function is expected to
initialize database tables, if needed. There return value, if any, is
not used.


## Module type: database_processor

This module is used to apply some operations to the database after
loading datasets during the initial import from files, as given in
command line arguments. An example implementation allows to link new
imported dataset with some lab-specific preparation ID.

For this module, specify

```
IocbioKineticsModule = ["database_processor"]
```

and function `database_process(database, data, args)`. It is possible
that data argument is `None` during a call with the processor function
expected to check for it if needed. Function is called after the data
was created on the basis of command line arguments.


## Module type: reader

This module is used to read data from file or database and create data
object. For this module, specify

```
IocbioKineticsModule = ["reader"]
```

and function `create_data`:

```python
create_data(database, experiment_id=None, args=None)
```

The function should return `None` if the dataset is not of the type
covered by this reader. Otherwise, `data` is expected as a return
value.

The function can be called either with command line arguments or with
`experiment_id` specified, but never both different from `None`. With
`experiment_id` specified, data should be loaded from database
according to that `experiment_id`.

For `args`, if specified, the function can assume that all global
options, such as `file_name` and `protocol` are available.

When loading the data, the first module that will return non-None
value and load the data will be considered as responsible for that
data type. In this case, none of the non-called reader modules will
not be called and the returned data will be used for analysis.



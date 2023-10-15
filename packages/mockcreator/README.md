# PySyft Mock Data Creator

This subpackage provides functionality for generating mock data using the Python `faker` package, as well as inferring the metadata/schema of an existing Pandas DataFrame.

## TODO
* refactor to use graph to generate data *field by field accross the tables*
  * required for proper multi-table support
  * the order of fields should be determined by the relations => graph
  * currently generated table by table
* more features for multi-table support
  * proper fuzzy and non-matching value generation (metadata support?)
  * ?
* support specifying relationships between features 
  * plaitpy has "lambda" support
* better inferring support
  * distributions, default inferring, etc.?
* how to integrate with pysyft?
* use mypy
* tests


## Demos
### Simple demo
* Notebook [simple_demo.ipynb](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/mockcreator/simple_demo.ipynb)
* Inferred metadata: [metadata/inferred.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/inferred.yaml)
  * age and height min and max values were inferred
  * is_student and favorite_color distributions (weights) were inferred
* Modified metadata after inferring: [metadata/final.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/final.yaml)
  * height uses gaussian distribution
  * id is unique
  * name uses faker's first_name method

### Multi-table demo
* Very naive implementation of a simple multi-table support
* Notebook [multi_table_demo.ipynb](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/mockcreator/multi_table_demo.ipynb)
* Inferred metadata: [metadata/multi_inferred.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/multi_inferred.yaml)
  * two tables, both have `ssn` field
* Modified metadata after inferring: [metadata/multi_final.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/multi_final.yaml)
  * in `conditions` table fuzzy match is specified for `ssn`
    ```
    ssn:
        relation: fuzzy_match
        ref: people.ssn
        weights:
          match: 0.7
          fuzzy: 0.1
          no_match: 0.2
    ```



## Features

* YAML metadata
* data generation based on the metadata via faker and random packages
* initial (naive) multi-table support
* currently, metadata inferring is supported for
  * faker: pyint, pyfloat, pybool, pystring
  * random: choices
* metadata can be overrided after inferring

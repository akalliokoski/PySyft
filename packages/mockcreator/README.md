# PySyft Mock Data Creator

This subpackage provides functionality for generating mock data using the Python `faker` package, as well as inferring the metadata/schema of an existing Pandas DataFrame.

## Demo
* Notebook [simple_demo.ipynb](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/mockcreator/simple_demo.ipynb)
* Inferred metadata: [metadata/inferred.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/inferred.yaml)
  * age and height min and max values were inferred
  * is_student and favorite_color distributions (weights) were inferred
* Modified metadata after inferring: [metadata/final.yaml](https://github.com/akalliokoski/PySyft/blob/mock-creator/packages/mockcreator/metadata/final.yaml)
  * height uses gaussian distribution
  * id is unique
  * name uses faker's first_name method


## Features

* YAML metadata
* data generation based on the metadata via faker and random packages
* currently, metadata inferring is supported for
  * faker: pyint, pyfloat, pybool, pystring
  * random: choices
* metadata can be overrided after inferring

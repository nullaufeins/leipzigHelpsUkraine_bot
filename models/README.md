#  Models #

- In this folder the configuration files for the models of data classes (as `*.yaml`-files) are stored.
- These are interpreted by `openapi` to generate the classes for the source code during the `build` phase of the programme.
- Once the models are generated, the app configurations are read at run time and interpreted as these models.
- Generating instead of manually encoding the classes is safer/more stable as it allows for validation.

## Folder structure ##

As per the 3rd point, the `yaml`-file/s for the models (schemata)
and the `yaml`-file/s for actual configuration values for the app
are to be kept separately.

All models are to be stored in [./models](../models/),
whereas configuration files are to be stored in [./setup](../setup/).

Note that the generated python files are not stored in the repository.
When deployed on a server, these are generated as part of the `build`-process.

## Developer notes ##

### Prerequisites ###

For the python source code, we currently use:

- Python: `v3.10.*`
- Modules:
  - `datamodel-code-generator==0.12.0`

(This is all taken care of during the `build` process.)

### Building the models ###

To build the models before run time, use the following command + options:
```bash
datamodel-codegen
    --input-file-type openapi
    --encoding "UTF-8"
    --disable-timestamp
    --use-schema-description
    --snake-case-field
    --strict-nullable
    --input <path/to/file.yml>
    --output <path/to/file.py>
```
(cf. https://pydantic-docs.helpmanual.io/datamodel_code_generator/).

Alternatively, call:
```
just build
```

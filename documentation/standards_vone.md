[⬆️](..)


# Thought Process


# General

This applies to all the other main headings as well.

## Context
- `anywhere`
    - Anywhere in the code, files, api or documentation.
- `name`
    - Variables, Files, Functions, Modules, APIs
- `special_name`
    - Constants, Classes
- `<thing>`
    - Whatever this example is referring to in the application.


## General Naming Conventions
- **snake_case** all `names`
- No **numbers** in `names` or `special_names`
- No **- dashes -** `anywhere`


# Files

## Context
- `config`
    - Used to configure parts of the application.

## Configs
- **auto generated** `config` files should be named *.config*.
- **user managed** `config` files should be named *<thing>.config*.
- All `config` files should use [**toml**](https://toml.io/en/) format.

## Settings


# Code

## Imports
- Imports should follow this format
```shell
# DEPENDENCIES
## Built-In
import standard_library
## Third-Party
import pip_installed_library
## Local
import app_files
```

## Modules
- Module sections should be seperated by two lines for major responsibilities, and single line for sub-responsibilities, using
comments to describe the purpose of the section or sub-section.
```python
# Category
def work() -> None:
    pass

## Sub-Category
def sub_work() -> None:
    pass

def sub_work_two() -> None:
    pass

## Sub-Category
def sub_work_three() -> None:
    pass


# Category
```

## Variables
- **PascalCase** all `Classes`
```python
class EnumClass:
    CONSTANT: int = 0
```
- **UPPERCASE** all `Constants`
```python
CONSTANT: int = 0
```


# API


# Documentation

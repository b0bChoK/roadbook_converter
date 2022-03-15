# FFM Roadbook Rallye converter to a format usable in a digital roadbook

## Install dependencies
This python project requier Python 3.10 and Poetry 1.1.13 (environment manager, good stuff).
See how to install both of them depending your OS :
https://www.python.org/downloads/
https://python-poetry.org/docs/

### Install Poppler
*pdf2image* needs to have *poppler*, see here https://pypi.org/project/pdf2image/ how to get *poppler* depending your OS.
For windows :
Unzip poppler in this directory and update the **POPPLER_PATH** in *convert_roadbook.py* if needed.
For linux :
Set the **POPPLER_PATH** to None in *convert_roadbook.py*.

## Setup environment
After installing poppler, initiate the environment, run : 
```
poetry install
```
Poetry will setup all needed dependencies.

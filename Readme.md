## Example to test python packaging and other build related tools

The project has been used to explore how to build package with modern tools.

This project demonstrates
* Create a Makefile-like python script only depending on stdlib
* Use of pre-commit framework
* Use of pyinstaller to build an exe file, `packaging-example.exe` 
* Example of defined a python package with pyproject.toml and setuptools
    * Focus on editable installs
    * Include package data in the package to be read wtih `importlib.resources`
* The package contains two project scripts `hello1` and `hello2` defined in pyproject.toml.
* If the package is installed with `pipx install .\packaging_example-0.0.3-py3-none-any.whl` you can run hello1.exe and hello2.exe


### Build wheel and test wheel content
* Setup venv with editable install (only dependant on stdlib)
    * `py -3.10 makefile.py venv`
* Activate the venv:
    * `.\venv\Scripts\Activate.ps1`
* Build wheel:
    * `py -3.10 makefile.py build`
* Build exe wtih pyinstaller:
    * `py -3.10 makefile.py build-exe`
* Inspect wheel content:
    * `7z l .\dist\packaging_example-0.0.1-py3-none-any.whl`


## Observations about editable installs and setuptools

With setuptools editable installs works with the src-folder layout.

Flat layout almost works with setuptools==63.4.3 if using an empty `setup.cfg`

Note to self, always use the src layout to avoid problems with flat layout


## Install packages directly from git
* Latest:
    *  pip install -U  git+https://github.com/per11235813/python-packaging-examples-setuptools.git
* Specific version (by tag)
    * pip install -U  git+https://github.com/per11235813/python-packaging-examples-setuptools.git@v0.0.2


## Run pre-commit hooks
* `pre-commit run --all-files`
* `pre-commit install`
* `pre-commit uninstall`


## Testing all notebooks
* powershell:
    * `(ls -recurse notebooks\*.ipynb).fullname | ForEach-Object { pytest --nbmake $_ }`
* bash (github actions)
    * `pytest --nbmake **/*ipynb`

## Example to test python packaging and other build related tools

The project has been used to explore how to build package with modern tools.

This project demonstrates
* Example of defined a python package with pyproject.toml and setuptools
    * Focus on editable installs
    * Include package data in the package to be read wtih `importlib.resources`
    * The package contains two project scripts `hello1` and `hello2` defined in pyproject.toml.
* Using a Makefile-like python script only depending on stdlib
* Use of pre-commit framework
* Use of pyinstaller to build an exe file, `packaging-example.exe` 
* If the package is installed with `pipx install .\packaging_example-0.0.3-py3-none-any.whl` you can run hello1.exe and hello2.exe
* Basic use of github action to run tests and build wheels
* pyinstaller does uses `--collect-data` and `--collect-binaries` to include data files and executables. So `--collect-data` also includes binary data
* pyinstaller does not consider include/exclude patterns in pyproject.toml. To ensure the pyinstaller includes exactly the data in the generated wheel, then a decidated venv should be created for the build

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

Flat layout (ie not src-folder) works in most cases but for editable installs it may case problems

My recommendation is to always use the src-folder layout to avoid problems with flat layout


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

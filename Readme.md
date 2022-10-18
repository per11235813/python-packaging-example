## Example to test python packaging

In particular the objective is to clarify how to get editable install working with setuptools and the VS Code tool set

* Build wheel and test wheel content
```
py -3.10 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip  install -U pip build
python -m build --wheel

# Inspect wheel content
7z l .\dist\packaging_example-0.0.1-py3-none-any.whl
```

* Editable install, this works for
    * src layout and flat layout with setuptools==63.4.3. Empty setup.cfg is required for 63.4.3
    * src layout with with setuptools==66.5
```
pip install -e .[dev]
```

* Editable install, this works for
    * flat layout with with setuptools==66.5
    * info here: https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#editable-install-modules-not-found
```
pip install -e .[dev] --config-settings editable_mode=compat
```

## Install packages directly from git
* Latest:
    *  pip install -U  git+https://github.com/per11235813/python-packaging-examples-setuptools.git
* Specific version (by tag)
    * pip install -U  git+https://github.com/per11235813/python-packaging-examples-setuptools.git@v0.0.2


## Run pre-commit hooks
`pre-commit run --all-files`

## Testing notebooks
* `(ls -recurse notebooks\*.ipynb).fullname | ForEach-Object { pytest --nbmake $_ }`
* `pytest --nbmake **/*ipynb`

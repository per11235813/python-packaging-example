import re
import shutil
import sys
from pathlib import Path

from makefileutils import cli_add, cli_exec, run


@cli_add("venv")
def venv():
    """Create or update venv"""
    py_exe = sys.executable

    if not Path("venv").exists():
        run(f"{py_exe} -m venv venv")
        # shutil.copy("pip.ini", "venv")

    run(rf".\venv\Scripts\activate.bat & python -m pip install -U pip")
    run(rf".\venv\Scripts\activate.bat & pip install -e .[dev]")


@cli_add("build")
def build():
    """Build wheel"""
    run(r".\venv\Scripts\activate.bat & python -m build --wheel")


@cli_add("build-exe")
def build_exe():
    """build the project"""

    cmd = r""".\venv\Scripts\activate.bat & pyinstaller.exe pyinstaller_main.py 
                    --name packaging-example
                    --noconfirm --console --clean --onefile
                    --collect-data "packaging_example.data" 
    """

    cmd = re.sub(" +", " ", cmd.replace("\n", " "))
    run(cmd)


@cli_add("clean")
def clean():
    """Cleanup build artifacts"""
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    Path("packaging-example.spec").unlink(missing_ok=True)

    for d in Path(".").glob("**/*.egg-info"):
        shutil.rmtree(d)


@cli_add("clean-all")
def clean_all():
    """Cleanup build artifacts and venv"""
    clean()
    shutil.rmtree("venv", ignore_errors=True)


@cli_add("nbclean-all")
def nbclean_all():
    """Remove output from all notebooks"""
    all_notebooks = (nb for nb in Path.cwd().glob("*.ipynb") if ".ipynb_checkpoints" not in nb.parts)
    for nb in all_notebooks:
        run(f'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "{nb}"')


if __name__ == "__main__":
    cli_exec()

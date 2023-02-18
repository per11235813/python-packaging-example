import re
import shutil
import sys
from pathlib import Path

from makefileutils import cli_add, cli_exec, run, get_pyproject_data, is_git_clean, is_git_tag_used

DIST_FOLDER = Path("dist")
DIST_TARGET = Path("dist-target")
DIST_TARGET.mkdir(exist_ok=True) # tmp folder for deployment

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
    run(r".\venv\Scripts\activate.bat & python -m build --wheel --no-isolation")


@cli_add("build-exe")
def build_exe():
    """Build exe file"""

    cmd = r""".\venv\Scripts\activate.bat & pyinstaller.exe
                pyinstaller_main.py 
                --name packaging-example
                --noconfirm --console --clean --onefile
                --collect-data "packaging_example.data" 
    """

    cmd = re.sub(r"\s+", " ", cmd)
    run(cmd)


@cli_add("test")
def pytest():
    """Run the tests"""
    run(r"pytest")


@cli_add("clean")
def clean():
    """Cleanup build artifacts"""
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    Path("packaging-example.spec").unlink(missing_ok=True)

    for d in Path(".").glob("**/*.egg-info"):
        shutil.rmtree(d)

    for d in Path(".").glob("**/__pycache__"):
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


@cli_add("dist")
def dist():
    """Tags current commit and deploy build artifacts"""

    name, version, git_tag = check_git()
    build()
    run(f'git tag -a {git_tag} -m "version {version} of {name}"')
    run(f"git push --follow-tags")

    for wheel in DIST_FOLDER.glob("*.whl"):
        print(f"Copy {wheel} to {DIST_TARGET}")
        shutil.copy(wheel, DIST_TARGET)


def check_git() -> tuple[str, str, str]:
    if not is_git_clean():
        print("Git index is dirty. Exiting ...", file=sys.stderr)
        sys.exit(1)

    version, name = get_pyproject_data()
    git_tag = f"v{version}"

    if is_git_tag_used(git_tag):
        print(f"Git tag: {git_tag} is already used. Update ersion in pyproject.toml. Exiting ...", file=sys.stderr)
        sys.exit(1)

    return name, version, git_tag


if __name__ == "__main__":
    cli_exec()

import datetime as dt
import re
import shutil
import sys
import tempfile
from itertools import chain
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen

venv_name = "venv"
activate = rf".\{venv_name}\Scripts\activate.bat & "
wheelhouse_folder = r"\\md-man.biz\project-cph\bwcph\wheelhouse_3_10"
pip_ini = Path(venv_name) / "pip.ini"
pip_ini_txt = f"[install]\nno-index = true\nfind-links = {wheelhouse_folder}"
py_exe = sys.executable


def venv():
    """Create or update venv"""

    if Path(venv_name).exists():
        print("venv exists, exiting")
        return

    run(f"{py_exe} -m venv {venv_name}")
    pip_ini.write_text(pip_ini_txt)
    run(f"{activate} python -m pip install -U pip")
    run(f"{activate} python -m pip install -e .[dev]")


def build():
    """Re-build wheel"""
    run(f"{activate} python -m build --wheel --no-isolation")


def build_exe():
    """Build exe file"""
    cmd = f"""
        {activate} pyinstaller.exe pyinstaller_main.py 
                --name packaging-example
                --collect-data "packaging_example.data" 
                --noconfirm --console --clean --onefile
    """
    cmd = re.sub(r"\s+", " ", cmd)
    run(cmd)


def pytest():
    """Run the tests"""
    run("pytest")


def clean_test():
    tmp_dir = Path(tempfile.gettempdir())
    now_str = dt.datetime.now().strftime("%Y%m%d_%H%M")
    checkout_folder = tmp_dir / f"{Path.cwd().name}-{now_str}"
    git_url = get_url_from_git_config()

    try:
        run(f"git clone {git_url} {checkout_folder.name}", cwd=tmp_dir)
        run(f"py -3.10 makefile.py venv", cwd=checkout_folder)
        run(f"py -3.10 makefile.py pytest", cwd=checkout_folder)
        status = "OK"
    except CalledProcessError:
        status = "NOK"

    run(f'git tag -a TEST_{status}_{now_str} -m "Test run {now_str} - {status}"', cwd=checkout_folder)
    run(f"git push --follow-tags", cwd=checkout_folder)

    rm(checkout_folder)


def clean():
    """Cleanup build artifacts"""
    src = Path("src")
    to_remove = chain(
        ("dist", "build", "packaging-example.spec"),
        src.glob("**/__pycache__"),
        src.glob("**/*.egg-info"),
    )

    for d in to_remove:
        rm(d)


def clean_all():
    """Cleanup build artifacts and venv"""
    clean()
    rm("venv")


def nbclean_all():
    """Remove output from all notebooks"""
    all_notebooks = (nb for nb in Path.cwd().glob("*.ipynb") if ".ipynb_checkpoints" not in nb.parts)
    for nb in all_notebooks:
        run(f'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "{nb}"')


actions = {
    "venv": venv,
    "build": build,
    "pytest": pytest,
    "clean-test": clean_test,
    "clean": clean,
    "nbclean-all": nbclean_all,
    "clean-all": clean_all,
}

####################################
#####  Boilerplate starts here
####################################


def get_url_from_git_config(conf: Path = Path.cwd() / ".git" / "config") -> str:
    """Get the url from the git config file"""
    lines = conf.read_text().splitlines()
    urls = [line.split(" = ")[1].strip() for line in lines if line.startswith("\turl = ")]
    assert len(urls) == 1, "More than one url found in git config"

    return urls[0]


def run(cmd: str, echo_cmd=True, echo_stdout=True, cwd: Path = None) -> str:
    """Run shell command with option to print stdout incrementally"""
    echo_cmd and print(f"##\n## Running: {cmd}", end="")
    cwd and print(f"\n## cwd: {cwd}")
    echo_cmd and print(f"\n")

    res = []
    proc = Popen(cmd, stdout=PIPE, stderr=sys.stderr, shell=True, encoding=sys.getfilesystemencoding(), cwd=cwd)
    while proc.poll() is None:
        line = proc.stdout.readline()
        echo_stdout and print(line, end="")
        res.append(line)

    if proc.returncode != 0:
        raise CalledProcessError(proc.returncode, cmd)

    return "".join(res)


def rm(path: Path | str, echo_cmd: bool = True):
    """Remove file or folder"""
    if isinstance(path, str):
        path = Path(path)
    echo_cmd and print(f"## Removing: {path}")
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


if __name__ == "__main__":
    cmd = sys.argv[0]
    sub_cmd = sys.argv[1] if len(sys.argv) == 2 else None

    if sub_cmd in actions and sub_cmd:
        actions[sub_cmd]()
    else:
        print(f"Options for '{sys.executable} {cmd}':")
        for arg, func in actions.items():
            doc_str = func.__doc__.split("\n")[0] if func.__doc__ else ""
            print(f"   {arg: <18}{doc_str}")

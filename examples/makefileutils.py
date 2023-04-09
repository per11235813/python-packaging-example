from pathlib import Path
import sys
from subprocess import PIPE, CalledProcessError, Popen
from collections import namedtuple

_cli_dict = {}


def cli_add(cli_name: str):
    """Add function as a command line option"""

    def middle(func):
        _cli_dict[cli_name] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__doc__ = func.__doc__
        return wrapper

    return middle


def cli_exec():
    """Run function by command line argument"""
    cmd = sys.argv[0]
    if len(sys.argv) != 2 or sys.argv[1] not in _cli_dict:
        print(f"Options for '{sys.executable} {cmd}':")
        for arg, func in _cli_dict.items():
            doc_str = func.__doc__.split("\n")[0] if func.__doc__ else ""
            print(f"   {arg: <18}{doc_str}")
        sys.exit(1)

    _cli_dict[sys.argv[1]]()


def run(cmd: str, echo_cmd=True, echo_stdout=True, cwd: Path=None) -> str:
    """Run shell command with option to print stdout incrementally"""
    echo_cmd and print(f"##\n## Running: {cmd}\n")
    res = []
    proc = Popen(cmd, stdout=PIPE, stderr=sys.stderr, shell=True, encoding=sys.getfilesystemencoding(), cwd=cwd)
    while proc.poll() is None:
        line = proc.stdout.readline()
        echo_stdout and print(line, end="")
        res.append(line)

    if proc.returncode != 0:
        raise CalledProcessError(proc.returncode, cmd)

    return "".join(res)


def is_git_clean() -> bool:
    run("git fetch")
    git_status = run("git status", echo_stdout=False)

    index_clean = "nothing to commit, working tree clean" in git_status
    branch_up_to_date = "Your branch is up to date with 'origin/" in git_status

    return branch_up_to_date and index_clean


def is_git_tag_used(tag: str) -> bool:
    git_tag_l = run("git tag -l")

    return tag in git_tag_l


pyproject_toml_data = namedtuple("pyproject_toml_data", (project_version, project_name))
def get_pyproject_data(pyproject_toml: Path = Path("pyproject.toml")) -> pyproject_toml_data:
    import tomli

    pyproject_toml = tomli.loads(pyproject_toml.read_text(encoding="utf8"))
    version = pyproject_toml["project"]["version"]
    package_name = pyproject_toml["project"]["name"]

    return pyproject_toml_data(version, package_name)


def check_git():
    """Check if index and cache is clean"""
    msg = "Index is clean" if is_git_clean(echo_stdout=False) else "Index is dirty"

    print(f"{Path.cwd.absolute()}: {msg}")

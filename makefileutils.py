import sys
from subprocess import PIPE, CalledProcessError, Popen

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


def run(cmd, echo_cmd=True, echo_stdout=True, cwd=None) -> str:
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

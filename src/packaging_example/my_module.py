from importlib.abc import Traversable
from importlib.resources import files
from pathlib import Path
from uuid import uuid4

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def hello():
    print("hello, world!")

    print("\nData collected from the package with importlib.resources:")
    csv_path: Traversable = files("packaging_example.data") / "data.csv"
    csv_text = csv_path.read_text()
    print(csv_text)

def export_pic():
    png_path: Traversable = files("packaging_example.data") / "pic.png"
    png_data = png_path.read_bytes()
    png_out = Path(f"pic_{uuid4()}.png")
    png_out.write_bytes(png_data)

    print(f"Exported picture to {png_out.absolute()}")
    

def hello2():
    print(f"hello, world! {fib(14)=}")

def hello3():
    print(f"hello, world! {fib(16)=}")



if __name__ == "__main__":
    hello2()
    hello3()
    export_pic()
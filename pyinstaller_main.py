from importlib.resources import files
from pathlib import Path

from packaging_example import my_module

if __name__ == "__main__":
    my_module.hello2()

    print("\nData collected from the package with importlib.resources:")
    csv_path: Path = files("packaging_example.data") / "data.csv"
    csv_text = csv_path.read_text()
    print(csv_text)

from importlib.resources import files
import csv


def test_csv_data():
    package = "packaging_example.data"
    p = files(package) / "data.csv"

    with open(p, encoding="utf8") as f:
        d = csv.reader(f)
        header = next(d)
        data = [[int(entry) for entry in r] for r in d]

    total = sum(entry for row in data for entry in row)

    assert total == sum(range(1, 7))


if __name__ == "__main__":
    package = "packaging_example.data"
    p = files(package) / "data.csv"

    with open(p, encoding="utf8") as f:
        d = csv.reader(f)
        header = next(d)
        data = [r for r in d]

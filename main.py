from pathlib import Path
from result import GResult


def main():
    data_dir = Path("./data")
    for f in data_dir.glob("*.tsv"):
        print(GResult.from_file(f))


if __name__ == "__main__":
    main()

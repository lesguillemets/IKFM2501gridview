from pathlib import Path
from result import GResultDF
import argparse

AP = argparse.ArgumentParser(description="loads")
AP.add_argument('--dir', type=Path, help="Path to load data from")


def main():
    args = AP.parse_args()
    data_dir = args.dir or Path("./data")
    for f in data_dir.glob("*.tsv"):
        print(GResultDF.from_file(f))


if __name__ == "__main__":
    main()

from pathlib import Path
from result import GResultDF
import plot_by_emotion
import argparse

AP = argparse.ArgumentParser(description="loads")
AP.add_argument('--dir', type=Path, help="Path to load data from")


def main():
    args = AP.parse_args()
    data_dir = args.dir or Path("./data")
    data_all = [GResultDF.from_file(f) for f in data_dir.glob("*.tsv")]
    plot_by_emotion.do_plot(data_all)


if __name__ == "__main__":
    main()

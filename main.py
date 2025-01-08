from pathlib import Path
from result import GResultDF, Emotion
import filters as fls

import plot_by_emotion
import argparse

AP = argparse.ArgumentParser(description="loads")
AP.add_argument('--dir', type=Path, help="Path to load data from")


def main():
    args = AP.parse_args()
    data_dir = args.dir or Path("./data")
    data_all = [GResultDF.from_file(f) for f in data_dir.glob("*.tsv")]
    funnel = fls.Funnel.new().and_then(fls.ref_is_self).and_then(fls.emo_is(Emotion.Hap))
    print(funnel.pour(data_all[0].df))
    print(data_all[0].df)
    # plot_by_emotion.do_plot(data_all)


if __name__ == "__main__":
    main()

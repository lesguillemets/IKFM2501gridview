from pathlib import Path
from result import GResultDF, Emotion
import filters as fls

import plot_by_emotion
import argparse

AP = argparse.ArgumentParser(description="loads")
AP.add_argument('--dir', type=Path, help="Path to load data from")
AP.add_argument('--filter-ref', choices=["Self", "Other", "All"], help="filter by Ref=?")
AP.add_argument('--filter-emo',
                nargs='*', choices=["Ang", "Exc", "Hap", "Rel", "Sad"],
                help="Filter by which emotion?"
                )


def main():
    args = AP.parse_args()
    data_dir = args.dir or Path("./data")
    data_all = [GResultDF.from_file(f) for f in data_dir.glob("*.tsv")]
    funnel = fls.Funnel.new()
    funnel = handle_filter_ref(funnel, args.filter_ref)
    funnel = handle_filter_emo(funnel, args.filter_emo)

    print(funnel.pour(data_all[0].df))
    print(data_all[0].df)
    # plot_by_emotion.do_plot(data_all)


def handle_filter_ref(f: fls.Funnel, arg: str | None) -> fls.Funnel:
    match arg:
        case None | "All":
            return f
        case "Self":
            return f.and_then(fls.ref_is_self)
        case "Other":
            return f.and_then(fls.ref_is_other)

def handle_filter_emo(f:fls.Funnel, arg: list[str] | None) -> fls.Funnel:
    for em in arg or []:
        f = f.and_then(fls.emo_is(Emotion[em]))
    return f

if __name__ == "__main__":
    main()

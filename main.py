import pandas as pd
from pandas import DataFrame
from pathlib import Path

from plotly import plot
from result import GResultDF, Emotion
import filters as fls

import plot_by_emotion
import argparse

AP = argparse.ArgumentParser(description="loads")
AP.add_argument('command', choices=["print", "plot_by_emotion"])
AP.add_argument('--dir', type=Path, help="Path to load data from")
AP.add_argument('--filter-ref', choices=["Self", "Other", "All"], help="filter by Ref=?")
AP.add_argument('--filter-group', choices=["H", "A"], help="filter by group=?")
AP.add_argument('--filter-emo',
                nargs='*', choices=["Ang", "Exc", "Hap", "Rel", "Sad"],
                help="Filter by which emotion?"
                )

def print_df(df: DataFrame):
    with pd.option_context('display.max_rows', None):
        print(df)

COMMANDS = {
    'print': print_df,
    'plot_by_emotion': plot_by_emotion.do_plot,
}

def main():
    args = AP.parse_args()
    data_dir = args.dir or Path("./data")
    data_all = [GResultDF.from_file(f) for f in data_dir.glob("*.tsv")]
    df = pd.concat(map(lambda d: d.df, data_all))
    funnel = fls.Funnel.new()
    funnel = handle_filter_ref(funnel, args.filter_ref)
    funnel = handle_filter_group(funnel, args.filter_group)
    funnel = handle_filter_emo(funnel, args.filter_emo)
    COMMANDS[args.command](funnel.pour(df))


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

def handle_filter_group(f: fls.Funnel, arg:str | None) -> fls.Funnel:
    match arg:
        case None:
            return f
        case "H":
            return f.and_then(fls.group_is_h)
        case "A":
            return f.and_then(fls.group_is_a)


if __name__ == "__main__":
    main()

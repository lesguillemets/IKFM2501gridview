from result import GResultDF, Emotion, Cond2_Ref
import pandas as pd
import numpy as np
from pandas import DataFrame
from collections import defaultdict

GRID_SIZE = 11

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def prepare_counter() -> np.ndarray:
    # 誰が何回か，を覚えておく
    ar = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            ar[x,y] = defaultdict(int)
    return ar


def count_trials(df:DataFrame) -> dict[Emotion,DataFrame]:
    """
    結果の DataFrame を読んで， Emotion ごとに x y {id: count} を返す
    """
    counters = { Emotion(i): prepare_counter() for i in range(9) }
    for (_, trial) in df.iterrows():
        emo: Emotion = trial['emotion']
        # この表情で，(x,y) における投票をだれが何回やったか
        x = int(trial['x'])+GRID_SIZE//2
        y = int(trial['y'])+GRID_SIZE//2
        counters[emo][x,y][trial['id']] += 1
    result = {}
    for (emo, counter) in counters.items():
        result[emo] = pd.DataFrame(
            [
                (x-GRID_SIZE//2,y-GRID_SIZE//2, counter[x,y])
                for x in range(11) for y in range(11)
            ],
            columns=['x','y', 'counts_by_id']
        )
    return result

def counts_by_id_to_str(d):
    return ', '.join( (f"{p}: {c}" for (p,c) in d.items()) )

def do_plot(df:DataFrame) -> None:
    counted_by_emotions = count_trials(df)
    for c in counted_by_emotions.values():
        c['total_count'] = c['counts_by_id'].apply(lambda d: sum(d.values()))

    zmax = max( (c['total_count'].max() for c in counted_by_emotions.values()) )
    fig = make_subplots(rows=2, cols=3, subplot_titles= [Emotion(i).name for i in range(5) ])
    for i in range(5):
        col = 1+i % 3
        row = 1+i // 3
        emo: Emotion = Emotion(i)
        this_count = counted_by_emotions[emo]
        customdata = this_count['counts_by_id'].apply(counts_by_id_to_str)
        heatmap = go.Heatmap(
                x  = this_count['x'],
                y  = this_count['y'],
                z  = this_count['total_count'],
                zmin = 0,
                zmax = zmax,
                customdata=customdata,
                hovertemplate=(
                               'X: %{x},' +
                               'Y: %{y}<br>' +
                               'Count: %{z}<br>' +
                               'Names: %{customdata}'
                               ),
                )
        fig.append_trace( heatmap, row=row, col=col,)
    fig.show()

def do_simple_plot(df: DataFrame):
    fig = make_subplots(rows=2, cols=3, subplot_titles= [Emotion(i).name for i in range(5) ])
    # df = pd.concat(map(lambda d: d.df, data))
    # (ID とかは column あるからどっちでもいいやろの気持ち)
    for i in range(5):
        col = 1+i % 3
        row = 1+i // 3
        emo: Emotion = Emotion(i)
        # https://stackoverflow.com/a/72588847/3026489
        dh = px.density_heatmap(
                # df[(df['emotion'] == emo) & (df['condition2'] == Cond2_Ref.Otherr],
                df[df['emotion'] == emo],
                x = 'x',
                y = 'y',
                text_auto=True,
                nbinsx = 11,
                nbinsy = 11,
                title = emo.name
                )
        for trace in range(len(dh["data"])):
            fig.append_trace(
                dh["data"][trace],
                row=row, col=col,
            )
    fig.show()



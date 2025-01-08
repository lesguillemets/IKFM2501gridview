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
    return np.full((GRID_SIZE,GRID_SIZE), defaultdict(int))

def count_trials(df:DataFrame) -> dict[Emotion,DataFrame]:
    """
    結果の DataFrame を読んで， Emotion ごとに x y {id: count} を返す
    """
    counters = { Emotion(i): prepare_counter() for i in range(9) }
    for (_, trial) in df.iterrows():
        emo: Emotion = trial['emotion']
        # この表情で，(x,y) における投票をだれが何回やったか
        counters[emo][int(trial['x'])+GRID_SIZE//2,int(trial['y'])+GRID_SIZE//2][trial['id']] += 1
    result = {}
    for (emo, counter) in counters.items():
        result[emo] = pd.DataFrame(
            [
                (x-GRID_SIZE//2,y-GRID_SIZE//2, counter[x,y])
                for x in range(11) for y in range(11)
            ]
        )
    return result

def do_plot(df:DataFrame) -> None:
    counted = count_trials(df)
    print(counted)

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



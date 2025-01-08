from result import GResultDF, Emotion, Cond2_Ref
import pandas as pd
import numpy as np
from pandas import DataFrame


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def prepare_counter() -> np.ndarray:
    # 誰が何回か，を覚えておく
    return np.full((11,11), dict())

def do_plot(df:DataFrame):
    counters = { Emotion(i): prepare_counter() for i in range(5) }
    pass

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



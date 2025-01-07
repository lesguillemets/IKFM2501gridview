from result import GResultDF, Emotion
import pandas as pd
from pandas import DataFrame


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def do_plot(data: list[DataFrame]):
    fig = make_subplots(rows=2, cols=3)
    df = pd.concat(map(lambda d: d.df, data))
    for i in range(5):
        col = 1+i % 3
        row = 1+i // 3
        emo = Emotion(i)
        # https://stackoverflow.com/a/72588847/3026489
        dh = px.density_heatmap(
                df[df['emotion'] == emo],
                x = 'x',
                y = 'y'
                )
        for trace in range(len(dh["data"])):
            fig.append_trace(
                dh["data"][trace],
                row=row, col=col
            )
    fig.show()



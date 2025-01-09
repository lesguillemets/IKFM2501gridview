from result import GResultDF, Emotion, Cond2_Ref
from pandas import DataFrame
from plot_helpers import count_trials_with_total, GRID_SIZE


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px



def counts_by_id_to_str(d):
    return ', '.join( (f"{p}: {c}" for (p,c) in d.items()) )

def do_plot(df:DataFrame) -> None:
    counted_by_emotions = count_trials_with_total(df)
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



from collections import defaultdict
import numpy as np
from pandas import DataFrame
import pandas as pd

from result import Emotion


GRID_SIZE = 11

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

def count_trials_with_total(df:DataFrame) -> dict[Emotion,DataFrame]:
    """
    count_trials に，全員のそのグリッドへの評定数を total_count として追加する
    """
    counted_by_emotions = count_trials(df)
    for c in counted_by_emotions.values():
        c['total_count'] = c['counts_by_id'].apply(lambda d: sum(d.values()))
    return counted_by_emotions

def prepare_counter() -> np.ndarray:
    # 誰が何回か，を覚えておく
    ar = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            ar[x,y] = defaultdict(int)
    return ar


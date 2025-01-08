from collections.abc import Callable
from typing import Optional
from pandas import DataFrame, Series

from result import Cond2_Ref, Emotion


type DataFilter = Callable[DataFrame, bool]

class Funnel:
    def __init__(self, f: Optional[DataFilter]=None):
        if f is None:
            fs = []
        else:
            fs = [f]
        self.filters: list[DataFilter] = fs

    @staticmethod
    def new(f:Optional[DataFilter]=None):
        return Funnel(f)

    def and_then(self, f:DataFilter):
        self.filters.append(f)
        print(self.filters)
        return self

    def pour(self, df: DataFrame):
        # FIXME: 多相すぎて返り値の annotation が面倒っぽい
        if self.filters == []:
            return df[:]
        result = df
        for f in self.filters:
            # 多分これでいい…??
            result = result[f(result)]
        return result


def ref_is_self(df: DataFrame) -> bool:
    return df['condition2'] == Cond2_Ref.Self

def ref_is_other(df: DataFrame) -> bool:
    return df['condition2'] == Cond2_Ref.Other

def emo_is(e: Emotion) -> DataFilter:
    return (lambda df: df['emotion'] == e)

def id_is(the_id:str) -> DataFilter:
    return (lambda df: df['id'] == the_id)

def group_is_h(df: DataFrame) -> bool:
    return df['id'].str.contains("CH")

def group_is_a(df: DataFrame) -> bool:
    return df['id'].str.contains("CA")

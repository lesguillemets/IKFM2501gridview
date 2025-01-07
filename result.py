"""
結果を表すクラスと，その parser
"""

from __future__ import annotations

from enum import IntEnum, Enum
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from pathlib import Path

HEADER_FORMAT = "index	condition1	condition2	layout	emotion	procedure	x	y	gender\n"


class Cond1_FB(Enum):
    """
    condition1: 自分の顔表示（0 = 映像なし・1 = 自分顔(自分の顔に自分の顔をスワップする)・2 = 他人顔）
    """

    NoFB = 0
    Self = 1
    Other = 2


class Cond2_Ref(Enum):
    """
    condition2: 参考顔表示（0 = 自分顔・1 = 他人顔(他人顔でも他人の顔をそのままスワップする)
    """

    Self = 0
    Other = 1


type Index = int
type Layout = bool
type Gender = int
type ID = str


class Emotion(Enum):
    Ang = 0
    Exc = 1
    Hap = 2
    Rel = 3
    Sad = 4
    TestA = 5
    TestB = 6
    TestC = 7
    TestD = 8

    def is_test(self) -> bool:
        return self.value > 4

    @staticmethod
    def from_str(s: str) -> Emotion:
        return Emotion(int(s))


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    @property
    def p(self) -> tuple[int,int]:
        return (self.x, self.y)


class Procedure(IntEnum):
    Test = 0
    Main = 1

    def is_test(self) -> bool:
        return self == Procedure.Test

class GResultDF:
    """
    被験者ID, optional に日付，後は結果を pd.DataFrame の形でもつ
    """

    def __init__(self, name: ID, df: pd.DataFrame , t: datetime | None = None) -> GResultDF:
        self.name: ID = name  # 被験者ID
        self.df:  pd.DataFrame = df  # 結果
        self.t: datetime | None = t  # 実施の日・時刻


    def __repr__(self) -> str:
        return f"{self.name} at {self.t} \n{self.df}"

    @staticmethod
    def from_file(p: Path) -> GResultDF:
        """
        所定の形式の tsv を読み込む．
        """
        assert p.is_file() and p.suffix == ".tsv"
        (the_id, the_date) = fname_parser(p)
        dat = pd.read_csv(p, sep='\t')
        return GResultDF.from_raw_dataframe(the_id, dat, the_date)

    @staticmethod
    def from_raw_dataframe(name:ID, df:DataFrame, t:datetime | None = None) -> GResultDF:
        """
        もとのデータに前処理をちょっと挟むのだ．
        """
        df["p"] = df.apply(lambda r: Point(int(r.x), int(r.y)), axis=1)
        df["condition1"] = df['condition1'].map(Cond1_FB)
        df["condition2"] = df['condition2'].map(Cond2_Ref)
        df["emotion"]  = df['emotion'].map(Emotion)
        df["gender"]  = df['gender'].map(int)
        df["procedure"]  = df['procedure'].map(int)
        df["layout"]  = df['layout'].map(lambda n: int(n) != 0)
        df["id"] = name
        df["time"] = t
        return GResultDF(name, df, t)



def fname_parser(p: Path) -> tuple[ID, datetime]:
    """
    ID と日付はファイル名に含まれているので，それを取り出す．
    mm-dd-hh-mm-ss-ID.tsv
    """
    parts = p.stem.split("-")
    if len(parts) < 6:
        # パーツが足りないので多分違います．
        raise ValueError(f"The filename doens't conform: {p.name}")
    # FIXME:
    # 現状年が含まれてない．11月-12月は2024年，それ以外は2025年としている．
    # フォーマットの変更依頼したいですね．冒頭に入れてもらえたら↓の5を6にしたらよさそう
    if parts[0] in ("11", "12"):
        year = 2024
    else:
        year = 2025
    rest_of_date = list(map(int, parts[:5]))
    return ("-".join(parts[5:]), datetime(year, *rest_of_date))

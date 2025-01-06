"""
結果を表すクラスと，その parser
"""

from __future__ import annotations

from enum import IntEnum
from datetime import datetime

from pathlib import Path


class Cond1_FB(IntEnum):
    """
    condition1: 自分の顔表示（0 = 映像なし・1 = 自分顔(自分の顔に自分の顔をスワップする)・2 = 他人顔）
    """

    NoFB = 0
    Self = 1
    Other = 2


class Cond2_Ref(IntEnum):
    """
    condition2: 参考顔表示（0 = 自分顔・1 = 他人顔(他人顔でも他人の顔をそのままスワップする)
    """

    Self = 0
    Other = 1


type Index = int
type Layout = bool
type Gender = int
type ID = str


class Emotion(IntEnum):
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

    @property
    def p(self):
        return (self.x, self.y)


class Procedure(IntEnum):
    Test = 0
    Main = 1

    def is_test(self) -> bool:
        return self == Procedure.Test


class SingleAnswer:
    """
    結果のtsv の一行にあたるやつ
    """

    def __init__(
        self,
        cond1: Cond1_FB,
        cond2: Cond2_Ref,
        layout: Layout,
        emo: Emotion,
        proc: Procedure,
        p: Point,
        gender: Gender,
    ):
        self.cond1: Cond1_FB = cond1
        self.cond2: Cond2_Ref = cond2
        self.layout: Layout = layout
        self.emotion: Emotion = emo
        self.proc: Procedure = proc
        self.loc: Point = p
        self.gender: Gender = gender

    @staticmethod
    def from_line(s: str) -> SingleAnswer:
        """
        tsv の一行を読み込む
        """
        data = list(map(int, s.split("\t")))
        return SingleAnswer(
            Cond1_FB(data[0]),
            Cond2_Ref(data[1]),
            bool(data[2]),
            Emotion(data[3]),
            Procedure(data[4]),
            Point(data[5], data[6]),
            data[7],
        )


class GResult:
    """
    被験者ID, optional に日付，後は結果のリスト．
    """

    def __init__(self, name: ID, dat: list[SingleAnswer], t: datetime | None = None):
        self.name: ID = name  # 被験者ID
        self.dat: list[SingleAnswer] = dat  # 結果のリスト
        self.t: datetime = t  # 実施の日・時刻

    @staticmethod
    def from_file(p: Path) -> GResult:
        """
        所定の形式の tsv を読み込む．
        """
        assert p.is_file() and p.suffix == ".tsv"
        (the_id, the_date) = fname_parser(p)
        with p.open("r") as f:
            results = map(SingleAnswer.from_line, f.read().splitlines())
        return GResult(the_id, list(results), the_date)


def fname_parser(p: Path) -> tuple[ID, date] | None:
    """
    ID と日付はファイル名に含まれているので，それを取り出す．
    mm-dd-hh-mm-ss-ID.tsv
    """
    parts = p.stem.split("-")
    if len(parts) < 6:
        # パーツが足りないので多分違います．ValueError でもいいのかも．
        return None
    # FIXME:
    # 現状年が含まれてない．11月-12月は2024年，それ以外は2025年としている．
    # フォーマットの変更依頼したいですね．冒頭に入れてもらえたら↓の5を6にしたらよさそう
    if parts[0] in ("11", "12"):
        year = 2024
    else:
        year = 2025
    rest_of_date = list(map(int, parts[:5]))
    return ("-".join(parts[5:]), date(year, *rest_of_date))

"""
結果を表すクラスと，その parser
"""

from __future__ import annotations

from enum import IntEnum
from datetime import date


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


class GResult:
    """
    被験者ID, optional に日付，後は結果のリスト．
    """

    def __init__(self, name: str, dat: list[SingleAnswer], date: date | None = None):
        self.name = name
        self.dat = dat
        self.date = date

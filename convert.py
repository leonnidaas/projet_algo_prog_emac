#!/usr/bin/env python3
import re
from typing import Tuple

Couple = Tuple[int, int]
Color = Tuple[int, int, int]


def str_to_definition(argument: str) -> Couple:
    """Reçoit un argument de la forme "100x300" et retourne un tuple de la
    forme (100, 300).  Les 2 valeurs entières doivent être strictement
    positives.

    Retourne None Si l'argument n'est pas de la bonne forme."""
    match = re.fullmatch(r"(\d+)x(\d+)", argument)
    if match:
        res = tuple(int(v) for v in match.group(1, 2))
        if res[0] < 1 or res[1] < 1:
            res = None
    else:
        res = None
    return res


def str_to_positive_int(argument: str) -> int:
    """Reçoit un argument sous la forme d'une suite de chiffres et retourne
    l'entier correspondant.

    Retourne None si l'argument n'est pas de la bonne forme."""
    match = re.fullmatch(r"(\d+)", argument)
    if match:
        return int(match.group(1))
    return None


def str_to_float(argument: str) -> float:
    """Reçoit une chaîne représentant un nombre flottant et retourne le
    nombre flottant correspondant.

    Retourne None si l'argument n'est pas de la bonne forme.

    """
    match = re.fullmatch(
        r"([+-]?(\d+([.]\d*)?(e[+-]?\d+)?|[.]\d+(e[+-]?\d+)?))", argument
    )
    if match:
        return float(match.group(1))
    return None


def str_to_color(argument: str) -> Color:
    """Reçoit une couleur sous la forme "123,0,255"
    et retourne un tuple de la forme (123, 0, 255)
    Les 3 valeurs entières doivent être dans l'intervalle [0, 255].

    Retourne None si l'argument n'est pas de la bonne forme."""
    match = re.fullmatch(r"(\d+),(\d+),(\d+)", argument)
    if match:
        res = tuple(int(v) for v in match.group(1, 2, 3))
        for v in res:
            if v < 0 or v > 255:
                return None
        return res
    return None


if __name__ == "__main__":
    assert str_to_definition("10x30") == (10, 30)
    assert str_to_definition("10,30") is None
    assert str_to_definition("0x30") is None
    assert str_to_definition("10x0") is None
    assert str_to_definition("10.5x30.23") is None

    assert str_to_positive_int("0") == 0
    assert str_to_positive_int("123456789") == 123456789
    assert str_to_positive_int("1234.56789") is None
    assert str_to_positive_int("-1") is None
    assert str_to_positive_int("aaa") is None

    assert str_to_float("0") == 0
    assert str_to_float("1.23") == 1.23
    assert str_to_float("-1.56e13") == -1.56e13
    assert str_to_float(".5e-99") == 0.5e-99
    assert str_to_float(".5e-99a") is None
    assert str_to_float("aa") is None

    assert str_to_color("12,23,34") == (12, 23, 34)
    assert str_to_color("0,0,0") == (0, 0, 0)
    assert str_to_color("255,255,255") == (255, 255, 255)
    assert str_to_color("255,256,255") is None
    assert str_to_color("255,255,256") is None
    assert str_to_color("255, 255, 255") is None
    assert str_to_color("-1,0,0") is None
    assert str_to_color("0,-1,0") is None
    assert str_to_color("0,0,-1") is None
    assert str_to_color("0,10.45,0") is None

from enum import IntEnum

__all__ = ["validate_roman_numeral", "roman2int", "int2roman"]


class RomanNumeral(IntEnum):
    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000


def validate_roman_numeral(numeral):
    return all(char.upper() in RomanNumeral.__members__ for char in numeral)


def roman2int(r):
    "Convert a Roman numeral to decimal integer (case insensitive)"
    # via https://stackoverflow.com/a/62115886/2668831
    numerals = [RomanNumeral[x].value for x in r.upper()]
    return sum(
        [
            -x if i < len(numerals) - 1 and x < numerals[i + 1] else x
            for i, x in enumerate(numerals)
        ]
    )


class RomanNumeralsWithPreceders(IntEnum):
    I = 1
    IV = 4
    V = 5
    IX = 9
    X = 10
    XL = 40
    L = 50
    XC = 90
    C = 100
    CD = 400
    D = 500
    CM = 900
    M = 1000


def int2roman(n):
    if n in [*RomanNumeralsWithPreceders._value2member_map_]:
        return RomanNumeralsWithPreceders(n).name

    for i in [1000, 100, 10, 1]:
        for j in [9 * i, 5 * i, 4 * i, i]:
            if n >= j:
                return int2roman(j) + int2roman(n - j)

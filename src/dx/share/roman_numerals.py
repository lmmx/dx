from enum import IntEnum

__all__ = ["validate_roman_numeral", "roman2int"]

class RomanNumeral(IntEnum):
    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000

def validate_roman_numeral(numeral):
    return all(
        char.upper() in RomanNumeral.__members__ for char in numeral
    )

def roman2int(r):
    "Convert a Roman numeral to decimal integer (case insensitive)"
    # via https://stackoverflow.com/a/62115886/2668831
    numerals = [RomanNumeral[x].value for x in r.upper()]
    return sum([
        -x if i < len(numerals)-1 and x < numerals[i+1] else x
        for i, x in enumerate(numerals)
    ])

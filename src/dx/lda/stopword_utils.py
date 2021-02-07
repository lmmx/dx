from ..share.data import dir_path as data_dir
from enum import Enum
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def load_packaged_stopwords(filename, data_dir=data_dir):
    with open(data_dir / filename, "r") as f:
        words = frozenset(f.read().split())
    return words

class StopWords(Enum):
    ENG = ENGLISH_STOP_WORDS
    BIB = load_packaged_stopwords("stopwords.txt")
    NUM = load_packaged_stopwords("numbers_stopwords100.txt")
    ROM = load_packaged_stopwords("roman_numerals_stopwords100.txt")
    ALL = frozenset.union(ENG, BIB, NUM, ROM)

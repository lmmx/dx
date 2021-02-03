import csv
from ..data import dir_path as data_dir

__all__ = ["data_dir", "topics"]

with open(data_dir / "topics.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    topics = dict(reader)

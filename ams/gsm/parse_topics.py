import csv

with open("topics.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    topics = dict(reader)

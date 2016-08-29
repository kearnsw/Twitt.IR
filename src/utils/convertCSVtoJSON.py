import csv
import json

concern = []
tweets = []
with open("../../data/mistrustData.tsv") as f:
    reader = csv.reader(f, delimiter='\t', quotechar="|")
    next(reader, None)
    for row in reader:
        if len(row[0]) == 1:
            row[0] = "0" + row[0]
        if len(row[1]) == 1:
            row[1] = "0" + row[1]
        date = "2016-" + row[0] + "-" + row[1]
        count = row[2]
        total = row[3]
        concern.append({"date": date, "value": count})
        tweets.append({"date": date, "value": total})

output = open("../../data/mistrustData.json", "wb")
json.dump(concern, output)

import csv


def getDictionary():
    # Create Dictionary from cluster information
    pathDictionary = dict()
    with open("../data/static/clusterData") as f:
        reader = csv.reader(f, delimiter='\t', quotechar='\x07')
        next(reader, None)
        for row in reader:
            if row[0] == "00110111101":
                print row[1]
            pathDictionary[row[1]] = row[0]
    print pathDictionary["research"]
    return pathDictionary

getDictionary()

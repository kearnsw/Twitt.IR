import csv


def getDictionary():
    # Create Dictionary from cluster information
    pathDictionary = dict()
    file = "../data/static/cluster1000"
    with open(file) as f:
        print "Reading paths from " + file
        reader = csv.reader(f, delimiter='\t', quotechar='\x07')
        next(reader, None)
        for row in reader:
            pathDictionary[row[1]] = row[0]

    return pathDictionary

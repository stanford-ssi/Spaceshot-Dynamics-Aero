import csv

def read_csv(filename):
    dic = {}
    with open(filename, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            dic = line
    return dict([key, float(value)] for key, value in dic.items())
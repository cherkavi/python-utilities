import csv

with open("sample.csv") as csv_file:
    reader = csv.reader(csv_file,)
    is_header = True
    for row in reader:
        if is_header:
            is_header = False
            continue
        print(row)
import csv
import os
from pathlib import Path
from datetime import date
from spanish_utils import Spanish_Utils

filename = f'DCHF-output-{date.today()}.csv'
with open(filename, 'r', encoding='utf-8') as inFile:
    reader = csv.reader(inFile)
    count = 1
    with open(f"Spanish-{filename}", 'a+', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for r in reader:
            if count == 1:
                writer.writerow(r)
                count += 1
            else:
                new_data_list = []
                for index in range(0, len(r)):
                    value = r[index]
                    if index == 6:
                        try:
                            value = Spanish_Utils.add_spanish[value.strip()]
                        except:
                            value = r[index]
                    new_data_list.append(value)
                writer.writerow(new_data_list)




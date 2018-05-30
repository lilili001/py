import csv

from googletrans import Translator

def startTranslate():
    translator = Translator()
    lines = []
    r = csv.reader(open('files/data.csv','r'))

    i = 0
    for row in r:
        print(row)
        temp_line = row
        temp_line[0] = translator.translate( row[0] ).text
        temp_line[4] = translator.translate( row[4] ).text
        lines.append(temp_line)

    new_csv = open('files/data_new.csv','w',newline='')
    writer = csv.writer(new_csv)
    writer.writerows(lines)
    new_csv.close()

startTranslate()
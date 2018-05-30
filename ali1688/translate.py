import csv

from googletrans import Translator

from ali1688.helper import str_replace_new


def startTranslate():
    translator = Translator()
    lines = []
    r = csv.reader(open('files/data.csv','r'))

    i = 0
    for row in r:
        print(row)
        temp_line = row
        temp_line[0] = str_replace_new(translator.translate( row[0] ).text)
        temp_line[4] = translator.translate( row[4] ).text
        lines.append(temp_line)

    new_csv = open('files/data_new.csv','w',newline='')
    writer = csv.writer(new_csv)
    writer.writerows(lines)
    new_csv.close()

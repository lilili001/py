import csv
import json

from googletrans import Translator

from ali1688.helper import str_replace_new

def startTranslate():
    translator = Translator()

    new_img_path = 'F:/laragon/www/python/image_hyg/'

    lines = []
    r = csv.reader(open(new_img_path+'data_hyg.csv'   ))
    #r = csv.reader(open('F:\laragon\www\python\image\data.csv','r'))


    for index,row in enumerate(r):
        temp_line = row
        print(index)
        print(row)
        print(   row[0] + ' | ' +row[4] )

        #price
        old_price = row[1]
        temp_price = 0

        if(index >0 ):

            temp_price = float(old_price)*0.5

            if( float(old_price) < 80 ):
                temp_price = 60

            temp_line[10] = float(old_price)+float(temp_price)+ 30
            p = float(old_price)+float(temp_price)+ 30

            #usd
            temp_line[11] =  round (  p/ 6.4 , 2)

            #quantity
            temp_line[12] = 9999

            #trans title
            if row[0] != None and len(row[0])>0:
                title = str( str_replace_new(  row[0] ) )
                title = title.replace(u'\u200b',u' ')

                temp_line[8] = translator.translate(  title   , dest='en'  ).text

            #trans colors
            if row[4] != None and len(row[4])>0 :
                colors = str( row[4]   )
                colors = colors.replace(u'\u200b', u' ')
                print(colors)
                temp_line[9] = translator.translate(  colors    ,dest='en' ).text

        lines.append(temp_line)

    #new_csv = open('F:\laragon\www\python\image\data_trans.csv','w',newline='')
    new_csv = open(new_img_path+'/data_hyg_trans.csv', 'a', newline='',encoding='GB18030')
    writer = csv.writer(new_csv)
    writer.writerows(lines)
    new_csv.close()

    print('=========本次共有%s个产品==========================='%len(lines))
    print(lines)

startTranslate()

#print( u'\u200b'.encode('utf-8').decode('utf-8'))
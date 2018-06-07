import csv
import json

from googletrans import Translator

from ali1688.helper import str_replace_new

import os

import sys

root_path = os.path.abspath('.')

def start():

    new_img_path = root_path+'/csv_org/'

    lines = []
    #r = csv.reader(open(new_img_path+'data_hyg_trans.csv' ,'r'  ,encoding='gbk' ))
    r = csv.reader(open(new_img_path+'data_baita_01_trans.csv' ,'r'   ))
    #r = csv.reader(open('F:\laragon\www\python\image\data.csv','r'))

    for index,row in enumerate(r):

        title = row[8].replace(u'\0xb4',u' ')

        #if index >  0 and  len(row) > 0 and row is not None  :
        print(index)

        temp_line = []
        temp_line.append('1010292')
        temp_line.append(title)
        temp_line.append('Woman dress')
        temp_line.append('')
        temp_line.append('new')
        temp_line.append(title)
        temp_line.append('9999')
        temp_line.append(row[11])
        temp_line.append('5')
        temp_line.append('https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/1.jpg' % row[2])
        temp_line.append('https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/2.jpg' % row[2])
        temp_line.append('https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/3.jpg' % row[2])
        temp_line.append('')
        temp_line.append('Color:'+row[9] +';Size:'+row[5])
        temp_line.append('Woman Dress')
        temp_line.append('Summer Dress')
        temp_line.append('Big size dress')
        temp_line.append('Hotsale dress')
        # temp_line[0] = '1010292' #category
        # temp_line[1] =  row[8]       #title
        # temp_line[2] =  'Woman dress'      #product_type
        # temp_line[3] =  ''      #brand
        # temp_line[4] =  'new'      #condition
        # temp_line[5] =  ''      #description
        # temp_line[6] =  '9999'      #quantity
        # temp_line[7] =  row[11]      #price
        # temp_line[8] =  '5'      #shipping
        # temp_line[9] =  'https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/1.jpg' % row[2]      #image1
        # temp_line[10] =  'https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/2.jpg' % row[2]    #image2
        # temp_line[11] =  'https://res.cloudinary.com/dzf6pxzir/image/upload/%s/800/3.jpg' % row[2]    #image3
        # temp_line[12] =  ''     #country_shipping
        # temp_line[13] =  'Colors:'+row[9] +'Sizes:'+row[5]     #item_specifics
        # temp_line[14] =  'Woman Dress'     #keyword1
        # temp_line[15] =  'Summer Dress'     #keyword2
        # temp_line[16] =  'Big size dress'     #keyword3
        # temp_line[17] =  'Hotsale dress'     #keyword4

        lines.append(temp_line)


    #new_csv = open('F:\laragon\www\python\image\data_trans.csv','w',newline='')
    new_csv = open(new_img_path+'/baita_ioffer.csv', 'a', newline=''  )
    writer = csv.writer(new_csv)
    writer.writerow(( 'category' ,'title','product_type','brand','condition',
                      'description','quantity','price','shipping','image1','image2','image3',
                      'country_shipping','item_specifics','keyword1','keyword2','keyword3','keyword4'))
    writer.writerows(lines)
    new_csv.close()

    print('=========本次共有%s个产品==========================='%len(lines))
    print(lines)

start()

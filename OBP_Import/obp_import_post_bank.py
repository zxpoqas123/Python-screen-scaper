__author__ = 'simonredfern'

import csv


#from pymongo import Connection


'''
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

'''



def do_import():
    print ('starting import')
    #connection = Connection('localhost', 27017)
    #db = connection.obp_imports

    #collection = db.post_bank_musicpictures

    # Note: enca command line tool can show char set info
    csv_path = '/home/akendo/Work/Tesobe/Pro/Projects/try_out/OBP_Import/PB_Umsatzauskunft.csv'
    delimiter = ';'
    quote_char = '"'


    a = open("PB_Umsatzauskunft.csv", "rb")
    #transactionReader = csv.reader(open(csv_path, 'rb'), delimiter=delimiter, quotechar=quote_char)

    #transactionReader = unicode_csv_reader(open(csv_path, 'rb'), delimiter=delimiter, quotechar=quote_char)

    for row in a:
        #import pdb; pdb.set_trace()
        print row

    print 'done'


if __name__ == '__main__':
    do_import()






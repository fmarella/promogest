#-*- coding: iso-8859-15 -*-
#CsvGenerator.py

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Marco Pinna "Dr astico" <zoccolodignu@gmail.com>


import csv
from promogest.ui.utils import *

class CsvFileGenerator:
    """convert a bidimensional array to a csv file (as table)"""

    def __init__(self, _file, encoding="utf-8"):
        my_csv_file=file(str(_file), 'wb')
        self.csvFile = csv.writer(my_csv_file, dialect='excel')

    def setAttributes(self, head, cols, data, totColumns=None):
        self.head = head
        self.cols = cols
        self.data = data
        self.totColumns = totColumns

    def createFile(self, wtot=False):
        """Writes the head, the data, and eventually, makes the sum of the numenrical fields

        (as columns) and writes it at the end of the file."""
        head = self.head
        data = self.data
        self.sum0 = 0
        self.sum1 = 0
        self.sum2 = 0
        flag = 0

        self.csvFile.writerow(head)
        for row in data:
            self.csvFile.writerow(row)
            if wtot:
                for elem in row:
                    if isinstance(elem, float):
                        if flag ==0:
                            self.sum0 += elem
                            flag = 1
                        elif flag == 1:
                            self.sum1 += elem
                            flag=2
                        elif flag == 2:
                            self.sum2 += elem
        if wtot:
            lastlist = []
            flag = 0
            for pos in self.totColumns:
                if pos == 0:
                    lastlist.append('')
                elif pos == 1:
                    lastlist.append('Totale:')
                elif pos == 2:
                    if flag == 0:
                        lastlist.append(('%.2f') % self.sum0)
                        flag = 1
                    elif flag == 1:
                        lastlist.append(('%.2f') % self.sum1)
                        flag = 2
                    elif flag == 2:
                        lastlist.append(('%.2f') % self.sum2)
                    else:
                        print('Unknown field type: Have no values to insert')
                        lastlist.append('')
            self.csvFile.writerow(lastlist)

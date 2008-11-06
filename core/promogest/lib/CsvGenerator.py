#-*- coding: iso-8859-15 -*-
#CsvGenerator.py

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import os
import csv
import gtk
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

#-*- coding: iso-8859-15 -*-
#XmlGenerator.py

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
import SimpleXMLWriter
from promogest.ui.utils import *

from SimpleXMLWriter import XMLWriter

class XlsXmlGenerator:
    """Convert a database query result into an xml spreadsheet file"""

    def __init__(self, _file, encoding="utf-8"):
        self.myfile=open(str(_file), 'w')
        self.filename = XMLWriter(_file, encoding)

    def setAttributes(self, head, cols, data, totColumns=None, sn=1):
        self.head = head
        self.cols = cols
        self.values = data
        self.totColumns = totColumns
        self.sn = sn

    def XlsXmlHeader(self):
        """Set up all the Xml code that we need to make a well formed document for MSO 2003"""
        wrkbook_attr={'xmlns':'urn:schemas-microsoft-com:office:spreadsheet',
                    'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance',
                    'xmlns:x':'urn:schemas-microsoft-com:office:excel',
                    'xmlns:x2':'http://schemas.microsoft.com/office/excel/2003/xml',
                    'xmlns:ss':'urn:schemas-microsoft-com:office:spreadsheet',
                    'xmlns:o':'urn:schemas-microsoft-com:office:office',
                    'xmlns:html':'http://www.w3.org/TR/REC-html40',
                    'xmlns:c':'urn:schemas-microsoft-com:office:component:spreadsheet'}
        ods_attr={'xmlns':'urn:schemas-microsoft-com:office:office'}
        EWB_attr={'xmlns':'urn:schemas-microsoft-com:office:excel'}
        Style_attr={'ss:ID':'Default', 'ss:Name':'Default'}
        Style_attr1={'ss:ID':'Result', 'ss:Name':'Result'}
        Style_attr2={'ss:ID':'Result2', 'ss:Name':'Result2'}
        Style_attr3={'ss:ID':'Heading', 'ss:Name':'Heading'}
        Style_attr4={'ss:ID':'Heading1', 'ss:Name':'Heading1'}
        Style_attr5={'ss:ID':'co1'}
        Style_attr6={'ss:ID':'ta1'}
        #specific cells attributes start here
        Style_attr7={'ss:ID':'ce1'}
        Style_attr8={'ss:ID':'ce2'}
        Style_attr9={'ss:ID':'ce3'}
        Style_attr10={'ss:ID':'ce4'}
        Style_attr11={'ss:ID':'ce5'}
        Style_attr12={'ss:ID':'ce6'}
        Style_attr13={'ss:ID':'ce7'}
        Style_attr14={'ss:ID':'ce8'}
        Style_attr15={'ss:ID':'ce9'}
        Style_attr16={'ss:ID':'ce10'}
        Style_attr17={'ss:ID':'ce11'}
        Style_attr18={'ss:ID':'ce12'}
        Bord_bott_attr={'ss:Position':'Bottom', 'ss:LineStile':'Continous', 'ss:Weight':'1', 'ss:Color':'#000000'}
        Bord_left_attr={'ss:Position':'Left', 'ss:LineStile':'Continous', 'ss:Weight':'1', 'ss:Color':'#000000'}
        Bord_top_attr={'ss:Position':'Top', 'ss:LineStile':'Continous', 'ss:Weight':'1', 'ss:Color':'#000000'}
        Bord_right_attr={'ss:Position':'Right', 'ss:LineStile':'Continous', 'ss:Weight':'1', 'ss:Color':'#000000'}
        Interior_attributes={'ss:Color':'#ffb515', 'ss:Pattern':'Solid'}
        Interior_attributes1={'ss:Color':'#fff515','ss:Pattern':'Solid'}
        Font_attr={'ss:Bold':'1', 'ss:Italic':'1', 'ss:Underline':'Single'}
        Font_attr1={'ss:Bold':'1', 'ss:Italic':'1', 'ss:Size':'16'}
        Font_attr2={'ss:Bold':'1'}
        NF_attr={'ss:Format':'Euro Currency'}
        Align_attr={'ss:Horizontal':'Center'}
        Align_cent_attr={'ss:Horizontal':'Center', 'ss:Vertical':'Center', 'ss:indent':'0'}
        Align_left_attr={'ss:Horizontal':'Left', 'ss:Vertical':'Center', 'ss:indent':'0'}
        Align_right_attr={'ss:Horizontal':'Right', 'ss:Vertical':'Center', 'ss:indent':'0'}
        ssWs_attr={'ss:Name':'Tabella1'}

        self.filename.declaration()
        self.filename.suffix()
        self._id = self.filename.start('Workbook', wrkbook_attr)
        self.filename.start('OfficeDocumentSettings', ods_attr)
        self.filename.start('Colors')
        self.filename.start('Color')
        self.filename.start('Index')
        self.filename.data('3')
        self.filename.end('Index')
        self.filename.start('RGB')
        self.filename.data('#c0c0c0')
        self.filename.end('RGB')
        self.filename.end('Color')
        self.filename.start('Color')
        self.filename.start('Index')
        self.filename.data('4')
        self.filename.end('Index')
        self.filename.start('RGB')
        self.filename.data('#ff0000')
        self.filename.end('RGB')
        self.filename.end('Color')
        self.filename.start('Color')
        self.filename.start('Index')
        self.filename.data('5')
        self.filename.end('Index')
        self.filename.start('RGB')
        self.filename.data('#ffb515')
        self.filename.end('RGB')
        self.filename.end('Color')
        self.filename.end('Colors')
        self.filename.end('OfficeDocumentSettings')
        self.filename.start('ExcelWorkBook',EWB_attr)
        self.filename.start('WindowHeight')
        self.filename.data('9000')
        self.filename.end('WindowHeight')
        self.filename.start('WindowWidth')
        self.filename.data('13860')
        self.filename.end('WindowWidth')
        self.filename.start('WindowTopX')
        self.filename.data('240')
        self.filename.end('WindowTopX')
        self.filename.start('WindowTopY')
        self.filename.data('75')
        self.filename.end('WindowTopY')
        self.filename.start('ProtectStructure')
        self.filename.data('False')
        self.filename.end('ProtectStructure')
        self.filename.start('ProtectWindows')
        self.filename.data('False')
        self.filename.end('ProtectWindows')
        self.filename.end('ExcelWorkBook')
        self.filename.start('Styles')
        self.filename.start('Style',Style_attr)
        self.filename.end('Style')
        self.filename.start('Style',Style_attr1)
        self.filename.start('Font',Font_attr)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr2)
        self.filename.start('Font',Font_attr)
        self.filename.end('Font')
        self.filename.start('NumberFormat',NF_attr)
        self.filename.end('NumberFormat')
        self.filename.end('Style')
        self.filename.start('Style',Style_attr3)
        self.filename.start('Alignment',Align_attr)
        self.filename.end('Alignment')
        self.filename.start('Font',Font_attr1)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr4)
        self.filename.start('Alignment', Align_attr)
        self.filename.end('Alignment')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr5)
        self.filename.end('Style')
        self.filename.start('Style', Style_attr6)
        self.filename.end('Style')
        self.filename.start('Style', Style_attr7)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_left_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.start('Interior', Interior_attributes)
        self.filename.end('Interior')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr8)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.start('Interior', Interior_attributes)
        self.filename.end('Interior')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr9)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.start('Interior', Interior_attributes)
        self.filename.end('Interior')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr10)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_left_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr11)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr12)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_left_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr13)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_right_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr14)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_right_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr15)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_left_attr)
        self.filename.end('Alignment')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr16)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_left_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_cent_attr)
        self.filename.end('Alignment')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.start('Interior', Interior_attributes1)
        self.filename.end('Interior')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr17)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_left_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_right_attr)
        self.filename.end('Alignment')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.start('Interior', Interior_attributes1)
        self.filename.end('Interior')
        self.filename.end('Style')
        self.filename.start('Style', Style_attr18)
        self.filename.start('Borders')
        self.filename.start('Border', Bord_bott_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_right_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_left_attr)
        self.filename.end('Border')
        self.filename.start('Border', Bord_top_attr)
        self.filename.end('Border')
        self.filename.end('Borders')
        self.filename.start('Alignment', Align_right_attr)
        self.filename.end('Alignment')
        self.filename.start('Font', Font_attr2)
        self.filename.end('Font')
        self.filename.start('Interior', Interior_attributes1)
        self.filename.end('Interior')
        self.filename.end('Style')
        self.filename.end('Styles')

    #writes up data in the xml document from a sql cursor
    #the same function writes II, III and more spreadsheet by specifying the sheet number "sn"
    #making a function call for each sheet you need to create.
    def XlsXmlsheet(self, wtot):
        """writes the concrete data you need to be in the spreadsheet

        if more than one data sheet is needed to be written, just do multiple calls to this function
        before you close the document. Making successive calls to this function, the 'sn' ("Sheet Number")
        attribute is required to be increased each time by one."""
        #This way seems to work good enough,
        #But for the future, consider to make some method that
        #try to 'append' another list of data to the generated document as separated worksheet"""
        sn = str(self.sn)
        work_attr = {'ss:Name':'tabella'+sn}
        tab_attr = {'ss:StyleID':'ta1'}
        row_attr = {'ss:Height':'15.6425'}
        ce = [{'ss:StyleID':'ce1'},
            {'ss:StyleID':'ce2'},
            {'ss:StyleID':'ce3'}]
        da = [{'ss:Type':'String'},
            {'ss:Type':'Number'}]

        #let's define the columns styles for the table we are generating
        cols= self.cols
        col_num = range(len(cols))
        col = []
        for n in col_num:
            if n == 0: #first field has always centered text-style
                single_col = {'ss:StyleID':'ce4', 'ss:Width':cols[n][0]}
            elif 1 <= n < col_num[-1]:
                if cols[n][1] == 'l': #As left
                    single_col = {'ss:StyleID':'ce6', 'ss:Width':cols[n][0]}
                elif cols[n][1] == 'r': #As right
                    single_col = {'ss:StyleID':'ce7', 'ss:Width':cols[n][0]}
                elif cols[n][1] == 'c': #As center
                    single_col = {'ss:StyleID':'ce5', 'ss:Width':cols[n][0]}
                else:
                    raise Exception('Unknown style!')
            elif n == col_num[-1]:
                if cols[n][1] == 'r':
                    single_col = {'ss:StyleID':'ce8', 'ss:Width':cols[n][0]}
                elif cols[n][1] == 'l':
                    single_col = {'ss:StyleID':'ce9', 'ss:Width':cols[n][0]}
            else:
                print "WARNING!! unknown column style! Is this normal??"
                single_col={}
            col.append(single_col)

        self.filename.start('ss:Worksheet', work_attr)
        self.filename.start('Table', tab_attr)

        head = self.head
        li = range(len(cols))
        for i in li:
            self.filename.start('Column', col[i])
            self.filename.end('Column')
        self.filename.start('Row', row_attr)
        for i in li:
            if i == 0:
                self.filename.start('Cell', ce[0])
                self.filename.start('Data', da[0])
                self.filename.data(head[i])
                self.filename.end('Data')
                self.filename.end('Cell')
            elif 1 <= i < li[-1]:
                self.filename.start('Cell', ce[1])
                self.filename.start('Data', da[0])
                self.filename.data(head[i])
                self.filename.end('Data')
                self.filename.end('Cell')
            elif i == li[-1]:
                self.filename.start('Cell', ce[2])
                self.filename.start('Data', da[0])
                self.filename.data(head[i])
                self.filename.end('Data')
                self.filename.end('Cell')

        self.filename.end('Row')

        #Now let's play. the real data inserting starts here
        flag = 0
        values = self.values
        self.sum0 = 0
        self.sum1 = 0
        self.sum2 = 0
        self.num_rows = 1
        for row in values:
            self.num_rows = self.num_rows + 1
            self.filename.start('Row', row_attr)
            for r in row:
                self.filename.start('Cell')
                if isinstance(r, str):
                    self.filename.start('Data', da[0])
                    self.filename.data(r)
                    self.filename.end('Data')
                elif isinstance(r,float):
                    __r = str(( '%.2f') % r)
                    self.filename.start('Data',da[1])
                    self.filename.data(__r)
                    self.filename.end('Data')
                    #flag is needed to know how many numerical fields are in the table
                    #to permit the sum of each value without miss the order of the data
                    if wtot:
                        if flag == 0:
                            self.sum0 +=  r
                            flag = 1
                        elif flag == 1:
                            self.sum1 +=  r
                            flag = 2
                        elif flag == 2:
                            self.sum2 += r
                elif isinstance(r,Decimal):
                    __r = str(r)
                    self.filename.start('Data',da[1])
                    self.filename.data(__r)
                    self.filename.end('Data')
                    #flag is needed to know how many numerical fields are in the table
                    #to permit the sum of each value without miss the order of the data
                    if wtot:
                        if flag == 0:
                            self.sum0 +=  r
                            flag = 1
                        elif flag == 1:
                            self.sum1 +=  r
                            flag = 2
                        elif flag == 2:
                            self.sum2 += r
                else:
                    self.filename.start('Data', da[0])
                    self.filename.data(str(r) or '')
                    self.filename.end('Data')
                self.filename.end('Cell')

            flag = 0
            self.filename.end('Row')
        if wtot:
            self.setTotalColumns()
            self.closeSheet()
        else:
            self.closeSheet()

    def closeSheet(self):
        self.filename.end('Table')
        self.filename.start('x:WorksheetOptions')
        self.filename.end('x:WorksheetOptions')
        self.filename.end('ss:Worksheet')

    def setTotalColumns(self):
        """Writes up the code needed to create sum of values indicated by "columns"

        columns should be a list, and each value is paired with a table field (in the order) and can be 0, 1 or 2.
        0 is for an empty cell,
        1 is for the "Totale" word,
        2 is to tell the function to format the cell with the value of the sum"""
        columns = self.totColumns
        rowStyle = {'ss:Height':'15.6425'}
        ce = {'ss:StyleID':'ce10'}
        da = [{'ss:Type':'String'},
            {'ss:Type':'Number'}]
        rows = self.num_rows
        self.filename.start('Row', rowStyle)
        for o in columns:
            if o == 0:
                self.filename.start('Cell')
                self.filename.start('Data', da[0])
                self.filename.data('')
                self.filename.end('Data')
                self.filename.end('Cell')
            elif o == 1:
                self.filename.start('Cell', ce)
                self.filename.start('Data', da[0])
                self.filename.data('Totale:')
                self.filename.end('Data')
                self.filename.end('Cell')
            else:
                sum0 = str(('%.2f') % self .sum0)
                sum1 = str(('%.2f') % self .sum1)
                sum2 = str(('%.2f') % self .sum2)
                flag = 0
                rr= str(rows-1)
                formula_str = '=DOLLAR(SUM(R[-'+rr+']C:R[-1]C);2)'
                cel_formula = {'ss:StyleID':'ce12','ss:Formula':formula_str}
                self.filename.start('Cell', cel_formula)
                self.filename.start('Data', da[0])
                if flag == 0:
                    self.filename.data('�     '+sum0)
                    flag = 1
                elif flag == 1:
                    self.filename.data('�     '+sum1)
                    flag = 2
                elif flag == 2:
                    self.filename.data('�     '+sum2)
                self.filename.end('Data')
                self.filename.end('Cell')

        self.filename.end('Row')


    def createFile(self, wtot=False):
        self.XlsXmlHeader()
        self.XlsXmlsheet(wtot)
        self.XlsXmlFooter()

    def XlsXmlFooter(self):
        """Simply closes the Worksheet tags at the end of the file"""
        self.filename.close(self._id)

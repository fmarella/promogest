# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
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

import ooolib
from decimal import *
import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.common import *
from reportlab.graphics.barcode.usps import *
from reportlab.graphics.barcode import getCodes, getCodeNames, createBarcodeDrawing
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Frame, Paragraph
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate


class Labels(BaseDocTemplate):

    def __init__(self, param,filename=None, **kw):
        #apply(BaseDocTemplate.__init__, (self, filename), kw)
        #self.addPageTemplates(
            #[
             #PageTemplate(id='plain',
               #           frames=[Frame(2.5*cm, 2.5*cm, 16*cm, 25*cm, id='F1')]
              #            ),
             #LeftPageTemplate(),
             #RightPageTemplate()
            #]
            #)
        self.param = param
        self.doc = ooolib.Calc()
        self.flag = 0
        self.lst = []
        self.run()



    def myMainPageFrame(canvas, doc):
        "The    page frame used for all PDF documents."

        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        pageNumber = canvas.getPageNumber()
        canvas.drawString(10*cm, cm, str(pageNumber))
        canvas.restoreState()


    def createbarcode(self):
        #self.story.append(Paragraph('vanilla{P}', styleN))
        bcd = createBarcodeDrawing('EAN13', value='4000417020000',width=4.8*cm,height=0.8*cm)
        return bcd


    def buildingPage(self):
        """
        """
        paramLen = len(self.param)
        stream = ""
        self.colonna = 0
        self.riga = 0
        maxRow = 3
        self.scartoRow = 0
        self.scartoColumn = 0
        for index in range(len(self.param)):
            if index == 0:
                self.scartoRow = 0
                self.scartoColumn = 0
            elif not index%2:
                self.scartoRow = self.scartoRow + 3
                self.scartoColumn = 0
            else:
                self.scartoColumn = 2
            self.run()

        filename = ".f.ods"
        self.doc.save(filename)
        tryFile = open(filename, 'rb')
        return tryFile


        #print dir(bcd)
    #story.append(bcd)

    def getTable(self):
        barc = self.createbarcode()
        index =3
        #prezzo = Paragraph("""<para>"€ " + str(Decimal(self.param[index]['prezzo_dettaglio']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))</para>""")
        prezzo = "€ " + str(Decimal(self.param[index]['prezzo_dettaglio']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        iva = str(int(self.param[index]['percentuale_iva'])) +"%"
        codiceArticolo = self.param[index]['codice_articolo']
        desc = self.param[index]['articolo'][0:25]
        date = datetime.datetime.now().strftime('%d/%m/%y')

        t = Table((
                (barc,codiceArticolo,""),
                (desc,"",iva),
                (prezzo,"", date)),
                (5*cm,2*cm,2*cm),
                (1*cm, 0.6*cm,0.9*cm)
                )
        return t


    def makeStyles(self):
        styles = []
        for i in range(5):
            styles.append(TableStyle([('ALIGN', (2,1), (-1,-1), 'LEFT'),
                                    ('ALIGN', (0,0), (-1,0), 'CENTRE'),
                                    ('HREF', (0,0), (0,0), 'www.google.com'),
                                    ]))
        for style in styles[1:]:
            style.add('GRID', (0,0), (-1,-1), 0.25, colors.green)
        for style in styles[2:]:
            style.add('LINEBELOW', (0,0), (-1,0), 2, colors.black)
        for style in styles[3:]:
            style.add('LINEABOVE', (0, -1), (-1,-1), 2, colors.black)
        styles[-1].add('LINEBELOW',(1,-1), (-1, -1), 2, (0.5, 0.5, 0.5))
        return styles


    def run(self):
        doc =Canvas('label_promogest.pdf')
        #doc = SimpleDocTemplate(outputfile('label_promogest.pdf'), pagesize=(8.5*inch, 11*inch), showBoundary=1)
        style = TableStyle([('ALIGN', (0,0), (2,1), 'LEFT'),
                            ('GRID', (0,0), (-1,-1), 0.25, colors.green),
                            #('ALIGN', (1,2), (-1,-1), 'RIGHT'),
                            ('FONTSIZE',(0,2),(0,2),15),
                            #('LINEABOVE', (0, -1), (-1,-1), 2, colors.black),
                            #('LINEBELOW',(1,-1), (-1, -1), 2, (0.5, 0.5, 0.5)),
                            ])
        t = self.getTable()
        t.setStyle(style)
        self.lst.append(t)
        #self.lst.append(Spacer(0,12))
        f = Frame(cm, cm, 9*cm, 3*cm, showBoundary=1)
        f.addFromList(self.lst,doc)
        doc.save()


    def singleLabelOds(self, index):

        self.doc.set_column_property(1 + self.scartoColumn, 'width', '2.9in')
        self.doc.set_column_property(2 + self.scartoColumn, 'width', '0.6in')
        self.doc.set_row_property(1 + self.scartoRow, 'height', '0.2in')
        self.doc.set_row_property(2 + self.scartoRow, 'height', '0.3in')
        self.doc.set_row_property(3 + self.scartoRow, 'height', '0.7in')
        self.doc.set_cell_property('valign', 'middle')
        self.doc.set_cell_property('bold', True)
        self.doc.set_cell_value(1 + self.scartoColumn,
                                1 + self.scartoRow,
                                "string",
                                self.param[index]['codice_articolo'])
        self.doc.set_cell_property('bold', False)

        self.doc.set_cell_property('bold', True)
        self.doc.set_cell_property('fontsize', '12')
        self.doc.set_cell_value(1 + self.scartoColumn,
                                2 + self.scartoRow,
                                "string",
                                self.param[index]['articolo'][0:25])
        self.doc.set_cell_property('fontsize', '10')
        self.doc.set_cell_property('bold', False)

        self.doc.set_cell_property('bold', True)
        #self.doc.set_cell_property('color', '#ff0000')
        self.doc.set_cell_property('halign', 'center')
        self.doc.set_cell_value(2 + self.scartoColumn,
                                1 + self.scartoRow,
                                "string",
                                 str(int(self.param[index]['percentuale_iva'])) +"%")
        #self.doc.set_cell_property('color', 'default')
        self.doc.set_cell_property('bold', False)

        self.doc.set_cell_property('bold', True)
        self.doc.set_cell_property('fontsize', '32')
        self.doc.set_cell_property('italic', True)
        self.doc.set_cell_value(1 + self.scartoColumn,
                                3 + self.scartoRow,
                                "string",
                                "€ " + str(Decimal(self.param[index]['prezzo_dettaglio']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        self.doc.set_cell_property('italic', False)
        self.doc.set_cell_property('fontsize', '10')
        self.doc.set_cell_property('halign', 'left')
        self.doc.set_cell_property('bold', False)

        self.doc.set_cell_property('bold', True)
        self.doc.set_cell_value(2 + self.scartoColumn,
                                3 + self.scartoRow,
                                "string",
                                datetime.datetime.now().strftime('%d/%m/%y'))
        self.doc.set_cell_property('bold', False)
        self.colonna = 0
        self.flag = 1


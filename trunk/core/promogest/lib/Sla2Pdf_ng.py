# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os

from reportlab.lib import colors, utils
from reportlab.platypus import Table, TableStyle, Frame, Image
from reportlab.pdfgen.canvas import Canvas
from promogest import Environment
from promogest.lib import Sla2pdfUtils
from promogest.lib import ColorDicTFull


class Sla2Pdf_ng(object):
    """ sla to pdf format translation """

    def __init__(self, document, pdfFolder,
                         version, tablesProperties,
                         pgObjList, numPages,
                         iteratableGroups):
        """
        Build a template object based on the specified file-like
        object and sequence of objects
        """
        self.pdfFolder = pdfFolder 
        self.pdfFileName = '_temp'
        self.version = version
        self.tablesProperties = tablesProperties
        self.document = document
        self.pageObjects = self.document.findall('PAGEOBJECT')
        self.pgObjList = pgObjList
        self.numPages = numPages
        self.iteratableGroups = iteratableGroups
        self.translate()

    def translate(self):
        self.pageProperties = Sla2pdfUtils.pageProFunc(self.document)
        self.canvas = Canvas(filename = self.pdfFolder + self.pdfFileName + '.pdf', pagesize=(self.pageProperties[0][8],self.pageProperties[0][7]))
        # Page's table
        reiter = False
        self.pdfPage = 0
        for e in xrange(0, self.numPages):
            self.pdfPage = e
            for group in self.tablesProperties:
                self.group = group.keys()[0]
                self.tablesPropertie = group.values()[0]
                try:
                    self.group= self.group.strip().split('%%%')[0]
                except:
                    self.group= self.group.strip()
                if self.group in self.iteratableGroups:
                    colu = int(self.tablesPropertie['columns'])
                    self.tablesPropertie['iterproper'] = self.tablesPropertie['parasobj'][colu:(colu*2)]
                    reiter = True
                cells = int(self.tablesPropertie['cells'])
                # Closing pages (elements of the same page must be near)
                if "noGroup" in self.group and self.tablesPropertie["pfile"] != "" :
                    #print "IMMAGINEEEEEEEEEEEEEEE", self.group, self.tablesPropertie["isTableItem"]
                    self.drawImage(group=self.group) # IMMAGINE
                elif "noGroup" in self.group  and self.tablesPropertie["pfile"] == "":
                    #print "MONOCELLAAAAAAA", self.group, self.tablesPropertie
                    self.drawTable(group =self.group, monocell=True)# MONOCELLA
                else:
#                    print "TABELLAAAAAAAA", self.group, self.tablesPropertie["isTableItem"]
                    self.drawTable(group =self.group, reiter = reiter) # TABELLA
            self.canvas.saveState()
            self.canvas.showPage()
        self.canvas.save()

    def drawImage(self,group):
        """ Drawing an image """
        pfile = self.tablesPropertie['pfile']
        (imgPath, imgFile) = os.path.split(pfile)
        #innerIterator = self.iterator
        width = self.tablesPropertie['widths'][0]
        height = self.tablesPropertie['heights'][0]
        xPos = self.tablesPropertie['xpos'][0]
        yPos = self.tablesPropertie['ypos'][0]
        img = utils.ImageReader(Environment.imagesDir + imgFile)
        self.canvas.drawImage(img,
                            xPos - self.pageProperties[self.pdfPage][9],
                            self.pageProperties[0][7] - yPos - height + self.pageProperties[self.pdfPage][10],
                            width=width,
                            height=height)
        self.canvas.saveState()

    def drawTable(self, group=None, monocell=None, reiter = None):
        """ Drawing a table """
        matrix = []
        lst = []
        matrix2 = []
        vector = []
        # Total of element's table
        cells = int(self.tablesPropertie['cells'])
        columns = int(self.tablesPropertie['columns'])
        rows = int(self.tablesPropertie['rows'])
        widths = self.tablesPropertie['widths']
        heights = self.tablesPropertie['heights']
        xpos = self.tablesPropertie['xpos']
        ypos = self.tablesPropertie['ypos']
        print "DATI", cells, columns, rows, group, heights, widths
        contColumns = 0
        ch = ''
        col = 0
        cycle = False
        vector = []
        alignment= None
        itexts = self.tablesPropertie['itextsobj']
        paras = self.tablesPropertie['parasobj']
        stile = TableStyle([])
        stile.add('VALIGN',(0,0),(-1,-1),'TOP')
        tblprop = self.tablesPropertie['cellProperties']
        if monocell==True:
            cells = 1
            columns=1
            rows = 1
        for v in xrange(0,cells):
            if v == 0:
                contRows = 0
                contColumns = 0
            elif columns==1:
                contColumns = -1
                contRows= int(v/columns)
            else:
                contRows= int(v/columns)
                contColumns = ((v)%columns)
            background = self.backgroundFunc(tblprop[v])# Finding background
            hexBorderColor = self.hexBorderColorFunc(tblprop[v]['borderColor'])
            stile.add('ROWBACKGROUNDS', (contColumns,contRows),
                                (contColumns,contRows),
                                (background, background))
            cellpr = tblprop[v]
            cellpict = cellpr['cellPicture']
            cellIMGHeight = cellpr['cellHeight']
            cellIMGWidth = cellpr['cellWidth']
            if (cellpr['bottomLine'] == 1 and cellpr['topLine'] == 1 and\
                        cellpr['leftLine'] == 1 and cellpr['rightLine'] == 1):
                stile.add('BOX', (contColumns,contRows),
                                (contColumns,contRows),
                                cellpr['lineWidth'],
                                hexBorderColor)
            else:
                if cellpr['bottomLine'] == 1:
                    stile.add('LINEBELOW', (contColumns,contRows),
                                (contColumns,contRows),
                                cellpr['lineWidth'],
                                hexBorderColor)
                elif cellpr['topLine'] == 1:
                    stile.add('LINEABOVE', (contColumns,contRows),
                                (contColumns,contRows),
                                cellpr['lineWidth'],
                                hexBorderColor)
                if cellpr['leftLine'] == 1:
                    stile.add('LINEBEFORE', (contColumns,contRows),
                                (contColumns,contRows),
                                cellpr['lineWidth'],
                                hexBorderColor)
                if cellpr['rightLine'] == 1:
                    stile.add('LINEAFTER', (contColumns,contRows),
                                (contColumns,contRows),
                                cellpr['lineWidth'],
                                hexBorderColor)

            if not monocell:
                ch = self.chFunc(itexts[v])[0]
                itext = self.chFunc(itexts[v])[1]
            else:
                try:
                    itext = itexts[0]
                    ch = itexts[0].get('CH')
                except:
                    itext = None
                    ch = ""
            # self.chFunc(itexts[0])[1]
            actualPageObject = self.tablesPropertie# Borders
            uff = self.tablesPropertie['iterproper']
            if uff != [] and v > columns:
                pdfAlignment = self.alignmentFunc(self.tablesPropertie['iterproper'][contColumns],v, reiter=True)
            else:
                pdfAlignment = self.alignmentFunc(paras, v, monocell) #alignment
            stile.add('ALIGN', (contColumns,contRows),
                                (contColumns,contRows),
                                pdfAlignment)
            if itext != None:
                fontName = self.fontNameFunc(itext) #  Font name
                stile.add('FONT', (contColumns,contRows),
                                    (contColumns,contRows),
                                    fontName)

                fontSize = self.fontSizeFunc(itext)# Font size
                stile.add('FONTSIZE', (contColumns,contRows),
                                    (contColumns,contRows),
                                    fontSize)

                foreground = self.foregroundFunc(itext) #foreground
                stile.add('TEXTCOLOR', (contColumns,contRows),
                                    (contColumns,contRows),
                                    foreground)
                if "bcview" in ch:
                    alignment="LEFT"
                    vector.append(Sla2pdfUtils.createbarcode(ch))
                else:
                    vector.append(Sla2pdfUtils.makeParagraphs(ch, background, foreground, alignment, fontName, fontSize))
            elif cellpict:
                (imgPath, imgFile) = os.path.split(cellpict)
                path = Environment.imagesDir + imgFile
                widthIMG = (float(cellIMGHeight)-2)*100/(float(cellIMGWidth)-2)
                img = Image(path,width=widthIMG,height=float(cellIMGHeight)-2)
                vector.append(img)
            else:
                vector.append('')
            if monocell==True:
                cycle= True
            elif ((v+1)%columns) == 0:
                contRows = 0
                cycle= True
            if cycle == True:
                matrix.append(vector)
                vector = []
                cycle = False
#        if columns > 1 and not reiter:
#            #wid = []
#            hei = []
#            for h in range(0,len(heights),rows):
#                hei.append(heights[h])
#            heights = hei
#        print "MATRIXXXXXXXXXXXXXXXXX", matrix,widths[:columns],heights[:rows], rows
        table=Table(matrix,style=stile,  colWidths=widths[:columns], rowHeights=heights[:rows])

        lst.append(table)
        # Effective table size
        sumRows = Sla2pdfUtils.sumRowsFunc(heights,rows)
        sumColumns = Sla2pdfUtils.sumColumnsFunc(widths,columns)
#        print "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", sumRows, sumColumns
        f = Frame(x1=(xpos[0] - self.pageProperties[self.pdfPage][9]),
                    y1=(self.pageProperties[self.pdfPage][7] - ypos[0] - sumRows + self.pageProperties[self.pdfPage][10] - 12),
                    width=sumColumns,
                    height=(sumRows+12),
                    showBoundary=0)
        sumRows = sumColumns = 0
        f.addFromList(lst, self.canvas)
        reiter = False
        #self.canvas.saveState()

    # ATTENZIONE !!!   this part above is for generic function.

    def fontSizeFunc(self, itext):
        fontSize = "0"
        # Font size
        if self.version:
            try:
                fontSize = float(itext.get('FONTSIZE'))
            except:
                pass
        else:
            fontSize = float(itext.get('CSIZE'))
        if fontSize =="0":
            CHARSTYLE = self.document.findall('CHARSTYLE')[0]
            fontSize = float(CHARSTYLE.get('FONTSIZE'))
                #fontSize = "8"
        return fontSize

    def fontNameFunc(self, itext, monocell=False):
        if self.version:
            fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('FONT')))
        else:
            fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('CFONT')))
        return fontName

    def alignmentFunc(self,paras, v, monocell=False, reiter=False):
        if monocell==True:
            slaAlignment = paras[0].get('ALIGN')
        elif reiter ==True:
            slaAlignment = paras[0].get('ALIGN')
        else:
            slaAlignment = paras[v][0].get('ALIGN')
        if slaAlignment == None:
            slaAlignment = self.slaStyleDefault()
        pdfAlignment= Sla2pdfUtils.alignment(slaAlignment)
        return pdfAlignment

    def hexBorderColorFunc(self, borderColor):
        hexBorderColor = ColorDicTFull.colorDict[str(borderColor)][1]
        return hexBorderColor

    def foregroundFunc(self, itext):
        if self.version:
            textColor = itext.get('FCOLOR')
        else:
            textColor = itext.get('CCOLOR')
        foreground = colors.HexColor(ColorDicTFull.colorDict[str(textColor)][1])
        return foreground

    def backgroundFunc(self, pageObject):
        cellProperties = pageObject
        if cellProperties['cellBackground'] == str("None"):
            sfondo = "White"
        else:
            sfondo = cellProperties['cellBackground']
        background = colors.HexColor(ColorDicTFull.colorDict[str(sfondo)][1])
        return background

    def chFunc(self, text):
        itexts = text
        ch = ''
        if len(itexts)>=1:
            if len(itexts)>1:
                for itext in itexts:
                    chtmp = itext.get('CH')
                    ch = ch +" "+ chtmp
                itext = itexts[0]
            else:
                itext = itexts[0]
                ch = itext.get('CH')
        else:
            itext = None
        return [ch, itext]

    def slaStyleDefault(self):
        styleTag = self.document.findall('STYLE')[0]
        styleDefault = styleTag.get('ALIGN')
        return styleDefault

# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

import os

from reportlab.lib import colors, utils
from reportlab.platypus import Table, TableStyle,Frame
from reportlab.platypus import *

from reportlab.pdfgen.canvas import Canvas

#import xml.etree.cElementTree as ElementTree
try:
    from promogest import Environment
except:
    print "NESSUN ENV "

try:
    from promogest.lib.utils import pbar
except:
    pass

import Sla2pdfUtils
import ColorDicTFull
from SlaParser import SlaParser

class Sla2Pdf_ng(SlaParser):
    """ sla to pdf format translation """

    def __init__(self, pdfFolder=None, slaFileName = None, fileName= None,
                                                    slafile = None, pbar=None):
        """
        Build a template object based on the specified file-like
        object and sequence of objects
        """

        self.pdfFolder = pdfFolder
        self.slaFileName = slaFileName
        self.pbar = pbar
        SlaParser.__init__(self, slaFileName=slaFileName,
                                    pdfFolder=pdfFolder,
                                    slafile=slafile)
        self.document = None
#        self.version = self.scribusVersion()
        self.version = True
        self.numPages = len(self.slaPage())
#        self.translate()

    def drawImage(self,group=None, tabpro=None):
        """ Drawing an image """
        pfile = tabpro['pfile']
        celle = tabpro["cells"]
        (imgPath, imgFile) = os.path.split(pfile)
        #innerIterator = self.iterator
        width = [float(x.get("WIDTH")) for x in celle][0]
        height = [float(x.get("HEIGHT")) for x in celle][0]
        xPos = [float(x.get("XPOS")) for x in celle][0]
        yPos = [float(x.get("YPOS")) for x in celle][0]
#        print "IMAGE Path ", pfile
        img = None
        try:
            if os.path.exists(Environment.imagesDir + imgFile):
                img = utils.ImageReader(Environment.imagesDir + imgFile)
        except:
            if not imgPath:
                imgPath = os.path.expanduser('~') + os.sep
            else:
                imgPath = os.path.expanduser('~') + os.sep+imgPath +"/"
            if os.path.exists(imgPath +imgFile):
                img = utils.ImageReader(imgPath +imgFile)
        if img:
            self.canvas.drawImage(img,
                                xPos - self.pageProperties[self.pdfPage][9],
                                self.pageProperties[0][7] - yPos - height + self.pageProperties[self.pdfPage][10],
                                width=width,
                                height=height)
            self.canvas.saveState()
        else:
            from promogest.lib.utils import messageError
            messageError(msg="ATTENZIONE!!!\n L'immagine scelta come logo in dati azienda\n NON è stata trovata!")

    def drawTable(self, group=None, monocell=None, reiter = None, tabpro=None):
        """ Drawing a table """
        matrix = []
        lst = []
        matrix2 = []
        vector = []
        # Total of element's table
        n_cells = int(tabpro['n_cells'])
        columns = int(tabpro['columns'])
        rows = int(tabpro['rows'])
        celle = tabpro["cells"]
        widths = [float(x.get("WIDTH")) for x in celle]
        heights = [float(x.get("HEIGHT")) for x in celle]
        xpos = [float(x.get("XPOS")) for x in celle]
        ypos = [float(x.get("YPOS")) for x in celle]
        contColumns = 0
        ch = ''
        col = 0
        cycle = False
        vector = []
        alignment= None
        itexts = [x.findall("ITEXT") for x in celle]
        paras = [x.findall("para") for x in celle]
        trail = [x.findall("trail") for x in celle]
        stile = TableStyle([])
        stile.add('VALIGN',(0,0),(-1,-1),'TOP')
        if monocell==True:
            cells = 1
            columns=1
            rows = 1
        #print "CEEEEEEEEEEEEEELS", cells
        for v in range(0,n_cells):
            if v == 0:
                contRows = 0
                contColumns = 0
            elif columns==1:
                contColumns = -1
                contRows= int(v/columns)
            else:
                contRows= int(v/columns)
                contColumns = ((v)%columns)
#            print "VVVVVVVVVVVVV E CELLE", "celle", celle,"V:",v, "LEN DI CELLE",len(celle), "NCELLS", n_cells, group
            try:
                background = self.backgroundFunc(celle[v])# Finding background
            except Exception as e:
                Environment.pg2log.info("ERRORE NEL GRUPPO TABELLA"+ group + "ERRORE:" + str(e.args))
            hexBorderColor = self.hexBorderColorFunc(celle[v].get('PCOLOR2'))
            stile.add('ROWBACKGROUNDS', (contColumns,contRows),
                                (contColumns,contRows),
                                (background, background))
            cellpict = celle[v].get('PFILE')
            cellIMGHeight = celle[v].get('HEIGHT')
            cellIMGWidth = celle[v].get('WIDTH')
            bordoriga = False
            if (celle[v].get('BottomLine') == "1" and celle[v].get('TopLine') == "1" and\
                        celle[v].get('LeftLine') =="1" and celle[v].get('RightLine') == "1"):
                stile.add('BOX', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
                                hexBorderColor)
                bordoriga = True
            else:
                if celle[v].get('BottomLine') == "1":
                    stile.add('LINEBELOW', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
                                hexBorderColor)
                    bordoriga = True
                if celle[v].get('TopLine') == "1":
                    stile.add('LINEABOVE', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
                                hexBorderColor)
                    bordoriga = True
                if celle[v].get('LeftLine') == "1":
                    stile.add('LINEBEFORE', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
                                hexBorderColor)
                    bordoriga = True
                if celle[v].get('RightLine') == "1":
                    stile.add('LINEAFTER', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
                                hexBorderColor)
                    bordoriga = True
            if not bordoriga and str(celle[v].get('PCOLOR2')) != "None":
                stile.add('BOX', (contColumns,contRows),
                                (contColumns,contRows),
                                float(celle[v].get('PWIDTH')),
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

            actualPageObject = tabpro # Borders

            pdfAlignment = self.alignmentFunc(paras,v, monocell, trail=trail, reiter=reiter) #alignment
            stile.add('ALIGN', (contColumns,contRows),
                                (contColumns,contRows),
                                pdfAlignment)
            if itext != None:

                fontSize = self.fontSizeFunc(itext,v=v, trail=trail)# Font size
                stile.add('FONTSIZE', (contColumns,contRows),
                                    (contColumns,contRows),
                                    fontSize)

                fontName = self.fontNameFunc(itext,trail=trail) #  Font name
                stile.add('FONT', (contColumns,contRows),
                                    (contColumns,contRows),
                                    fontName)

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
        table=Table(matrix,style=stile,  colWidths=widths[:columns], rowHeights=heights[:rows])
        lst.append(table)
        # Effective table size
        sumRows = Sla2pdfUtils.sumRowsFunc(heights,rows)
        sumColumns = Sla2pdfUtils.sumColumnsFunc(widths,columns)
        f = Frame(x1=(xpos[0] - self.pageProperties[self.pdfPage][9]),
                    y1=(self.pageProperties[self.pdfPage][7] - ypos[0] - sumRows + self.pageProperties[self.pdfPage][10] - 12),
                    width=sumColumns,
                    height=(sumRows+12),
                    showBoundary=0)
        sumRows = sumColumns = 0
        f.addFromList(lst, self.canvas)
        reiter = False
        #self.canvas.saveState()


    def translate(self):
        # begin translate
        self.pageProperties = Sla2pdfUtils.pageProFunc(self.slaDocumentTag())
        self.canvas = Canvas(filename = self.slafile + '.pdf', pagesize=(self.pageProperties[0][8],self.pageProperties[0][7]))
        # Page's table
        reiter = False
        self.pdfPage = 0
        tablepropertys = self.findTablesProperties()
        iteratable = self.getIteratableGroups(tablepropertys)
        for self.pdfPage in xrange(0, self.numPages):
            for tableproperty in tablepropertys:
                for group in tableproperty.keys():
                    if self.pbar:
                        pbar(self.pbar,pulse=True,text="GEN STAMPA ATTENDERE 2 di 2")
                    tabpro = tableproperty[group]
                    try:
                        group= group.strip().split('%%%')[0]
                    except:
                        group= group.strip()
                    if group in iteratable:
                        colu = int(tabpro['columns'])
    #                    tabpro['iterproper'] = tabpro['parasobj'][colu:(colu*2)]
                        reiter = True
                    n_cells = int(tabpro['n_cells'])
                    # Closing pages (elements of the same page must be near)
                    if "noGroup" in group and tabpro["pfile"] != "" :
#                        print "IMMAGINEEEEEEEEEEEEEEE", group
                        self.drawImage(group=group, tabpro=tabpro) # IMMAGINE
                    elif "noGroup" in group  and tabpro["pfile"] == "":
#                        print "MONOCELLAAAAAAA", group
                        self.drawTable(group =group, monocell=True, tabpro=tabpro)# MONOCELLA
                    else:
#                        print "TABELLAAAAAAAA", group, reiter
                        self.drawTable(group =group, reiter = reiter, tabpro = tabpro) # TABELLA
            self.canvas.saveState()
            self.canvas.showPage()
        self.canvas.save()
        # temporary pdf file is removed immediately
#        filename = self.pdfFolder + self.pdfFileName + '.pdf'
        filename = self.slafile + '.pdf'

        f = file(filename, 'rb')
        result = f.read()
        f.close()
#        os.remove(filename)
        return result

    # ATTENZIONE !!!   this part above is for generic function.

    def fontSizeFunc(self, itext,v=None,trail=None):
        fontSize = "0"
        # Font size
        if self.version:
            try:
                fontSize = float(itext.get('FONTSIZE'))
            except:
                pass
        else:
            fontSize = float(itext.get('CSIZE'))
        if fontSize == "0":
            try:
                fontSize = float(trail[v][0].get('FONTSIZE'))
            except:
                pass
        if fontSize =="0":
            CHARSTYLE = self.document.findall('CHARSTYLE')[0]
            fontSize = float(CHARSTYLE.get('FONTSIZE'))
                #fontSize = "8"
        return fontSize

    def fontNameFunc(self, itext, monocell=False,v=None,trail=None):
        bold = False
        try:
            ch = itext.get('CH')
            if "<b>" in ch:
                bold=True
        except:
            bold= False
        if self.version:
            if bold:
                fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('FONT')+"-bold"))
            else:
                fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('FONT')))
        else:
            if bold:
                fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('CFONT')+"-bold"))
            else:
                fontName = Sla2pdfUtils.getPdfFontName(str(itext.get('CFONT')))
        return fontName

    def alignmentFunc(self,paras, v, monocell=False, reiter=False, trail=None):
        if monocell==True:
            try:
#                print "TRAIL DI MONOCELLA PER CURIOSI", trail
                slaAlignment = trail[0][0].get('ALIGN')
            except:
                slaAlignment = paras[0][0].get('ALIGN')
        elif reiter ==True:
#            print "TRAIL DEL REITER VEDIAMO UN PO?", trail[v][0].get('ALIGN')
            slaAlignment = trail[v][0].get('ALIGN')
#            if not slaAlignment:
#                slaAlignment = paras[0][0].get('ALIGN')
        else:
            try:
#
                slaAlignment = trail[v][0].get('ALIGN')
            except:
                slaAlignment = paras[v][0].get('ALIGN')
                if not slaAlignment:
#                    print "NON RIESCO AD ALLINEARE"
                    slaAlignment = None
        if not slaAlignment:
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
        cellProperties = pageObject.get('PCOLOR')
        if cellProperties == str("None"):
            sfondo = "White"
        else:
            sfondo = cellProperties
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
        ch = ch.replace("<b>","")
        ch = ch.replace("</b>","")
        return [ch, itext]

    def slaStyleDefault(self):
        styleTag = self.document.findall('STYLE')[0]
        styleDefault = styleTag.get('ALIGN')
        return styleDefault

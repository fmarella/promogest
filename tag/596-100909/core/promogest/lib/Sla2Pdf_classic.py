# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
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
import math
import datetime
from reportlab.lib import colors, utils
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
#from reportlab.lib.pagesizes import cm, inch, A4, landscape
from reportlab.pdfgen.canvas import Canvas
#from PIL import Image

##from elementtree import ElementTree
##from elementtree.ElementTree import *
#import cElementTree as ElementTree
import xml.etree.cElementTree as ElementTree
from promogest import Environment


# KNOWN BUGS
# ****************************************************************
# Fonts don't selectable
# Images: the position may be incorrect                     fixed
# Table's borderline, always present by default             fixed
# Double itexts or more, don't work (see also Paragraph)
# Tags live only in tables, at least 1x1
# Wrong tags break the program

# Fonts working
##const QString tmpf[] = {"/Courier", "/Courier-Bold", "/Courier-Oblique", "/Courier-BoldOblique",
##                        "/Helvetica", "/Helvetica-Bold", "/Helvetica-Oblique", "/Helvetica-BoldOblique",
##                        "/Times-Roman", "/Times-Bold", "/Times-Italic", "/Times-BoldItalic",
##                        "/ZapfDingbats", "/Symbol"};



class Sla2Pdf_classic(object):

    def __init__(self, slaFileName, pdfFolder, report=False):
        """
        Build a template object based on the specified file-like
        object and sequence of objects
        """

        self.slaFileName = slaFileName
        self.pdfFolder = pdfFolder
        self.pdfFileName = '_temp'
        self.slaTempFileName = '_temp.sla'
        self.formatFunctions = ['trunc','approx','itformat']
        self.timeTags = ['date','time','datetime']
        self.positionTags = ['first','last']
        self.pageTags = ['currentPage','totalPage']

        self.report = report
        self.cycle = 0


    def serialize(self, objects, dao):
        """ Model parsing, values substitution and pdf creation """
        self.objects = objects
        #~ print "[[[[[[[[[]]]]]]]]]]", objects
        result = None
        #try:
        self.dao =dao
        self.initialize()
        self.findTablesAndTags()
        self.findTablesProperties()
        self.getIteratableGroups()
        self.getPagesNumber()
        self.addEmptyPages()
        self.fillDocument()
        self.translate()
        #finally:

        # temporary pdf file is removed immediately
        filename = self.pdfFolder + self.pdfFileName + '.pdf'
        f = file(filename, 'rb')
        result = f.read()
        f.close()
        os.remove(filename)
        return result


    def initialize(self):
        """ Initial operations """
        # replacing scribus carriage return with \n
        f = file(self.slaFileName, 'rb')
        text = f.read()
        text = text.replace('&#x5;', '\\n')
        f.close()
        tempFile = self.pdfFolder + self.slaTempFileName
        f = file(tempFile, 'wb')
        f.write(text)
        f.close()
        self.doc = ElementTree.parse(tempFile)
        os.remove(tempFile)

        self.root = self.doc.getroot()    #<Element 'SCRIBUSUTF8NEW' at 0x24cf660>
        version = self.root.get('Version')
        if version == "1.3.4":
            self.version=True
        else:
            self.version = None

        self.document = self.root.findall('DOCUMENT')[0]   # <Element 'DOCUMENT' at 0x24dc2d0>
        self.pageObjects = self.document.findall('PAGEOBJECT')
        if self.version:
            self.defaultStyle = self.document.findall('STYLE')[0]
            self.defaultAlignment = self.defaultStyle.get('ALIGN')

        else:
            self.defaultAlignment = "0"
        #print "AAAAAAAAAAAAAAAAAAAAA self.defaultAlignment", self.defaultAlignment

    def findTablesAndTags(self):
        """ Creates associations between groups and tags """
        group = ''
        vector = []
        self.tablesTags = {}        # relation group -> tags
        self.tagsTables = {}        # relation tag -> group

        for pagObjAttr in self.pageObjects:
            isTableItem = (pagObjAttr.get('isTableItem') == "1")
            if not isTableItem:
                continue

            group = pagObjAttr.get('GROUPS')
            if group.replace(' ', '') == '':
                continue

            itexts = pagObjAttr.findall('ITEXT')
            ch = ''
            if self.tablesTags.has_key(group):
                vector = self.tablesTags[group]
            else:
                vector = []
            for i in itexts:
                ch = str(i.get('CH'))
                if ch.replace(' ', '') == '':
                    continue
                tags = self.findTags(ch)
                if tags is not None:
                    if tags not in vector:
                        vector.append(tags)

                    for k in tags.keys():
                        self.tagsTables[k] = group

            self.tablesTags[group] = vector


    def findTags(self, string):
        """ Isolating tags and functions applied to tags"""
        # RULES:
        # Tags must be divided by spaces
        # No spaces inside a tag
        # Parenthesis [] and () must be balanced
        #
        # EXAMPLES:
        # [[prova1(n)]]    [[itformat(prova2(n))]]    [[trunc(prova3,3)]]
        # [[last:approx(righe(n).prova4,4)]]    [[last:prova5]]    [[last:righe(n).prova6]]

        squareOpen = string.count('[')
        squaresOpen = string.count('[[')
        squareClose = string.count(']')
        squaresClose = string.count(']]')
        roundOpen = string.count('(')
        roundClose = string.count(')')
        chDict = {}

        # Syntax control
        if not ((squaresOpen == squareOpen/2) and (squareOpen%2 == 0) and
                (squaresClose == squareClose/2) and (squareClose%2 == 0) and
                (squaresOpen == squaresClose) and (roundOpen == roundClose)):
            print 'ERROR: Please check your tags!!'
            print string
            return None

        # Better choice to work with RE
        # wordList = re.findall(r'\b[\S]+\b',string)
        elements = string.split()

        # Finding Tags
        for element in elements:
            if not((element[:2] == '[[') and (element[-2:] == ']]')):
                continue

            position = ''
            function = ''
            tag = ''
            parameter = ''

            # Finding position
            indexPosition = element.find(':')
            if indexPosition != -1:
                position = element[2:indexPosition]

            # Analyzing tag
            if element.count('(') != element.count(')'):
                continue

            indexBeginFunction = element.find('(')
            indexEndFunction = element.rfind(')')
            isIterator = element.find('(n)')
            if (((isIterator == -1) or ((isIterator != -1) and (isIterator != indexBeginFunction))) and
                (indexBeginFunction != -1) and (indexEndFunction != -1)):
                    # Finding function
                if indexPosition != -1:
                    function = element[indexPosition+1:indexBeginFunction]
                else:
                    function = element[2:indexBeginFunction]

                # Finding tag and parameter
                indexParameter = element.find(',')
                if indexParameter != -1:
                    parameter = element[indexParameter+1:indexEndFunction]
                    tag = element[indexBeginFunction+1:indexParameter]
                else:
                    tag = element[indexBeginFunction+1:indexEndFunction]

            # Finding tag
            else:
                if indexPosition != -1:
                    tag = element[indexPosition+1:-2]
                else:
                    tag = element[2:-2]
            #qui compone il tag con i vai elementi
            chDict[tag] = {'position': position,
                           'function': function,
                           'parameter': parameter,
                           'completeTag': element}

        if chDict != {}:
            return chDict
        else:
            return None


    def findTablesProperties(self):
        """ Finding tables dimensions and contents """
        self.tablesProperties = {}
        index = 0
        while index < len(self.pageObjects):
            p = self.pageObjects[index]

            isTableItem = (p.get('isTableItem') == "1")
            if not isTableItem:
                index += 1
                continue

            group = p.get('GROUPS')
            if group.replace(' ', '') == '':
                index += 1
                continue

            pfile = p.get('PFILE')
            if pfile != '':
                index += 1
                continue

            actualGroup = group
            cells = 0
            columns = 0
            maxCells = cells
            maxColumns = columns
            numCol = 0
            innerIndex = index
            while (actualGroup == group) and (innerIndex < len(self.pageObjects)):
                ip = self.pageObjects[innerIndex]
                actualGroup = ip.get('GROUPS')
                if actualGroup == group:
                    cells = int(ip.get('OwnLINK'))
                    if cells > maxCells:
                        maxCells = cells

                    if not(maxColumns > 0):
                        columns = ip.get('RightLINK')
                        if columns != '-1':
                            numCol += 1
                        else:
                            maxColumns = numCol

                innerIndex += 1
            cells = int(maxCells) + 1 - int(p.get('OwnLINK'))
            columns = int(maxColumns) + 1
            rows = cells / columns
            self.tablesProperties[group] = {'cells': cells,
                                            'rows': rows,
                                            'columns': columns,
                                            'itexts': list({} for i in range(0, columns)),
                                            'counters': list(-1 for i in range(0, columns))}
            index += cells


    def getIteratableGroups(self):
        """ Gets tables where we have to iterate """
        self.iteratableGroups = []
        for group in self.tablesTags.keys():
            for tagDict in self.tablesTags[group]:
                for tag in tagDict.keys():
                    indexN = tag.find('(n)')
                    if (indexN != -1):
                        if group not in self.iteratableGroups:
                            self.iteratableGroups.append(group)


    def getPagesNumber(self):
        """ Gets number of pages to build """
        self.pagesNumber = pages = 1
        for group in self.tablesTags.keys():
            for tagDict in self.tablesTags[group]:
                for tag in tagDict.keys():
                    indexN = tag.find('(n)')
                    if (indexN != -1):
                        indexNP = tag.find('(n).')
                        if (indexNP != -1):
                            arrayName = tag[:indexNP]
                            valuesNumber = len(self.objects[self.cycle][arrayName])
                            rowsNumber = self.tablesProperties[group]['rows'] - 1
                        else:
                            valuesNumber = len(self.objects)
                            rowsNumber = self.tablesProperties[group]['rows'] - 1

                        pages = int(math.ceil(float(valuesNumber) / float(rowsNumber)))
                        if pages > self.pagesNumber:
                            self.pagesNumber = pages


    def addEmptyPages(self):
        """ Creates new pages based on the model's first page """

        def getTagToPrint(string, increment=True):
            # valuation of tags to resolve
            if tags[k]['position'] in self.positionTags:
                if (((tags[k]['position'] == 'first') and (pageNumber == 1)) or
                    ((tags[k]['position'] == 'last') and (pageNumber == self.pagesNumber))):
                    if (k.find('(n)') > -1):
                        if increment:
                            self.tablesProperties[group]['counters'][column - 1] += 1
                        counter = self.tablesProperties[group]['counters'][column - 1]
                        tag = tags[k]['completeTag']
                        tag = tag + ('<<%d>>' % counter)
                        string = string.replace(tags[k]['completeTag'], tag)
                    else:
                        string = tags[k]['completeTag']
                else:
                    string = ''
            else:
                if k.find('(n)') > -1:
                    if increment:
                        self.tablesProperties[group]['counters'][column - 1] += 1
                    counter = self.tablesProperties[group]['counters'][column - 1]
                    tag = tags[k]['completeTag']
                    tag = tag + ('<<%d>>' % counter)
                    string = string.replace(tags[k]['completeTag'], tag)
                else:
                    pass
            return string

        # Index of first tag 'PAGE'
        childrens = self.document.getchildren()
        index = ''
        for index in range(0, len(childrens)):
            childrens[index] = str(childrens[index])
            s = childrens[index].find("<Element 'PAGE' at ")
            if s!= -1:
                break

        # Duplicate page's information
        numPages = self.document.findall('PAGE')
        for i in range(0, self.pagesNumber - 1):
            attributes = numPages[0].items()
            dictionary =  {}
            for j in range(0, len(attributes)):
                dictionary[attributes[j][0]] = attributes[j][1]
            app = numPages[0].makeelement('PAGE', dictionary)
            self.document.insert(index, app)

        # Processing page's information
        numPages = self.document.findall('PAGE')
        pageHeight = numPages[0].get('PAGEHEIGHT')
        borderTop = numPages[0].get('BORDERTOP')
        for i in range(1, len(numPages)):
            # Number page
            numPages[i].set('NUM', str(i))
            # Coordinates
            lastPageYPos = numPages[i-1].get('PAGEYPOS')
            numPages[i].set('PAGEYPOS', str(float(pageHeight) + float(borderTop) + float(lastPageYPos)))

        # Duplicating all elements, page by page
        for j in range(1, len(numPages)):
            for pageObject in self.pageObjects:
                # Creating dictionary attributes pageobject
                attributes = pageObject.items()
                dictionary = {}
                for k in range(0, len(attributes)):
                    dictionary[attributes[k][0]] = attributes[k][1]

                # Applying attributes
                app = pageObject.makeelement('PAGEOBJECT', dictionary)

                # Creating dictionary attributes itext of the pageobject
                itexts = pageObject.findall('ITEXT')
                for itext in itexts:
                    attributes = itext.items()
                    dictionary = {}
                    for kk in range(0, len(attributes)):
                        dictionary[attributes[kk][0]] = attributes[kk][1]
                    # Applying attributes
                    ElementTree.SubElement(app, 'ITEXT', dictionary)

                # Number page
                app.set('OwnPage', str(j))
                # Coordinates
                initial = app.get('YPOS')
                app.set('YPOS', str( j * (float(pageHeight) + float(borderTop)) + float(initial)))
                self.document.append(app)

        # Duplicating tags
        self.pageObjects = self.document.findall('PAGEOBJECT')
        for pageObject in self.pageObjects:
            isTableItem = pageObject.get('isTableItem') == "1"
            group = pageObject.get('GROUPS')
            pageNumber = int(pageObject.get('OwnPage')) + 1
            if isTableItem and (group in self.iteratableGroups):
                itexts = pageObject.findall('ITEXT')
                cell = int(pageObject.get('OwnLINK')) + 1
                columns = self.tablesProperties[group]['columns']
                row = (cell / columns) + 1
                column = (cell % columns)
                if not(len(itexts) > 0):
                    # first row of the table (with itext)
                    itext = self.tablesProperties[group]['itexts'][column - 1].copy()
                    if itext == {}:
                        continue
                    ch = str(itext['CH'])
                    tags = self.findTags(ch)
                    if tags is None:
                        continue
                    tmp = ch
                    tagsKeys = tags.keys()
                    increment = True
                    for k in tagsKeys:
                        if k.replace(' ', '') == '':
                            continue
                        if k.find('(n)') > -1:
                            tmp = getTagToPrint(tmp, increment)
                            increment = False
                    itext['CH'] = tmp
                    ElementTree.SubElement(pageObject, 'ITEXT', itext)
                else:
                    # next rows of the table (without itext)
                    itext = itexts[0]
                    ch = str(itext.get('CH'))
                    tags = self.findTags(ch)
                    if tags is not None:
                        tmp = ch
                        tagsKeys = tags.keys()
                        increment = True
                        for k in tagsKeys:
                            if k.replace(' ', '') == '':
                                continue
                            if k.find('(n)') > -1:
                                if self.tablesProperties[group]['itexts'][column - 1] == {}:
                                    self.tablesProperties[group]['itexts'][column - 1] = dict([attribute[0], attribute[1]] for attribute in itext.items())
                                tmp = getTagToPrint(tmp, increment)
                                increment = False
                        itext.set('CH', tmp)
            else:
                # cell text
                itexts = pageObject.findall('ITEXT')
                if len(itexts) > 0:
                    itext = itexts[0]
                    ch = str(itext.get('CH'))
                    tags = self.findTags(ch)
                    if tags is not None:
                        tmp = ch
                        tagsKeys = tags.keys()
                        increment = True
                        for k in tagsKeys:
                            if k.replace(' ', '') == '':
                                continue
                            tmp = getTagToPrint(tmp, increment)
                            increment = False
                        itext.set('CH', tmp)

        #self.doc.write('__temp.sla')


    def fillDocument(self):
        """ Replacing tags with real values """
        self.pageObjects = self.document.findall('PAGEOBJECT')
        iterator = 0
        while iterator < len(self.pageObjects):
            pageObject = self.pageObjects[iterator]
            isTableItem = pageObject.get('isTableItem')
            pageNumber = int(pageObject.get('OwnPage')) + 1
            group = pageObject.get('GROUPS')
            pfile = pageObject.get('PFILE')
            actualGroup = group

            if (pfile != ''):
                iterator += 1
                continue

            if actualGroup not in self.iteratableGroups:
                # Replacing non-iterator tags
                itexts = pageObject.findall('ITEXT')
                for itext in itexts:
                    ch = str(itext.get('CH'))
                    tags = self.findTags(ch)
                    if tags is not None:
                        tagsKeys = tags.keys()
                        for k in tagsKeys:
                            if k.replace(' ', '') == '':
                                continue

                            try:
                                resolvedTag = ''

                                function = tags[k]['function']
                                parameter = tags[k]['parameter']

                                if k == 'currentPage':
                                    value = pageNumber
                                elif k == 'totalPage':
                                    value = self.pagesNumber
                                elif k in self.timeTags:
                                    value = self.getNowValue(k)
                                else:
                                    if self.cycle <= (len(self.objects) - 1):
                                        #exec "value = self.dao."+k
                                        value = self.objects[self.cycle][k] or ''
                                    else:
                                        value = ''

                                # Function
                                if function in self.formatFunctions:
                                    resolvedTag = self.callFunction(function, value, parameter)
                                else:
                                    resolvedTag = str(value)

                                ch = ch.replace(tags[k]['completeTag'], resolvedTag)

                                # Save itext
                                itext.set('CH', ch)
                            except:
                                print "bad tag will be visible on the generated pdf"
                                #pass

            else:
                if isTableItem != '1':
                    iterator += 1
                    continue

                itexts = pageObject.findall('ITEXT')
                for itext in itexts:
                    ch = str(itext.get('CH'))
                    if (ch.find('<<') > -1) and (ch.find('>>') > -1):
                        while (ch.find('<<') > -1) and (ch.find('>>') > -1):
                            arrayIndex = int(ch[ch.find('<<')+2:ch.find('>>')])
                            ch = ch.replace(('<<%d>>' % arrayIndex), '')
                    else:
                        arrayIndex = -1
                    tags = self.findTags(ch)
                    if tags is not None:
                        tagsKeys = tags.keys()
                        for k in tagsKeys:
                            if k.replace(' ', '') == '':
                                continue

                            try:
                                resolvedTag = ''

                                function = tags[k]['function']
                                parameter = tags[k]['parameter']

                                if k == 'currentPage':
                                    value = pageNumber
                                elif k == 'totalPage':
                                    value = self.pagesNumber
                                elif k in self.timeTags:
                                    value = self.getNowValue(k)
                                else:
                                    indexN = k.find('(n)')
                                    if (indexN != -1):
                                        indexNP = k.find('(n).')
                                        if (indexNP != -1):
                                            arrayName = k[:indexNP]
                                            tagName = k[indexNP+4:]
                                            if self.cycle <= (len(self.objects) - 1):
                                                if arrayIndex <= (len(self.objects[self.cycle][arrayName]) - 1):
                                                    arraySource = self.objects[self.cycle][arrayName][arrayIndex]
                                                    value = arraySource[tagName] or ''
                                                else:
                                                    value = ''
                                            else:
                                                value = ''
                                        else:
                                            tagName = k[:indexN]
                                            if arrayIndex <= (len(self.objects) - 1):
                                                arraySource = self.objects[arrayIndex]
                                                value = arraySource[tagName] or ''
                                            else:
                                                value = ''
                                    else:
                                        if self.cycle <= (len(self.objects) - 1):
                                            value = self.objects[self.cycle][k] or ''
                                        else:
                                            value = ''

                                # Function
                                if function in self.formatFunctions:
                                    resolvedTag = self.callFunction(function, value, parameter)
                                else:
                                    resolvedTag = str(value)

                                ch = ch.replace(tags[k]['completeTag'], resolvedTag)

                                # Save itext
                                itext.set('CH', ch)
                            except:
                                # bad tag will be visible on the generated pdf
                                pass

            iterator += 1

        #self.doc.write('___temp.sla')


    def translate(self):
        """ sla to pdf format translation """

        def getPdfFontName(font=None):
            """ Trying to resolve font name """
            boldStr = 'BOLD'
            italicStr = 'ITALIC'
            obliqueStr = 'OBLIQUE'
            fontStr = font.upper()
            if 'COURIER' in fontStr:
                if boldStr in fontStr and obliqueStr in fontStr:
                    fontName = 'Courier-BoldOblique'
                elif boldStr in fontStr:
                    fontName = 'Courier-Bold'
                elif obliqueStr in fontStr:
                    fontName = 'Courier-Oblique'
                else:
                    fontName = 'Courier'
            elif 'HELVETICA' in fontStr:
                if boldStr in fontStr and obliqueStr in fontStr:
                    fontName = 'Helvetica-BoldOblique'
                elif boldStr in fontStr:
                    fontName = 'Helvetica-Bold'
                elif obliqueStr in fontStr:
                    fontName = 'Helvetica-Oblique'
                else:
                    fontName = 'Helvetica'
            else:
                if boldStr in fontStr and (obliqueStr in fontStr or italicStr in fontStr):
                    fontName = 'Times-BoldItalic'
                elif boldStr in fontStr:
                    fontName = 'Times-Bold'
                elif obliqueStr in fontStr or italicStr in fontStr:
                    fontName = 'Times-Italic'
                else:
                    fontName = 'Times-Roman'

            return fontName


        def drawImage(width, height):
            """ Drawing an image """
            (imgPath, imgFile) = os.path.split(self.pfile)
            img = utils.ImageReader(Environment.imagesDir + imgFile)
            self.canvas.drawImage(img,
                                xPos - self.pageProperties[self.pdfPage][9],
                                self.pageProperties[0][7] - yPos - height + self.pageProperties[self.pdfPage][10],
                                width=width,
                                height=height)
            self.canvas.saveState()


        def drawCell():
            """ Drawing a cell text """
            # Finding background
            cellBackground = self.pageObject.get('PCOLOR')
            if self.colorList.has_key(cellBackground):
                try:
                    hexCellColor = self.colorList[cellBackground]
                    background = colors.HexColor(str(hexCellColor))
                except:
                    background = colors.HexColor('#ffffff')
            else:
                background = colors.HexColor('#ffffff')
            stile = TableStyle([('ROWBACKGROUNDS', (0,0), (0,0), (background, background))])

            # Borders
            bottomLine = int(self.pageObject.get('BottomLine'))
            topLine = int(self.pageObject.get('TopLine'))
            leftLine = int(self.pageObject.get('LeftLine'))
            rightLine = int(self.pageObject.get('RightLine'))
            lineWidth = float(self.pageObject.get('PWIDTH'))
            borderColor = self.pageObject.get('PCOLOR2')
            alignment = " "
            # Finding value and cell's style
            if self.version:
                paras = self.pageObject.findall('para')
            itexts = self.pageObject.findall('ITEXT')
            ch = ''
            matrix = []
            if len(itexts)>=1:
                if len(itexts)>1:
                    for itext in itexts:
                        chtmp = itext.get('CH')
                        ch = ch +" "+ chtmp
                    itext = itexts[0]
                else:
                    itext = itexts[0]
                    ch = itext.get('CH')
                if self.version:
                    try:
                        alignment = paras[0].get('ALIGN')
                    except:
                        alignment = "0"
                else:
                    alignment = itext.get('CAB')
                if alignment == None:
                    alignment = self.defaultAlignment
                if alignment == '0':
                    alignment = 'LEFT'
                elif alignment == '1':
                    alignment = 'CENTER'
                elif alignment == '2':
                    alignment = 'RIGHT'
                else:
                    alignment = "LEFT"
                stile.add('ALIGN', (0,0), (0,0), alignment)

                # Font Name
                if self.version:
                    fontName = getPdfFontName(str(itext.get('FONT')))
                else:
                    fontName = getPdfFontName(str(itext.get('CFONT')))
                stile.add('FONT', (0,0), (0,0), fontName)

                # Font size
                if self.version:
                    fontSize = float(itext.get('FONTSIZE'))
                else:
                    fontSize = float(itext.get('CSIZE'))
                stile.add('FONTSIZE', (0,0), (0,0), fontSize)

                # Hex color
                if self.version:
                    textColor = itext.get('FCOLOR')
                else:
                    textColor = itext.get('CCOLOR')
                if self.colorList.has_key(textColor):
                    try:
                        hexTextColor = self.colorList[textColor]
                        foreground = colors.HexColor(str(hexTextColor))
                    except:
                        foreground = colors.HexColor('#000000')
                else:
                    foreground = colors.HexColor('#000000')
                stile.add('TEXTCOLOR', (0,0), (0,0), foreground)

                # Applying attributes
                if self.colorList.has_key(borderColor):
                    try:
                        hexBorderColor = self.colorList[borderColor]
                    except:
                        hexBorderColor = '#000000'
                else:
                    hexBorderColor = '#000000'
                stile.add('VALIGN',(0,0),(-1,-1),'TOP')
                if (bottomLine == 1 and topLine == 1 and leftLine == 1 and rightLine == 1) or (lineWidth > 1):
                    stile.add('BOX', (0,0), (-1,-1), lineWidth, hexBorderColor)
                else:
                    if bottomLine == 1:
                        stile.add('LINEBELOW', (0,0), (-1,-1), lineWidth, hexBorderColor)
                    elif topLine == 1:
                        stile.add('LINEABOVE', (0,0), (-1,-1), lineWidth, hexBorderColor)
                    if leftLine == 1:
                        stile.add('LINEBEFORE', (0,0), (-1,-1), lineWidth, hexBorderColor)
                    if rightLine == 1:
                        stile.add('LINEAFTER', (0,0), (-1,-1), lineWidth, hexBorderColor)

                    # Creating and filling
                    data = []
                    data.append(self.makeParagraphs(ch, background, foreground, alignment, fontName, fontSize))
                    matrix.append(data)
            if len(matrix) > 0:
                table=Table(data=matrix, colWidths=width, rowHeights=height, style=stile)

                # Adding cell to the frame and save it
                lst = []
                lst.append(table)
                f = Frame(x1=(xPos - self.pageProperties[self.pdfPage][9]),
                          y1=(self.pageProperties[0][7] - yPos - height + self.pageProperties[self.pdfPage][10] - 12),
                          width=width,
                          height=(height + 12),
                          showBoundary=0)
                f.addFromList(lst, self.canvas)
                self.canvas.saveState()


        def drawTable():
            """ Drawing a table """
            matrix = []
            vector = []

            # Total of element's table
            actualGroup = self.group
            cells = int(self.tablesProperties[actualGroup]['cells'])
            columns = int(self.tablesProperties[actualGroup]['columns'])
            rows = int(self.tablesProperties[actualGroup]['rows'])

            # Finding cell size
            cont = 0
            widths = []
            heights = []
            innerIterator = self.iterator
            xpos = float(self.pageObjects[innerIterator].get('XPOS'))
            ypos = float(self.pageObjects[innerIterator].get('YPOS'))
            while actualGroup == self.group and innerIterator < len(self.pageObjects):
                cont += 1
                actualGroup = self.pageObjects[innerIterator].get('GROUPS')
                if actualGroup == self.group:
                    width = float(self.pageObjects[innerIterator].get('WIDTH'))
                    widths.append(width)
                    if cont == columns:
                        height = float(self.pageObjects[innerIterator].get('HEIGHT'))
                        heights.append(height)
                        cont = 0
                    innerIterator += 1

            # General table style (always the same!!!)
            stile = TableStyle([])
            stile.add('VALIGN',(0,0),(-1,-1),'TOP')

            # Applying stile, font and color for every cell
            contColumns = -1
            contRows = 0
            ch = ''
            cont = 0
            vector = []
            actualGroup = self.group
            innerIterator = self.iterator
            alignment = " "

            while actualGroup == self.group and innerIterator < len(self.pageObjects):
                actualGroup = self.pageObjects[innerIterator].get('GROUPS')
                actualPage = int(self.pageObjects[innerIterator].get('OwnPage'))

                if actualPage != self.pdfPage:
                    innerIterator += 1
                    continue

                if actualGroup == self.group:
                    # Conversion between index - row/column
                    contColumns += 1
                    if contColumns == columns:
                        contColumns = 0
                        contRows += 1

                    # Finding background
                    cellBackground = self.pageObjects[innerIterator].get('PCOLOR')
                    if self.colorList.has_key(cellBackground):
                        try:
                            hexColor = self.colorList[cellBackground]
                            background = colors.HexColor(str(hexColor))
                        except:
                            background = colors.HexColor('#ffffff')
                    else:
                        background = colors.HexColor('#ffffff')
                    stile.add('ROWBACKGROUNDS', (contColumns,contRows), (contColumns,contRows), (background, background))
                    itexts = self.pageObjects[innerIterator].findall('ITEXT')
                    put = False
                    if self.version:
                        paras = self.pageObjects[innerIterator].findall('para')
                    if len(itexts)>=1:
                            if len(itexts)>1:
                                for itext in itexts:
                                    chtmp = itext.get('CH')
                                    ch = ch +" "+ chtmp
                                itext = itexts[0]

                            else:
                                itext = itexts[0]
                                ch = itext.get('CH')
                            if self.version:
                                #try:
                                alignment = paras[0].get('ALIGN')
                                #except:
                                    #alignment = "0"
                            else:
                                alignment = itext.get('CAB')
                            if alignment == None:
                                alignment = self.defaultAlignment
                            if alignment == '0':
                                alignment = 'LEFT'
                            elif alignment == '1':
                                alignment = 'CENTER'
                            elif alignment == '2':
                                alignment = 'RIGHT'
                            else:
                                alignment = "LEFT"
                            stile.add('ALIGN', (contColumns,contRows), (contColumns,contRows), alignment)

                            # Font name
                            if self.version:
                                fontName = getPdfFontName(str(itext.get('FONT')))
                            else:
                                fontName = getPdfFontName(str(itext.get('CFONT')))
                            stile.add('FONT', (contColumns,contRows), (contColumns,contRows), fontName)

                            # Font size
                            if self.version:
                                try:
                                    print "TEEEEE", itext.get('FONTSIZE')
                                    fontSize = float(itext.get('FONTSIZE'))
                                except:
                                    fontSize = float(10)
                            else:
                                fontSize = float(itext.get('CSIZE'))

                            stile.add('FONTSIZE', (contColumns,contRows), (contColumns,contRows), fontSize)

                            # Hex color
                            textColor = itext.get('FCOLOR')
                            if self.colorList.has_key(textColor):
                                try:
                                    hexColor = self.colorList[textColor]
                                    foreground = colors.HexColor(str(hexColor))
                                except:
                                    foreground = colors.HexColor('#000000')
                            else:
                                foreground = colors.HexColor('#000000')
                            stile.add('TEXTCOLOR', (contColumns,contRows), (contColumns,contRows), foreground)

                            # Borders
                            actualPageObject = self.pageObjects[innerIterator]
                            bottomLine = int(actualPageObject.get('BottomLine'))
                            topLine = int(actualPageObject.get('TopLine'))
                            leftLine = int(actualPageObject.get('LeftLine'))
                            rightLine = int(actualPageObject.get('RightLine'))
                            lineWidth = float(actualPageObject.get('PWIDTH'))

                            borderColor = actualPageObject.get('PCOLOR2')
                            if self.colorList.has_key(borderColor):
                                try:
                                    hexBorderColor = self.colorList[borderColor]
                                except:
                                    hexBorderColor = '#000000'
                            else:
                                hexBorderColor = '#000000'

                            if (bottomLine == 1 and topLine == 1 and leftLine == 1 and rightLine == 1):
                                stile.add('BOX', (contColumns,contRows), (contColumns,contRows), lineWidth, hexBorderColor)
                            else:
                                if bottomLine == 1:
                                    stile.add('LINEBELOW', (contColumns,contRows), (contColumns,contRows), lineWidth, hexBorderColor)
                                elif topLine == 1:
                                    stile.add('LINEABOVE', (contColumns,contRows), (contColumns,contRows), lineWidth, hexBorderColor)
                                if leftLine == 1:
                                    stile.add('LINEBEFORE', (contColumns,contRows), (contColumns,contRows), lineWidth, hexBorderColor)
                                if rightLine == 1:
                                    stile.add('LINEAFTER', (contColumns,contRows), (contColumns,contRows), lineWidth, hexBorderColor)

                            vector.append(self.makeParagraphs(ch, background, foreground, alignment, fontName, fontSize))
                            put = True
                    if put == False:
                        vector.append('')
                    cont += 1
                    if cont == columns:
                        #print "VECTORRRR ", vector
                        matrix.append(vector)
                        vector = []
                        cont = 0
                    test = None
                    innerIterator += 1

            # Creating and filling table
            #print "matrix", matrix
            table=Table(matrix, style=stile, colWidths=widths[:columns], rowHeights=heights[:rows])

            # Adding cell to the frame and save it
            lst = []
            lst.append(table)

            # Effective table size
            sumRows = 0
            sumColumns = 0
            for i in range(0, rows):
                sumRows += heights[i]
            for i in range(0, columns):
                sumColumns += widths[i]

            f = Frame(x1=(xpos - self.pageProperties[self.pdfPage][9]),
                      y1=(self.pageProperties[self.pdfPage][7] - ypos - sumRows + self.pageProperties[self.pdfPage][10] - 12),
                      width=sumColumns,
                      height=(sumRows+12),
                      showBoundary=0)
            f.addFromList(lst, self.canvas)
            self.canvas.saveState()

            self.iterator += cells - 1



        # begin translate
        self.pageObjects = self.document.findall('PAGEOBJECT')
        self.colorList = {}
        self.pageProperties = []

        # Color's table
        docColor = self.document.findall('COLOR')
        for c in docColor:
            rgbColor = c.get('RGB')
            nameColor =  c.get('NAME')
            self.colorList[nameColor] = rgbColor

        # Page's table
        numPages = self.document.findall('PAGE')
        for n in numPages:
            size = n.get('SIZE')
            num  = int(n.get('NUM')) + 1
            borderTop = float(n.get('BORDERTOP'))
            borderBottom = float(n.get('BORDERBOTTOM'))
            borderRight = float(n.get('BORDERRIGHT'))
            borderLeft = float(n.get('BORDERLEFT'))
            orientation = int(n.get('Orientation'))
            pageHeight = float(n.get('PAGEHEIGHT'))
            pageWidth = float(n.get('PAGEWIDTH'))
            pageXPos = float(n.get('PAGEXPOS'))
            pageYPos = float(n.get('PAGEYPOS'))
            self.pageProperties.append([size, num,
                                        borderTop, borderBottom, borderRight, borderLeft,
                                        orientation, pageHeight, pageWidth, pageXPos, pageYPos])

        self.canvas = Canvas(filename = self.pdfFolder + self.pdfFileName + '.pdf', pagesize=(pageWidth, pageHeight))

        # Analyzing elements
        self.pdfPage = 0
        self.iterator = 0
        while self.iterator < len(self.pageObjects):

            self.pageObject = self.pageObjects[self.iterator]
            width = float(self.pageObject.get('WIDTH'))
            height = float(self.pageObject.get('HEIGHT'))
            xPos = float(self.pageObject.get('XPOS'))
            yPos = float(self.pageObject.get('YPOS'))

            # Closing pages (elements of the same page must be near)
            docPage = int(self.pageObject.get('OwnPage'))
            for e in range(0, docPage - self.pdfPage):
                self.canvas.saveState()
                self.canvas.showPage()
            self.pdfPage = docPage

            # Checking object type: (0)cell - (1)table - (2)image
            isTableItem = self.pageObject.get('isTableItem')
            self.group = self.pageObject.get('GROUPS')
            self.pfile = self.pageObject.get('PFILE')

            if self.pfile != '':
                width = float(self.pageObject.get('WIDTH'))
                height = float(self.pageObject.get('HEIGHT'))

                drawImage(width, height)
            elif ((self.pfile == '') and (isTableItem == '1')):
                drawTable()
            elif ((self.pfile == '') and (isTableItem == '0')):
                drawCell()

            self.iterator += 1

        self.canvas.save()


    def makeParagraphs(self, text, background, foreground, alignment, fontName, fontSize):
        """Convert plain text into a list of paragraphs."""
        if (text == '') or ('\\n' not in text):
            return text

        if alignment == 'CENTER':
            alignment = TA_CENTER
        elif alignment == 'RIGHT':
            alignment = TA_RIGHT
        else:
            alignment = TA_LEFT
        style = ParagraphStyle(name='Normal',
                               fontName=fontName,
                               fontSize=fontSize,
                               alignment=alignment,
                               backColor=background,
                               textColor=foreground)
        lines = text.split("\\n")
        retval = [Paragraph(line[:6]=='<para>' and line or ('<para>%s</para>' % line), style) for line in lines]
        return retval


    def callFunction(self, functionName, value=None, parameter=None):
        """
        Call a function by its functionName
        """
        value = value or ''
        parameter = parameter or ''

        if functionName == 'trunc':
            if value == '' or parameter == '':
                return ''
            else:
                return self.truncValue(value, int(parameter))
        elif functionName == 'approx':
            if value == '' or parameter == '':
                return ''
            else:
                return self.approxValue(value, int(parameter))
        elif functionName == 'itformat':
            if value == '':
                return ''
            else:
                return self.itformatValue(value)
        else:
            return ''


    def truncValue(self, value, length):
        """
        Trunc the length of the element
        """
        return str(value[0:length])


    def approxValue(self, value, decimals):
        """
        Approximate the floating point values of the element with the
        given number of decimals
        """
        format = '%%.%df' % decimals

        return ((value != '' and value is not None) and (format % (value or 0.0)) or '')


    def itformatValue(self, value):
        """
        Convert the dates of the element into strings with italian
        datetime format
        """
        if isinstance(value, datetime.datetime):
            return value.strftime('%d/%m/%Y, ore %H:%M')
        elif isinstance(value, datetime.date):
            return value.strftime('%d/%m/%Y')
        elif isinstance(value, datetime.time):
            return value.strftime('%H:%M')


    def getNowValue(self, tag):
        """ Returns formatted now value """
        if tag == 'date':
            return datetime.datetime.now().strftime('%d/%m/%Y')
        elif tag == 'time':
            return datetime.datetime.now().strftime('%H:%M')
        else:
            return datetime.datetime.now().strftime('%d/%m/%Y  %H:%M')


    def scontiSequenceValues(self, sequence):
        """
        Convert a sequence of sequences of "Sconto" DAOs into a sequence
        of human-readable strings
        """
        def _sconto2str(sconto):
            if sconto == '':
                return ''

            sym = ''
            if sconto.tipo_sconto == 'valore':
                sym = u'E' # FIXME: put Euro symbol here
            elif sconto.tipo_sconto == 'percentuale':
                sym = '%'
            return '%.2f %s' % (sconto.valore, sym)

        def _reduceSconto(sconto1, sconto2):
            str1 = ''
            if type(sconto1) is type('') or type(sconto1) is type(u''):
                str1 = sconto1
            else:
                str1 = _sconto2str(sconto1)

            str2 = _sconto2str(sconto2)

            return str1 + ' + ' + str2

        if len(sequence) == 0:
            return []
        else:
            return [((len(sconti) > 1 and reduce(_reduceSconto, sconti))
                    or (len(sconti) == 1 and _sconto2str(sconti[0]))
                    or '')
                    for sconti in sequence]


    def cancelOperation(self):
        """
        Cancel current operation (i.e. make the computation stop as
        soon as possible, e.g. when executed in a parallel thread)
        """
        pass

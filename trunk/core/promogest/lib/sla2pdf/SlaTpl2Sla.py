# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>


import sys
import os
import math
import datetime
import time
from reportlab.lib import colors, utils
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import cm, inch, A4, landscape
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
import xml.etree.cElementTree as ElementTree
from promogest import Environment
import Sla2pdfUtils
from SlaParser import SlaParser


class SlaTpl2Sla(SlaParser):
    """
    Build a template object based on the specified file-like
    object and sequence of objects
    """

    def __init__(self,slafile=None,label=None, report=None, objects=None,
                    daos=None, slaFileName=None, pdfFolder=None, classic=None, template_file=None):

        #self.pdfFileName = '_temp'
        #self.slaTempFileName = '_temp.sla'
        self.slaFileName = slaFileName
        self.report = report
        self.classic = classic
        self.template_file = template_file
        SlaParser.__init__(self, slaFileName=slaFileName,
                                    pdfFolder=pdfFolder,
                                    slafile=slafile)
        self.objects = objects
        self.label = label
        self.formatFunctions = ['trunc','approx','itformat','itformatdataora','itformatdata', 'bcview']
        self.timeTags = ['date','time','datetime']
        self.positionTags = ['first','last']
        self.pageTags = ['currentPage','totalPage']
        self.cycle = 0
        self.findTablesAndTags()
        self.tableProperties = self.findTablesProperties()
        self.getIteratableGroups()
        self.getPagesNumber()
        if self.label and self.classic:
            self.duplicateElementLabel()
        self.addEmptyPages()
        self.fillDocument()

    def toPdf(self, slafile=None):
        version=self.scribusVersion()
        if version ==True:
            from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
            slatopdf = Sla2Pdf_ng( slafile= slafile)
            return slatopdf
        else:
            from promogest.lib.Sla2Pdf_classic import Sla2Pdf_classic
            slatopdf = Sla2Pdf_classic(pdfFolder = self.pdfFolder,
                                        slaFileName = self.slaFileName,
                            report = self.report).serialize(objects, dao=dao)
            return slatopdf

    def indexGroupTableFromListDict(self, group):
        """
        Dato un gruppo ti dà la sua tabella
        """
        for index in self.tablesProperties:
            if str(index.keys()[0]).strip() == str(group).strip():
                tableGroup = index[str(group)]
                break
        return tableGroup

    def getPagesNumber(self):
        """
        Al momento la funzione itera sula lista dei gruppi con più righe
        scarta i tag non utili e verifica poi la lunghezza del dao e il numero
        di righe presenti, c'è da migliorarla ma per il momento funziona
        """
        if not self.classic:
            self.pagesNumber = len(self.objects)
        else:
            self.pagesNumber =1
            for group in self.iteratableGroups:
                tableGroup = self.indexGroupTableFromListDict(group)
                for tagDict in self.tablesTags[group]:
                    for tag in tagDict.keys():
                        indexN = tag.find('(n)')
                        if (indexN != -1):
                            indexNP = tag.find('(n).')
                            group = str(group).strip()
                            if (indexNP != -1):
                                arrayName = tag[:indexNP]
                                valuesNumber = len(self.objects[self.cycle][arrayName])
                                rowsNumber = tableGroup['rows'] - 1
                            else:
                                valuesNumber = len(self.objects)
                                rowsNumber = tableGroup['rows'] - 1
                            self.pagesNumber = int(math.ceil(float(valuesNumber) / float(rowsNumber)))
        print "NUMERO PAGINE", self.pagesNumber


    def createPageTag(self, pagesNumber=None):
        # Index of first tag 'PAGE'
        self.pagesNumber = pagesNumber
        childrens = self.document.getchildren()
        Page = self.document.findall('PAGE')
        index = ''
        for index in range(0, len(childrens)):
            childrens[index] = str(childrens[index])
            s = childrens[index].find("<Element 'PAGE' at ")
            if s!= -1:
                break
        numPages = self.slaPage()
        for i in range(1, self.pagesNumber):
            attributes = numPages[0].items()
            dictionary =  {}
            for attr in attributes:
                dictionary[attr[0]] = attr[1]
            app = numPages[0].makeelement('PAGE', dictionary)
            self.slaDocumentTag().insert(index, app)
        print self.slaPage()

        # Processing page's information
        self.pageHeight = numPages[0].get('PAGEHEIGHT')
        self.borderTop = numPages[0].get('BORDERTOP')
        numPages = self.slaPage()
        for i in range(1, len(numPages)):
            # Number page
            numPages[i].set('NUM', str(i))
            # Coordinates
            self.lastPageYPos = numPages[i-1].get('PAGEYPOS')
            numPages[i].set('PAGEYPOS', str(float(self.pageHeight) + float(self.borderTop) + float(self.lastPageYPos)))


    def addEmptyPages(self):
        """ Creates new pages based on the model's first page """
        self.createPageTag(self.pagesNumber)
        if not self.label:
            self.duplicateElement()
            self.duplicateTags()
        elif self.label and not self.classic:
            self.duplicateElement()
            #self.duplicateTags()
            self.labelSla()
        #self.doc.write('__temp.sla')

    def duplicateElement(self):
        pages = len(self.slaPage())
        adesso = self.slaPageObjects()
        for j in range(1,pages):
            for pageObject in adesso:
                # Creating dictionary attributes pageobject
                attributes = pageObject.items()
                dictionary = {}
                for attr in attributes:
                    dictionary[attr[0]] = attr[1]

                # Applying attributes
                app = pageObject.makeelement('PAGEOBJECT', dictionary)
                # Creating dictionary attributes itext of the pageobject
                itexts = pageObject.findall('ITEXT')
                for itext in itexts:
                    attributes = itext.items()
                    dictionary = {}
                    for attrr in attributes:
                        dictionary[attrr[0]] = attrr[1]
                    # Applying attributes
                    ElementTree.SubElement(app, 'ITEXT', dictionary)
                paras = pageObject.findall('para')
                for para in paras:
                    attributes = para.items()
                    dictPara = {}
                    for attrrr in attributes:
                        dictPara[attrrr[0]] = attrrr[1]
                    # Applying attributes
                    ElementTree.SubElement(app, 'para', dictPara)
                pageItemAttributes = pageObject.findall('pageItemAttributes')
                ElementTree.SubElement(app, 'pageItemAttributes')
                # Number page
                inigroup = str(app.get('GROUPS')).strip()
                if inigroup:
                    nuovogruppo = (j+1)*(str(inigroup)+"%%%"+str(inigroup))
                    app.set('GROUPS',str(nuovogruppo))
                app.set('OwnPage', str(j))
                # Coordinates
                initial = app.get('YPOS')
                app.set('YPOS', str( j * (float(self.pageHeight) + float(self.borderTop)) + float(initial)))
                self.slaDocumentTag().append(app)


    def getTagToPrint(self, string,tags=None,k=None, increment=True,column = False ):
        """
        Questa funzione valuta quali tag riportare nel template definitivo
        TODO:da rivedere
        """
        if tags[k]['position'] in self.positionTags:
            if (((tags[k]['position'] == 'first') and (self.pageNumber == 1)) or
                ((tags[k]['position'] == 'last') and (self.pageNumber == self.pagesNumber))):
                if (k.find('(n)') > -1):
                    if increment:
                        self.tableGroup['counters'][column - 1] += 1
                    counter = self.tableGroup['counters'][column - 1]
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
                    self.tableGroup['counters'][column - 1] += 1
                counter = self.tableGroup['counters'][column - 1]
                tag = tags[k]['completeTag']
                tag = tag + ('<<%d>>' % counter)
                string = string.replace(tags[k]['completeTag'], tag)
            else:
                pass
        return string


    def duplicateTags(self):

        self.pageObjects = self.slaPageObjects()
        for pageObject in self.pageObjects:
            isTableItem = pageObject.get('isTableItem') == "1"
            group = str(pageObject.get('GROUPS')).strip()
            try:
                group= group.strip().split('%%%')[0]
            except:
                group= group
            if group:
                self.pageNumber = int(pageObject.get('OwnPage')) + 1
                self.tableGroup = self.indexGroupTableFromListDict(group)
                if isTableItem and (group in self.iteratableGroups):
                    # Qui vengono gestite le tabelle iterabili , e le righe
                    itexts = pageObject.findall('ITEXT')
                    paras = pageObject.findall('para')
                    pages = self.slaPage()
                    cell = int(pageObject.get('OwnLINK')) + 1
                    columns = self.tableGroup['columns']
                    row = (cell / columns) + 1
                    column = (cell % columns)
                    if not (len(itexts) > 0):
                        # first row of the table (with itext)
                        itext = self.tableGroup['itexts'][column - 1].copy()
                        if itext == {}:
                            continue
                        ch = str(itext['CH'])
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags is None:
                            continue
                        tmp = ch
                        tagsKeys = tags.keys()
                        increment = True
                        for k in tagsKeys:
                            if k.replace(' ', '') == '':
                                continue
                            if k.find('(n)') > -1:
                                tmp = self.getTagToPrint(tmp, column = column, increment=increment, tags=tags,k=k)
                                increment = False
                        itext['CH'] = tmp
                        ElementTree.SubElement(pageObject, 'ITEXT', itext)
                    else:
                        # next rows of the table (without itext)
                        # banalmente è la prima riga della tabella  es: U.M, DESCRIZIONE
                        itext = itexts[0]
                        ch = str(itext.get('CH'))
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags is not None:
                            tmp = ch
                            tagsKeys = tags.keys()
                            increment = True
                            for k in tagsKeys:
                                if k.replace(' ', '') == '':
                                    continue
                                if k.find('(n)') > -1:
                                    if self.tableGroup['itexts'][column - 1] == {}:
                                        self.tableGroup['itexts'][column - 1] = dict([attribute[0], attribute[1]] for attribute in itext.items())
                                    tmp = self.getTagToPrint(tmp,column = column, increment=increment, tags=tags,k=k)
                                    increment = False
                            itext.set('CH', tmp)
                else:
                    # Qui vengono gestite le tabelle e le celle con tag non iteranti
                    itexts = pageObject.findall('ITEXT')
                    if len(itexts) > 0:
                        itext = itexts[0]
                        ch = str(itext.get('CH'))
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags is not None:
                            tmp = ch
                            tagsKeys = tags.keys()
                            increment = True
                            for k in tagsKeys:
                                if k.replace(' ', '') == '':
                                    continue
                                tmp = self.getTagToPrint(tmp,increment=increment, tags=tags, k=k)
                                increment = False
                            itext.set('CH', tmp)




    def fillDocument(self):
        """ Replacing tags with real values """
        self.pageObjects = self.slaPageObjects()
        iterator = 0
        while iterator < self.lenPageObjects():
            pageObject = self.slaPageObjects()[iterator]
            isTableItem = pageObject.get('isTableItem')
            pageNumber = int(pageObject.get('OwnPage')) + 1
            group = str(pageObject.get('GROUPS')).strip()
            try:
                group= group.strip().split('%%%')[0]
            except:
                group = group
            pfile = pageObject.get('PFILE')
            if (pfile != ''):
                iterator += 1
                continue
            if group:
                actualGroup = group
                if str(actualGroup).strip() not in self.iteratableGroups:
                    # Replacing non-iterator tags
                    itexts = pageObject.findall('ITEXT')
                    for itext in itexts:
                        ch = str(itext.get('CH'))
                        tags = Sla2pdfUtils.findTags(ch)
                        #print "Stampo il tag", tags
                        if tags is not None:
                            tagsKeys = tags.keys()
                            #print "Dizionario dei tags tagsKeys",  tagsKeys
                            for tagkey in tagsKeys:
                                if tagkey.replace(' ', '') == '':
                                    continue
                                #try:
                                resolvedTag = ''
                                function = tags[tagkey]['function']
                                #print "function" , function
                                parameter = tags[tagkey]['parameter']
                                #print "parameter", parameter
                                if "X" in parameter:
                                    parameter = parameter.split("X")
                                if tagkey == 'currentPage':
                                    value = pageNumber
                                elif tagkey == 'totalPage':
                                    value = self.pagesNumber
                                elif tagkey in self.timeTags:
                                    value = Sla2pdfUtils.getNowValue(tagkey)
                                else:
                                    if self.cycle <= (len(self.objects) - 1):
                                        value = self.objects[self.cycle][tagkey] or ''
                                    else:
                                        value = ''
                                # Function
                                if function in self.formatFunctions:
                                    resolvedTag = self.callFunction(function, value, parameter)
                                else:
                                    resolvedTag = str(value)

                                ch = ch.replace(tags[tagkey]['completeTag'], resolvedTag)
                                  # Save itext
                                itext.set('CH', ch)

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
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags is not None:
                            tagsKeys = tags.keys()
                            for k in tagsKeys:
                                if k.replace(' ', '') == '':
                                    continue
                                #try:
                                resolvedTag = ''
                                function = tags[k]['function']
                                parameter = tags[k]['parameter']
                                if k == 'currentPage':
                                    value = pageNumber
                                elif k == 'totalPage':
                                    value = self.pagesNumber
                                elif k in self.timeTags:
                                    value = Sla2pdfUtils.getNowValue(k)
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
            iterator += 1
        #self.pageObjectPropertiesDict()
        #if not self.label:
        #self.findTablesProperties()
        self.doc.write(self.pdfFolder+"_temppp")
        self.toPdf(slafile=self.pdfFolder+"_temppp")
        #print

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
                return Sla2pdfUtils.truncValue(value, int(parameter))
        elif functionName == 'approx':
            if value == '' or parameter == '':
                return ''
            else:
                return Sla2pdfUtils.approxValue(value, int(parameter))
        elif functionName == 'itformat' or functionName == 'itformatdataora':
            if value == '':
                return ''
            else:
                return Sla2pdfUtils.itformatValue(value)
        elif functionName == 'itformatdata':
            if value == '':
                return ''
            else:
                return Sla2pdfUtils.itformatValue(value,tronca=True)
        elif functionName == 'bcview':
            if value == '':
                return ''
            else:
                #bcvalueTag= Sla2pdfUtils.bcviewValue(value, parameter)
                #return bcvalueTag
                return value
        else:
            return ''


    def scontiSequenceValues(self, sequence):
        """  Convert a sequence of sequences of "Sconto" DAOs into a sequence
        of human-readable strings  """
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

    def duplicateElementLabel(self):
        """
        Funzione base per la gestione delle frontaline:
        La gestione frontaline ha problematiche differenti rispetto ai report ed
        alle stampe singole. Il template contiene una frontalina di base che deve essere
        replicata enne volte quante dovuto uguale a se stessa per poi gestirne i tag
        rendendoli "iteranti". La parte meno complessa è quella della traduzione in
        pdf in quanto lo sla finito non rappresenta complessità particolari
        """
        numPages = self.slaPage()
        document = self.slaDocumentTag()
        self.pageProperties = Sla2pdfUtils.pageProFunc(document)
        group = self.tablesProperties[0].keys()[0]
        self.tablesPropertie = self.tablesProperties[0][group]
        widths = self.tablesPropertie['widths']
        heights = self.tablesPropertie['heights']
        cells = int(self.tablesPropertie['cells'])
        columns = int(self.tablesPropertie['columns'])
        rows = int(self.tablesPropertie['rows'])
        sumRows = Sla2pdfUtils.sumRowsFunc(heights,rows)
        sumColumns = Sla2pdfUtils.sumColumnsFunc(widths,columns)
        otherColumn = sumColumns +Environment.sistemaColonnaFrontaline
        sumRows = sumRows + Environment.sistemaRigaFrontaline
        self.pageYpos = float(numPages[0].get('PAGEYPOS'))
        self.pageXpos = float(numPages[0].get('PAGEXPOS'))
        self.pageHeight = float(numPages[0].get('PAGEHEIGHT'))
        self.borderTop = float(numPages[0].get('BORDERTOP'))
        self.borderBottom = float(numPages[0].get('BORDERBOTTOM'))
        self.borderLeft = float(numPages[0].get('BORDERLEFT'))
        self.borderRight = float(numPages[0].get('BORDERRIGHT'))
        self.pageWidth = float(numPages[0].get('PAGEWIDTH'))

        realHeightPage = self.pageHeight - self.borderTop - self.borderBottom
        realWidthPage = self.pageWidth - self.borderLeft - self.borderRight
        NumMaxRowLabelForPage = int(realHeightPage/sumRows)
        NumMaxColumnLabelForPage = int(realWidthPage /otherColumn)
        NumMaxLabelForPageTotal = NumMaxRowLabelForPage*NumMaxColumnLabelForPage
        NumLabelInDao = len(self.objects)
        pagesNumber = int((NumLabelInDao/NumMaxLabelForPageTotal)) +1
        self.createPageTag(pagesNumber)
        self.labelObj = self.slaPageObjects()
        op = True
        col = True
        for j in range(1, NumLabelInDao):
            p=r=c = 1
            for pageObject in self.labelObj:
                ## Creating dictionary attributes pageobject
                attributes = pageObject.items()
                dictionary = {}
                for k in range(0, len(attributes)):
                    dictionary[attributes[k][0]] = attributes[k][1]
                ## Applying attributes
                app = pageObject.makeelement('PAGEOBJECT', dictionary)
                ## Creating dictionary attributes itext of the pageobject
                itexts = pageObject.findall('ITEXT')
                for itext in itexts:
                    attributes = itext.items()
                    dictionary = {}
                    for kk in range(0, len(attributes)):
                        dictionary[attributes[kk][0]] = attributes[kk][1]
                    ## Applying attributes
                    ElementTree.SubElement(app, 'ITEXT', dictionary)

                paras = pageObject.findall('para')
                for para in paras:
                    attributes = para.items()
                    dictPara = {}
                    for kkk in range(0, len(attributes)):
                        dictPara[attributes[kkk][0]] = attributes[kkk][1]
                    ## Applying attributes
                    ElementTree.SubElement(app, 'para', dictPara)
                pageItemAttributes = pageObject.findall('pageItemAttributes')
                ElementTree.SubElement(app, 'pageItemAttributes')
                ## Number page
                #inigroup = str(app.get('GROUPS')).strip()
                x = str(10 +j)+ " "
                app.set('GROUPS', str(x))
                #app.set('OwnPage', str(j))
                ## Coordinates
                ypos = app.get('YPOS')
                height = app.get('HEIGHT')
                xpos = app.get('XPOS')
                if (j/NumMaxLabelForPageTotal) >= 1:
                    page = int(j/NumMaxLabelForPageTotal)
                else:
                    page = 0
                if j < NumMaxRowLabelForPage:
                    app.set('YPOS',str(float(ypos)+ sumRows*j))
                elif (j >= NumMaxRowLabelForPage) and (j < NumMaxLabelForPageTotal):
                    app.set('XPOS',str(float(xpos) + float(otherColumn)))
                    app.set('YPOS',str(float(ypos)+(sumRows*(j-NumMaxRowLabelForPage))))
                elif page != 0 and j < ((NumMaxLabelForPageTotal * page) + NumMaxRowLabelForPage):
                    app.set('YPOS',str(float(ypos)+\
                        ((float(self.pageHeight)+float(self.borderTop))*page)+\
                        sumRows*(j-(NumMaxLabelForPageTotal*page))))
                elif page !=0 and j >= (NumMaxLabelForPageTotal * page) +NumMaxRowLabelForPage and j < NumMaxLabelForPageTotal * page +NumMaxLabelForPageTotal:
                    app.set('XPOS',str(float(xpos) + float(otherColumn)))
                    app.set('YPOS',str(float(ypos)+\
                        ((float(self.pageHeight)+float(self.borderTop))*page)+\
                        sumRows*(j-(NumMaxLabelForPageTotal*page)-NumMaxRowLabelForPage)))
                else:
                    print "attenzione oggetto che non ha trovato collocazione"
                self.slaDocumentTag().append(app)
                app = {}
        self.labelSla()
        self.findTablesProperties()

    def labelSla(self):
        """
        FIXME: Grave bug , non lascia il testo semplice nella cella in cui è presente
            anche un tag ...
        """
        self.labelObj = self.slaPageObjects()
        index = -1
        gr = []
        for pageObject in self.labelObj:
            itexts = pageObject.findall('ITEXT')
            group = pageObject.get('GROUPS')
            if group in gr:
                for itext in itexts:
                    attributes = itext.items()
                    dictionary = {}
                    for kk in range(0, len(attributes)):
                        dictionary[attributes[kk][0]] = attributes[kk][1]
                    ch = dictionary['CH']
                    tags = Sla2pdfUtils.findTags(ch)
                    #print "tagsssss", ch, tags
                    if tags:
                        tagsKeys = tags.keys()[0] or []
                        function = tags[tagsKeys]['function']
                        parameter = tags[tagsKeys]['parameter']
                        if function == "bcview":
                            bc = str(self.objects[index][tagsKeys])
                            if bc == "None":
                                bc = "0000000000000"
                            value = "bcview;%s;%s;%s" %(bc,
                                        str(tags[tagsKeys]['parameter'].split('X')[0]),
                                        str(tags[tagsKeys]['parameter'].split('X')[1])) or ""
                        elif tagsKeys in self.timeTags:
                            value = Sla2pdfUtils.getNowValue(tagsKeys)
                        else:
                            value = self.objects[index][tagsKeys] or ""
                        if function in self.formatFunctions and "X" not in parameter:
                            resolvedTag = self.callFunction(function, str(value), int(parameter))
                            value = ch.replace(tags[tagsKeys]['completeTag'], resolvedTag)
                        else:
                            value = str(value)
                    else:
                        value = ch
                    #print "valueeeeeeeeeeeeee", value
                    itext.set('CH', str(value))
            else:
                gr.append(group)
                index += 1

    def cancelOperation(self):
        """
        Cancel current operation (i.e. make the computation stop as
        soon as possible, e.g. when executed in a parallel thread)
        """
        pass

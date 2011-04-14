# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os
import math
import pprint
from promogest.ui.utils import setconf
import xml.etree.cElementTree as ElementTree
from promogest import Environment
from promogest.lib import Sla2pdfUtils

# KNOWN BUGS
# ****************************************************************
# Fonts don't selectable
# Double itexts or more, don't work (see also Paragraph)
# Tags live only in tables, at least 1x1
# Wrong tags break the program

# Fonts working
##const QString tmpf[] = {"/Courier", "/Courier-Bold", "/Courier-Oblique", "/Courier-BoldOblique",
##                        "/Helvetica", "/Helvetica-Bold", "/Helvetica-Oblique", "/Helvetica-BoldOblique",
##                        "/Times-Roman", "/Times-Bold", "/Times-Italic", "/Times-BoldItalic",
##                        "/ZapfDingbats", "/Symbol"};

## New tag  for 0.4 version :   [[bcview(codice_a_barre,1X2)]]  where bcview is
## function, codice_a_barre is the tag and 1X2 are width and height also decimal dot separated is allow. ( 1X0.8)
## Image Size fixed on pdf convertion.
# fixed fontsize recognition with standard font if not setted

__Version__ = "0.6"

class SlaTpl2Sla(object):

    def __init__(self, slaFileName, pdfFolder, report=False, label=False, classic=None, template_file=None):
        """
        Build a template object based on the specified file-like
        object and sequence of objects
        """
        self.pp = pprint.PrettyPrinter(indent=4)
        self.slaFileName = slaFileName
        self.pdfFolder = pdfFolder
        self.pdfFileName = '_temp'
        self.slaTempFileName = '_temp.sla'
        self.formatFunctions = ['trunc','approx','itformat','itformatdataora','itformatdata', 'bcview']
        self.timeTags = ['date','time','datetime']
        self.positionTags = ['first','last']
        self.pageTags = ['currentPage','totalPage']
        self._classic = classic
        self._template_file = template_file
        self.report = report
        self.label = label
        self.cycle = 0

    def slaRootTag(self):
        """ Restituisce la root del file XML di scribus
        """
        f = file(self.slaFileName, 'rb')
        text = f.read()
        text = text.replace('&#x5;', '\\n')
        f.close()
        tempFile = self.pdfFolder + self.slaTempFileName
        f = file(tempFile, 'wb')
        f.write(text)
        f.close()
        self.doc = ElementTree.parse(tempFile)
        #os.remove(tempFile)
        self.root = self.doc.getroot() #<Element 'SCRIBUSUTF8NEW' at 0x24cf660>
        self.document= self.root.findall('DOCUMENT')[0]

    def indexGroupTableFromListDict(self, group):
        """ Dato un gruppo ti dà la sua tabella
        """
        for index in self.tablesProperties:
            if str(index.keys()[0]).strip() == str(group).strip():
                tableGroup = index[str(group)]
                break
        return tableGroup

    def serialize(self, objects, dao=None, classic =None, template_file=None):
        """ Model parsing, values substitution and pdf creation """
        self.objects = objects
        result = None
        self._classic = classic
        self._template_file = template_file
        if template_file:
            self.slaFileName = Environment.labelTemplatesDir+template_file
        self.slaRootTag()
        version=self.scribusVersion()
        if version:
            print "DICIAMO 1.3.4", "label",self.label,"classic", self._classic
            from promogest.lib.Sla2Pdf_ng import Sla2Pdf_ng as Sla2Pdf
            self.findTablesAndTags()
            self.findTablesProperties()
            self.getIteratableGroups()
            self.getPagesNumber()
#            print " dopo getPagesNumber"
            if self.label and self._classic:
#                print " è una label ...di tipo classico ? "
                self.duplicateElementLabel()

            self.addEmptyPages()
#            print " prima di fillDocument()"
            self.fillDocument()
#            print " prima di findTablesProperties()"
            self.findTablesProperties()
#            print "PRIMA DELLA CONVERSIONE IN PDF"
            slatopdf = Sla2Pdf(document = self.slaDocumentTag(),
                            pdfFolder = self.pdfFolder,
                            version=self.scribusVersion(),
                            tablesProperties=self.tablesProperties,
                            pgObjList=self.slaPageObjects(),
                            numPages = self.pagesNumber,
                            iteratableGroups = self.iteratableGroups)
            # temporary pdf file is removed immediately
            filename = self.pdfFolder + self.pdfFileName + '.pdf'
            f = file(filename, 'rb')
            result = f.read()
            f.close()
            os.remove(filename)
            return result
        else:
            print "DICIAMO 1.3.3"
            from promogest.lib.Sla2Pdf_classic import Sla2Pdf_classic
            slatopdf = Sla2Pdf_classic(pdfFolder = self.pdfFolder,
                                slaFileName = self.slaFileName,
                                report = self.report).serialize(objects, dao=dao)
            return slatopdf

    def findTablesProperties(self):
        """
        Questa Funzione crea un dizionario che ha come chiave il gruppo, sia nella
        sua forma originale che in quella modificata per poter distinguere immagini
        e campi monocella, come valori al momento ha tutto ciò che occorre per
        capire come sia composta la tabella, proprietà delle celle, numero delle colonne,
        formattazione.

        TODO: Lavoro sprecato, si potrebbero far viaggiare oggetti che poi
                all'occorrenza potrebbero venire manipolati per fornire i dati
                necessari
        FIXME: Brutta la ripetizione dei campi per la gestione del monocella
        """
        propertiesList = []
        tableList = []
        table= None
        monoFoto = False
        for obj in self.slaPageObjects():
            groupDict = {}
            leftLink = []
            widths = []
            heights = []
            topLink = []
            ypos = []
            xpos = []
            itexts = []
            ownPage = []
            paras = []
            tableMod = []
            cellproperties= []
            table = obj.get('GROUPS')
            #table = table[0]
            #except:
                #table = table
            pfile2 = obj.get('PFILE')
            if table == "":
                xpos = [float(obj.get('XPOS'))]
                ypos = [float(obj.get('YPOS'))]
                isTableItem2 = obj.get('isTableItem')
                table = "noGroup" + str(xpos) + str(ypos)
                cellproperties = [{
                                "bottomLine" : int(obj.get('BottomLine')),
                                "topLine":  int(obj.get('TopLine')),
                                "leftLine" : int(obj.get('LeftLine')),
                                "rightLine" : int(obj.get('RightLine')),
                                "lineWidth" : float(obj.get('PWIDTH')),
                                "borderColor" : obj.get('PCOLOR2'),
                                "cellBackground" : obj.get('PCOLOR'),
                                "cellBackground" : obj.get('PCOLOR'),
                                "cellPicture": obj.get('PFILE'),
                                "cellHeight" :obj.get('HEIGHT'),
                                "cellWidth" :obj.get('WIDTH')}]
                widths = [float(obj.get('WIDTH'))]
                heights = [float(obj.get('HEIGHT'))]
                paras = obj.findall('para')
                itexts = obj.findall('ITEXT')
                isGroupControl = obj.get('isGroupControl')
            else:
                itext = obj.findall('ITEXT')
                for abj in self.slaPageObjects():
                    gruppo = abj.get('GROUPS')
                    #try:
                        #gruppo = gruppo[0]
                    #except:
                        #gruppo = gruppo
                    if gruppo == table and (table not in tableList):
                        if abj.get('isGroupControl')=="0":
                            if abj.get("LeftLINK") == "-1":
                                leftLink.append(abj.get("LeftLINK"))
                            if abj.get("TopLINK") == "-1":
                                topLink.append(abj.get("TopLINK"))
                            cellpropert = {
                                        "bottomLine" : int(abj.get('BottomLine')),
                                        "topLine":  int(abj.get('TopLine')),
                                        "leftLine" : int(abj.get('LeftLine')),
                                        "rightLine" : int(abj.get('RightLine')),
                                        "lineWidth" : float(abj.get('PWIDTH')),
                                        "borderColor" : abj.get('PCOLOR2'),
                                        "cellBackground" : abj.get('PCOLOR'),
                                        "cellPicture": abj.get('PFILE'),
                                        "cellHeight" :abj.get('HEIGHT'),
                                        "cellWidth" :abj.get('WIDTH')
                                        }
                            cellproperties.append(cellpropert)
                            width = float(abj.get('WIDTH'))
                            widths.append(width)
                            height = float(abj.get('HEIGHT'))
                            heights.append(height)
                            xposvar = float(abj.get('XPOS'))
                            xpos.append(xposvar)
                            yposvar = float(abj.get('YPOS'))
                            ypos.append(yposvar)
                            itexts.append(abj.findall('ITEXT'))
                            paras.append(abj.findall('para'))
                            #pfile2 = abj.get('PFILE')
                            isTableItem2 = abj.get('isTableItem')
                            isGroupControl = abj.get('isGroupControl')
                            ownPag = abj.get('OwnPage')
                            ownPage.append(ownPag)
                            if len(topLink) == 0:
                                columns = 1
                            else:
                                columns= len(topLink)
            #print "questa è la lista delle tabelle già parsate", tableList, table
            if table not in tableList:
                n_cells = len(leftLink)*columns
                groupDict[str(table).strip()] = {
                            'GROUPS': table,
                            'isTableItem': isTableItem2,
                            'isGroupControl':isGroupControl,
                            'cells': n_cells,
                            'rows': len(leftLink),
                            'columns': columns,
                            'widths' :widths,
                            'heights':heights,
                            'ypos':ypos,
                            'xpos':xpos,
                            'ownPage' :ownPage,
                            'pfile':pfile2,
                            'iterproper':[],
                            'cellProperties':cellproperties,
                            'itexts' : list({} for i in range(0,len(topLink ))),
                            'para' : list({} for i in range(0,len(topLink ))),
                            'itextsobj':itexts,
                            'parasobj': paras,
                            'counters' :list(-1 for i in range(0,len(topLink )))}
                #print "DDDDDDDDDDDDDDDD", table, pfile2, isTableItem2,len(leftLink), columns, n_cells,
                tableList.append(table)
                widths = heights =ypos =  xpos = tableMod = topLink = ownPage = leftLink = itexts = cellproperties = paras =[]
                monoFoto = False
                propertiesList.append(groupDict)
        self.tablesProperties=propertiesList

    def findTablesAndTags(self):
        """
        Questa funzione crea DUE e dico DUE dizionari, uno con chiave gruppo
        e valore tags e l'altro con i tags come chiave e il gruppo come valore.
        il secondo DICT lo trovo assurdo, temo che non consideri campi Dao doppi
        nel templates e la cosa NON mi piace. NON ho tempo adesso per verificare

        TODO: Verificare il dizionario tagsTables. ...
        """
        group = ''
        vector = []
        self.tablesTags = {}        # relation group -> tags
        self.tagsTables = {}        # relation tag -> group

        for pageObject in self.slaPageObjects():
            isTableItem = (pageObject.get('isTableItem') == "1")
            if not isTableItem:
                continue
            group = str(pageObject.get('GROUPS')).strip()
            if group:
                itexts = pageObject.findall('ITEXT')
                ch = ''
                if self.tablesTags.has_key(group):
                    vector = self.tablesTags[group]
                else:
                    vector = []
                for i in itexts:
                    ch = str(i.get('CH'))
#                    print " CHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", ch
                    if ch.replace(' ', '') == '':
                        continue
                    tags = Sla2pdfUtils.findTags(ch)
#                    print "TAAAAAAAAAAAAAAGSSS", tags, vector
                    if tags is not None:
                        if tags not in vector:
                            vector.append(tags)
                        for k in tags.keys():
                            self.tagsTables[k] = group
                self.tablesTags[group] = vector

    def getIteratableGroups(self):
        """
        Questa funzione ha l'importante compito di creare una lista con i gruppi
        relativi alle tabelle che iterano ( righe e castelletto iva al momento )
        """
        self.iteratableGroups = []
        for group in self.tablesTags.keys():
            for tagDict in self.tablesTags[group]:
                for tag in tagDict.keys():
                    indexN = tag.find('(n)')
                    if (indexN != -1):
                        if group.strip() not in self.iteratableGroups:
                            self.iteratableGroups.append(str(group).strip())
        #print "questi sono i gruppi su cui deve iterare:", self.iteratableGroups

    def getPagesNumber(self):
        """
        Al momento la funzione itera sula lista dei gruppi con più righe
        scarta i tag non utili e verifica poi la lunghezza del dao e il numero
        di righe presenti, c'è da migliorarla ma per il momento funziona
        """
        if not self._classic:
            self.pagesNumber = len(self.objects)
        else:
            self.pagesNumber = 1
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
        #self.pagesNumber = 2
        print "questo è il nuovo numero di pagine del template sla:", self.pagesNumber

    def createPageTag(self, pagesNumber=None):
        # Index of first tag 'PAGE'
        self.pagesNumber = pagesNumber
        childrens = self.slaDocumentTag().getchildren()
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
        elif self.label and not self._classic:
            self.duplicateElement()
            #self.duplicateTags()
            self.labelSla()

        self.doc.write('_temp.sla')

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

        otherColumn = sumColumns +(int(setconf("Label", "sistemacolonnafrontaline")) or 0)
        sumRows = sumRows + (int(setconf("Label", "sistemarigafrontaline")) or 0)

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

    def getTagToPrint(self, string,tags=None,k=None, increment=True,column = False ):
        """
        Questa fuinzione valuta quali tag riportare nel template definitivo
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
                            if "€" in ch or "Euro" in ch:
                                mettilo = True
                            tagsKeys = tags.keys()
                            increment = True
                            for k in tagsKeys:
                                if k.replace(' ', '') == '':
                                    continue
                                tmp = self.getTagToPrint(tmp,increment=increment, tags=tags, k=k)
#                                print " TEEEEMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP", tmp, ch
                                increment = False
                                prova = ch.replace(tmp,"")
                                if "EUR" in prova.upper() :
                                    prova = "€ "
#                            if prova:
                                itext.set('CH',prova +tmp )
#                            else:
#                                itext.set('CH', tmp)

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
        if not self.label:
            self.findTablesProperties()
        self.doc.write('___temp.sla')

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

    def scribusVersion(self):
        slaversion = self.root.get('Version')
        print "VERSIONE FILE SLA", slaversion
        if slaversion == "1.3.4" or  "1.3.5" in slaversion:
            version=True
        else:
            version = False
        return version

    def slaDocumentTag(self):
        document = self.root.findall('DOCUMENT')[0]
        return document

    def slaPageObjects(self):
        if self.document:
            pageObjects =self.document.findall('PAGEOBJECT')
        else:
            pageObjects = self.slaDocumentTag().findall('PAGEOBJECT')
        return pageObjects

    def lenPageObjects(self):
        lenPageObjects = len(self.slaPageObjects())
        return lenPageObjects


    def slaCharStyleDefault(self):
        charStyleTag = self.slaDocumentTag().findall('CHARSTYLE')
        return charStyleTag

    def slaPdfDefault(self):
        pdfTag = self.slaDocumentTag().findall('PDF')
        return pdfTag

    def slaPage(self):
        page = self.slaDocumentTag().findall('PAGE')
        return page

    def cancelOperation(self):
        """
        Cancel current operation (i.e. make the computation stop as
        soon as possible, e.g. when executed in a parallel thread)
        """
        pass

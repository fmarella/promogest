# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>

import math
import operator
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
                    daos=None, slaFileName=None, pdfFolder=None, classic=None,
                    template_file=None):


        SlaParser.__init__(self, slaFileName=slaFileName,
                                    pdfFolder=pdfFolder,
                                    slafile=slafile)
        #self.pdfFileName = '_temp'
        #self.slaTempFileName = '_temp.sla'
        self.slaFileName = slaFileName
        self.report = report
        self.classic = classic
        self.template_file = template_file
        self.daos = daos
        self.objects = objects
        self.label = label
        self.formatFunctions = ['trunc','approx','itformat','itformatdataora','itformatdata', 'bcview']
        self.timeTags = ['date','time','datetime']
        self.positionTags = ['first','last']
        self.pageTags = ['currentPage','totalPage']
        self.cycle = 0
        # in slaparser in quanto server anche dopo per sla2pdf
#        self.findTablesAndTags()
        #questa è una funzione chiave .....
        self.tableProperties = self.findTablesProperties()
        self.pagesNumber = self.getPagesNumber()
        if self.label and self.classic:
            self.duplicateElementLabel()
        if self.pagesNumber >1:
            self.addEmptyPages()
        if not self.label:
            self.duplicateElement(self.pagesNumber)
            self.duplicateTags()
            self.doc.write(self.pdfFolder+"_tep.sla")
            self.fillDocument()
        elif self.label and not self.classic:
            self.duplicateElement(self.pagesNumber)
            #self.duplicateTags()
            self.labelSla()

#        self.fillDocument()
        self.doc.write(self.pdfFolder+"_temppp.sla")

    def fileElaborated(self):
        """ aggiunto per maggiore pulizia"""
        return self.pdfFolder+"_temppp.sla"

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
        Al momento la funzione itera sulla lista dei gruppi con più righe
        scarta i tag non utili e verifica poi la lunghezza del dao e il numero
        di righe presenti, c'è da migliorarla ma per il momento funziona
        """
        pags = [1]
        if not self.classic:
            pags = [len(self.objects)]
        else:
            for group in self.getIteratableGroups(self.tableProperties):
                gruppo = self.indexGroupTableFromListDict(group)

                cellsprop = [x.findall('ITEXT') for x in gruppo["cells"] if x.findall('ITEXT')]
                righe = [round(float(x.get('gYpos')),3) for x in gruppo["cells"]]
                rowsNumber = len(sorted(list(set(righe))))
                for i in cellsprop:
                    a = [g.get("CH") for g in i if "(n)" in g.get("CH")]
                    for s in a:
                        arrayName = Sla2pdfUtils.findTags(s).values()[0]["arrayName"]
                        valuesNumber = len(self.objects[self.cycle][arrayName])
                        pagesNumber = int(math.ceil(float(valuesNumber) / float(rowsNumber)))
                        pags.append(pagesNumber)
        return max(pags)

    def createPageTag(self, pagesNumber=None):
        # Index of first tag 'PAGE'
        childrens = self.document.getchildren()
        page = self.document.findall('PAGE')
        index = ''
        for index in range(0, len(childrens)):
            if "<Element 'PAGE' at " in str(childrens[index]):
                break
        numPages = self.slaPage()
        for i in range(1, pagesNumber):
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
        #self.doc.write('__temp.sla')

    def duplicateElement(self, pages):
        """ Duplica TUTTI gli oggetti da una pagina all'altra """
#        pages = len(self.slaPage())
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
                    ElementTree.SubElement(app, 'ITEXT', dictionary)
                trails = pageObject.findall('trail')
                for trai in trails:
                    attributes = trai.items()
                    dictTrai = {}
                    for attrrr in attributes:
                        dictTrai[attrrr[0]] = attrrr[1]
                    ElementTree.SubElement(app, 'trail', dictTrai)

                paras = pageObject.findall('para')
                for para in paras:
                    attributes = para.items()
                    dictPara = {}
                    for attrrr in attributes:
                        dictPara[attrrr[0]] = attrrr[1]
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

    def getTagToPrint(self, string,tags=None,k=None, increment=True,column = False,row=None, pageNamber=0):
        """
        Questa funzione valuta quali tag riportare nel template definitivo
        TODO:da rivedere
        """
        if tags[k]['position'] in self.positionTags:
            if (((tags[k]['position'] == 'first') and (pageNamber+1 == 1)) or
                ((tags[k]['position'] == 'last') and (pageNamber+1 == self.pagesNumber))):
                if '(n)' in k:
                    tag = tags[k]['completeTag']
                    tag = tag + ('<<%d>>' % row)
                    string = string.replace(tags[k]['completeTag'], tag)
                else:
                    string = tags[k]['completeTag']
            else:
                string = ''
        else:
            if '(n)' in k:

                tag = tags[k]['completeTag']
                tag = tag + ('<<%d>>' % row)
                string = string.replace(tags[k]['completeTag'], tag)
        return string

    def duplicateTags(self):
        """ Dopo aver duplicato gli elementi adesso duplichiamo i tags
            TODO: refactoring di questa func"""

        self.gruppi = self.findTablesProperties()
        iteranti = self.getIteratableGroups(self.gruppi)
        for group in self.gruppi:
            rigaConItextDict = {}
            gruppo = group.values()[0]
            if "%%%" in gruppo["GROUPS"]:
                groupname= str(gruppo["GROUPS"].strip().split('%%%')[0])
            else:
                groupname = str(gruppo["GROUPS"].strip())

            if groupname in iteranti :
                # Qui vengono gestite le tabelle iterabili , e le righe
                cellsprop = [{x:[x,x.findall('ITEXT'),x.findall('para'),
                                x.findall('trail')]} for x in gruppo["cells"]]
                colonne = [float(x.get('gXpos')) for x in gruppo["cells"]]
                righe = [float(x.get('gYpos')) for x in gruppo["cells"]]
                col = list(set(colonne))
                col = sorted(col)
                rows = list(set(righe))
                rows = sorted(rows)
                numeroRighe = len(rows)-1
                for cel in cellsprop:
#                    print "CELLLLLLLLLLLLLLLLA", cel
                    CH = None
                    tags = {}
                    rowgg = rows.index(float(cel.values()[0][0].get("gYpos")))
                    pageNamber = int(cel.values()[0][0].get("OwnPage"))
                    row = (numeroRighe*pageNamber)+rowgg
                    for ite in cel.values()[0][1]:
                        CH = ite.get("CH")
                        tags = Sla2pdfUtils.findTags(CH)
                    column = col.index(float(cel.values()[0][0].get("gXpos")))+1
                    # quelli con tag e CH sono quelli della seconda riga che poi dovrò andare a ciclare
                    # nella prima riga c'è di norma solo un CH ma senza TAG
                    if tags and CH:
                        # build a dict with all second row data with tags and CH
                        rigaConItextDict[str(column)+"%"+groupname] = [CH,tags,ite,cel]
                        for k in tags.keys():
                            if k.replace(' ', '') is not '':
                                if '(n)' in k :
                                    if tags[k]['position'] == 'last':
                                        row = rowgg
                                    tmp = self.getTagToPrint(CH, column = column,row=row-1, tags=tags,k=k, pageNamber=pageNamber)
                                ite.set("CH", tmp)
                    else:
                        colu = int(col.index(float(cel.values()[0][0].get("gXpos")))+1)
                        if str(colu)+"%"+groupname in rigaConItextDict:
                            ch = rigaConItextDict[str(colu) +"%" + groupname][0]
                            tags = rigaConItextDict[str(colu) +"%"+ groupname][1]
                            ite = rigaConItextDict[str(colu)+"%"+groupname][2]
                            ricel = rigaConItextDict[str(colu)+"%"+groupname][3]

                            attributes = ite.items()
                            itedict= {}
                            for attrr in attributes:
                                itedict[attrr[0]] = attrr[1]
                            tmp = ch
                            for k in tags.keys():
                                if k.replace(' ', '') is not '':
                                    if '(n)' in k :
                                        if tags[k]['position'] == 'last':
                                            row = rowgg
                                        tmp = self.getTagToPrint(tmp, column = colu,row=row-1, tags=tags,k=k,pageNamber=pageNamber)
                                itedict["CH"] = tmp
                                ElementTree.SubElement(cel.values()[0][0], 'ITEXT', itedict)

#                            origpara = ricel.values()[0][2]
#                            para = cel.values()[0][2]
#                            if origpara:
#                                origpara=origpara[0]
#                                if para:
#                                    for t in para:
#                                        attria = t.items()
#                                        for attrr in attria:
#                                            origpara.set(attrr[0],attrr[1])
#                                else:
#                                    paradict = {}
#                                    for attrr in origpara.items():
#                                        paradict[attrr[0]] = attrr[1]
#                                    ElementTree.SubElement(cel.values()[0][0], 'para', paradict)

                            trai = ricel.values()[0][3]
                            origtrai = cel.values()[0][3]
                            if origtrai:
                                origtrai=origtrai[0]
                                for t in trai:
                                    attria = t.items()
                                    for attrr in attria:
                                        origtrai.set(attrr[0],attrr[1])
                            else:
                                for t in trai:
                                    traidict = {}
                                    attria = t.items()
                                    for attrr in attria:
                                        traidict[attrr[0]] = attrr[1]
                                        ElementTree.SubElement(cel.values()[0][0], 'trail', traidict)
            else:
                # Qui vengono gestite le tabelle e le celle con tag non iteranti
                itexts = [x.findall('ITEXT') for x in gruppo["cells"]]
                pageNamber = int(gruppo["cells"][0].get("OwnPage"))
                if itexts:
                    for tex in itexts:
                        if type(tex) == type([1,2]):
                            if tex:
                                itext = tex[0]
                            else:
                                continue
                        ch = itext.get('CH')
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags:
                            tmp = ch
                            tagsKeys = tags.keys()
                            for k in tagsKeys:
                                if k.replace(' ', '') == '':
                                    continue
                                tmp = self.getTagToPrint(tmp,tags=tags, k=k,pageNamber =pageNamber)
                                prova = ch.replace(tmp,"")
                                itext.set('CH',prova.encode()+" "+ tmp.encode() )

    def fillDocument(self):
        """ Replacing tags with real values """
        self.gruppi = self.findTablesProperties()
        iteranti = self.getIteratableGroups(self.gruppi)
        self.pageObjects = self.slaPageObjects()
        iterator = 0
        while iterator < self.lenPageObjects():
            pageObject = self.pageObjects[iterator]
            isTableItem = pageObject.get('isTableItem')
            isGroupControl = pageObject.get('isGroupControl')
            pageNumber = int(pageObject.get('OwnPage')) + 1
            group = str(pageObject.get('GROUPS')).strip()
            itexts = pageObject.findall('ITEXT')
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
                if str(actualGroup).strip() not in iteranti:
                    # Replacing non-iterator tags

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
                                parameter = tags[tagkey]['parameter']
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
                                itext.set('CH', ch.decode())

                else:
                    if isGroupControl == '1':
                        iterator += 1
                        continue
                    for itext in itexts:
                        ch = str(itext.get('CH'))
                        if '<<' in ch and '>>' in ch:
                            while (ch.find('<<') > -1) and (ch.find('>>') > -1):
                                arrayIndex = int(ch[ch.find('<<')+2:ch.find('>>')])
                                ch = ch.replace(('<<%d>>' % arrayIndex), '')
                        else:
                            arrayIndex = -1
                        tags = Sla2pdfUtils.findTags(ch)
                        if tags is not None:
                            for k in tags.keys():
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
                                    if '(n)' in k:
                                        indexNP = k.find('(n).')
                                        if '(n).' in k:
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
#                                print "FUCTION", function, value, parameter
                                if function in self.formatFunctions:
                                    resolvedTag = self.callFunction(function, value, parameter)
                                else:
                                    resolvedTag = str(value)
                                ch = ch.replace(tags[k]['completeTag'], resolvedTag)
                                # Save itext
                                itext.set('CH', ch.decode())
            iterator += 1


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

        widths = [float(x.get("WIDTH")) for x in self.tablesPropertie['cells']]
        heights = [float(x.get("HEIGHT")) for x in self.tablesPropertie['cells']]
        cells = int(self.tablesPropertie['n_cells'])
        columns = int(self.tablesPropertie['columns'])
        rows = int(self.tablesPropertie['rows'])

        sumRows = reduce(operator.add, heights[:rows])
        sumColumns = reduce(operator.add, widths[:columns])
        otherColumn = sumColumns +Environment.sistemaColonnaFrontaline
        otherRows = sumRows + Environment.sistemaRigaFrontaline

        pageYpos = float(numPages[0].get('PAGEYPOS'))
        pageXpos = float(numPages[0].get('PAGEXPOS'))
        pageHeight = float(numPages[0].get('PAGEHEIGHT'))
        borderTop = float(numPages[0].get('BORDERTOP'))
        borderBottom = float(numPages[0].get('BORDERBOTTOM'))
        borderLeft = float(numPages[0].get('BORDERLEFT'))
        borderRight = float(numPages[0].get('BORDERRIGHT'))
        pageWidth = float(numPages[0].get('PAGEWIDTH'))

        realHeightPage = pageHeight - (borderTop + borderBottom)
        realWidthPage = pageWidth - (borderLeft + borderRight)
        NumMaxRowLabelForPage = int(realHeightPage/otherRows)
        NumMaxColumnLabelForPage = int(realWidthPage /otherColumn)
        NumMaxLabelForPageTotal = NumMaxRowLabelForPage*NumMaxColumnLabelForPage
        NumLabelInDao = len(self.objects)
        pagesNumber = int((NumLabelInDao/NumMaxLabelForPageTotal)) +1

        self.createPageTag(pagesNumber)
        labelObj = self.slaPageObjects()
        for j in range(1, NumLabelInDao):
            for pageObject in labelObj:
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

                trails = pageObject.findall('trail')
                for trai in trails:
                    attributes = trai.items()
                    dictTrai = {}
                    for attrrr in attributes:
                        dictTrai[attrrr[0]] = attrrr[1]
                    ElementTree.SubElement(app, 'trail', dictTrai)

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
                inigroup = str(pageObject.get('GROUPS')).strip()
                x = str(j+int(inigroup))+ " "
                app.set('GROUPS', x)
                app.set('OwnPage', str(j))
                ## Coordinates
                ypos = pageObject.get('YPOS')
                height = pageObject.get('HEIGHT')
                xpos = pageObject.get('XPOS')
                if (j/NumMaxLabelForPageTotal) >= 1:
                    page = int(j/NumMaxLabelForPageTotal)
                else:
                    page = 0
                colonna = NumMaxColumnLabelForPage- ((NumMaxLabelForPageTotal*(page+1) - (j+1)) / NumMaxRowLabelForPage)-1
                riga = j- (NumMaxRowLabelForPage * (j/NumMaxRowLabelForPage))
                if not j%NumMaxRowLabelForPage:
                    app.set('YPOS',str(float(ypos)+((float(pageHeight)+float(borderTop))*page)))
                else:
                    app.set('YPOS',str(float(ypos)+((float(pageHeight)+float(borderTop))*page)+ (otherRows* riga)))
                app.set('XPOS',str(float(xpos) + otherColumn* (colonna)))
                self.slaDocumentTag().append(app)
                app = {}
#        self.doc.write(self.pdfFolder+"_tempppPrima.sla")
        self.labelSla()

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
                    itext.set('CH', value)
            else:
                gr.append(group)
                index += 1

    def cancelOperation(self):
        """
        Cancel current operation (i.e. make the computation stop as
        soon as possible, e.g. when executed in a parallel thread)
        """
        pass

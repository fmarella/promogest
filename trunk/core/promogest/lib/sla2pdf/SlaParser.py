# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>
# Copyright (C) 2008-2009 by Promotux Informatica - http://www.promotux.it/
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
#from promogest import Environment
import Sla2pdfUtils

class SlaParser(object):

    def __init__(self, slaFileName=None, pdfFolder=None,
                        slafile=None):
        self.slaFileName = slaFileName
        self.pdfFolder = pdfFolder
        self.slafile = slafile
        print "FILE SLA", self.slafile
        #self.slaTempFileName = slaTempFileName
        ##print "FILETRANSLATEEEED", fileTranslated
        #if fileTranslated:
            #self.doc = fileTranslated
        #else:
        self.doc = None
        self.tempFile = self.simpleSanitize()


    def simpleSanitize(self ):
        """ Ripulisce lo sla da caratteri spuri
        """
        if self.slafile :
            #self.slaFileName = self.slafile
            self.doc = ElementTree.parse(self.slafile)
        else:
            f = file(self.slaFileName, 'rb')
            text = f.read()
            text = text.replace('&#x5;', '\\n')
            f.close()
            tempFile = self.pdfFolder+"_temp"
            f = file(tempFile, 'wb')
            f.write(text)
            f.close()
            self.doc = ElementTree.parse(tempFile)
        self.slaRootTag()
        self.slaDocumentTag()
        #return tempFile

    def lenPageObjects(self):
        lenPageObjects = len(self.slaPageObjects())
        return lenPageObjects

    def slaCharStyleDefault(self):
        charStyleTag = self.slaDocumentTag().findall('CHARSTYLE')
        return charStyleDefault

    def slaPdfDefault(self):
        pdfTag = self.slaDocumentTag().findall('PDF')
        return pdfDefault

    def slaPage(self):
        page = self.slaDocumentTag().findall('PAGE')
        return page

    def slaRootTag(self):
        self.root = self.doc.getroot()
        return self.root

    def slaDocumentTag(self):
        #root = self.slaRootTag()
        self.document = self.root.findall('DOCUMENT')[0]
        return self.document

    def slaPageObjects(self):
        self.pageObjects = self.document.findall('PAGEOBJECT')
        return self.pageObjects

    def shitFunc(self, lista):
        """ This shit func is here because scribus take off the right mode to calculate
            columns or rows in a table"""
        lista2 = []
        for l in lista:
            lista2.append(round(l,2))
        return len(set(lista2))



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
        #if self.tablesProperties:
            #return self.tablesProperties
        #else:
        print "IMPORTANTE ANALISI TABELLA", len(self.slaPageObjects())
        propertiesList = []
        tableList = []
        table= None
        monoFoto = False
        columns=1

        for obj in self.slaPageObjects():
            #print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",obj
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
                                "cellWidth" :obj.get('WIDTH')
                                }]
                widths = [float(obj.get('WIDTH'))]
                heights = [float(obj.get('HEIGHT'))]
                paras = obj.findall('para')
                itexts = obj.findall('ITEXT')
                isGroupControl = obj.get('isGroupControl')
            else:
                #print "TABLEEEEEEEEEE", table
                itext = obj.findall('ITEXT')
                for abj in self.slaPageObjects():
                    gruppo = abj.get('GROUPS')
                    #try:
                        #gruppo = gruppo[0]
                    #except:
                        #gruppo = gruppo
                    if gruppo == table and (table not in tableList):
                        if abj.get('isGroupControl')=="0":
                            ##if abj.get("LeftLINK") == "-1":
                            #if abj.get("gXpos") == "0" or "0.00" in abj.get("gXpos")[0:4]:
                                #leftLink.append(abj.get("gXpos"))
                            #if abj.get("gYpos") == "0" or "0.00" in abj.get("gYpos")[0:4]:
                                #topLink.append(abj.get("gYpos"))
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
                            #if len(topLink) == 0:
                                #columns = 1
                            #else:
                                #columns= len(topLink)
                            columns = self.shitFunc(xpos)
                            #print "XPOOOOOOOOOOOOOS", xpos
                            #print "YPOSSSSSS", ypos
            #print "questa è la lista delle tabelle già parsate", tableList, table
            if table not in tableList:
                n_cells = self.shitFunc(ypos)*(columns or 1)
                groupDict[str(table).strip()] = {
                            'GROUPS': table,
                            'isTableItem': isTableItem2,
                            'isGroupControl':isGroupControl,
                            'cells': n_cells,
                            'rows': self.shitFunc(ypos),
                            'columns': columns,
                            'widths' :widths,
                            'heights':heights,
                            'ypos':ypos,
                            'xpos':xpos,
                            'ownPage' :ownPage,
                            'pfile':pfile2,
                            'iterproper':[],
                            'cellProperties':cellproperties,
                            'itexts' : list({} for i in range(0,columns)),
                            'para' : list({} for i in range(0,columns)),
                            'itextsobj':itexts,
                            'parasobj': paras,
                            'counters' :list(-1 for i in range(0,columns))}
                #print "DDDDDDDDDDDDDDDD", table, pfile2, isTableItem2,len(leftLink), columns, n_cells,
                tableList.append(table)
                widths = heights =ypos =  xpos = tableMod = topLink = ownPage = leftLink = itexts = cellproperties = paras =[]
                monoFoto = False
                propertiesList.append(groupDict)
        self.tablesProperties = propertiesList
        return propertiesList

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
                    if ch.replace(' ', '') == '':
                        continue
                    tags = Sla2pdfUtils.findTags(ch)
                    if tags is not None:
                        if tags not in vector:
                            vector.append(tags)
                        for k in tags.keys():
                            self.tagsTables[k] = group
                self.tablesTags[group] = vector
        #return (self.tablesTags, self.tagsTables)

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
        return self.iteratableGroups

    def scribusVersion(self):
        root = self.slaRootTag()
        self.slaversion = root.get('Version')
        print "VERSIONE FILE SLA", self.slaversion
        if self.slaversion == "1.3.4" or  "1.3.5" in self.slaversion:
            version=True
        else:
            version = False
        return version

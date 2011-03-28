# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

import xml.etree.cElementTree as ElementTree
import Sla2pdfUtils

class SlaParser(object):

    def __init__(self, slaFileName=None, pdfFolder=None, slafile=None):

        self.slaFileName = slaFileName
        self.pdfFolder = pdfFolder
        self.slafile = slafile
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
        self.root = self.doc.getroot()
        self.document = self.root.findall('DOCUMENT')[0]

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

    def findTablesProperties(self):
        """
        Questa Funzione crea un dizionario che ha come chiave il gruppo, sia nella
        sua forma originale che in quella modificata per poter distinguere immagini
        e campi monocella, come valori al momento ha tutto ciò che occorre per
        capire come sia composta la tabella, proprietà delle celle, numero delle colonne,
        formattazione.

        FIXME: Brutta la ripetizione dei campi per la gestione del monocella
        """
        #if self.tablesProperties:
            #return self.tablesProperties
        #else:
        oggetti = self.slaPageObjects()
        propertiesList = []
        tableList = []
        table= None
        monoFoto = False
        columns=1
        rows = 1
        n_cells = 1
        for obj in oggetti:
            groupDict = {}
            ownPage = []
            leftLink = []
            topLink = []
            tableMod = []
            cells = []
            table = obj.get('GROUPS')
            pfile2 = obj.get('PFILE')
            if table == "":
                xpos = [float(obj.get('XPOS'))]
                ypos = [float(obj.get('YPOS'))]
                isTableItem2 = obj.get('isTableItem')
                table = "noGroup" + str(xpos) + str(ypos)
                cells = [obj]
                isGroupControl = obj.get('isGroupControl')
            else: #QUESTA é UNA TABELLA
                for abj in self.slaPageObjects():
                    gruppo = abj.get('GROUPS')
                    if gruppo == table and (table not in tableList):
                        if abj.get('isGroupControl')=="0":
#                            coox = abj.get("gXpos")
#                            if coox == "0" or "0.0" in coox:
#                                coox = "0.0"
#                            leftLink.append(coox)
#                            cooy = abj.get("gYpos")
#                            if cooy =="0" or "0.0" in cooy:
#                                cooy = "0.0"
#                            topLink.append(cooy)
                            cells.append(abj)
                            coox = None
                            cooy = None
            #print "questa è la lista delle tabelle già parsate", tableList, table
            if table not in tableList:
                colonne = [round(float(x.get('gXpos')),3) for x in cells]
                righe = [round(float(x.get('gYpos')),3) for x in cells]
                columns = len(sorted(list(set(colonne))))
                rows = len(sorted(list(set(righe))))
                n_cells = columns*rows
                if len(cells) != n_cells:
                   print "ERRORE INTERPRETAZIONE LETTURA TABELLA", "COLONNE", colonne, "RIGHE", righe,"NCOL", columns,"NRIG", rows, "TOTCELL", columns*rows ,"GRUPPO", table, cells
                groupDict[str(table).strip()] = {
                            'GROUPS': table,
                            'n_cells': n_cells,
                            'rows': rows,
                            'columns': columns,
                            'cells':cells,
                            'pfile':pfile2}
                tableList.append(table)
                tableMod = ownPage = paras =trails= cells=[]
                leftLink = []
                topLink = []
                rows = 1
                columns = 1
                monoFoto = False
                propertiesList.append(groupDict)
        self.tablesProperties = propertiesList
        return propertiesList

    def getIteratableGroups(self,tablepropertys):
        """
        Questa funzione ha l'importante compito di creare una lista con i gruppi
        relativi alle tabelle che iterano ( righe e castelletto iva al momento )
        """
        iteratableGroups = []
        for group in tablepropertys:
            itexts = [z for z in [y for y in [x.findall('ITEXT') for x in group.values()[0]["cells"]]]]
            for i in itexts:
                for a in i:
                    if '(n).' in a.get("CH"):
                        if "%%%" in group.values()[0]["GROUPS"]:
                            groupname= str(group.values()[0]["GROUPS"].strip().split('%%%')[0])
                        else:
                            groupname = str(group.values()[0]["GROUPS"].strip())
                        if groupname not in iteratableGroups:
                            iteratableGroups.append(str(groupname))
#            print "GRUPPI ITERANTI", iteratableGroups
        return iteratableGroups

#    def scribusVersion(self):
##        root = self.slaRootTag()
##        self.slaversion = self.root.get('Version')
##        print "VERSIONE FILE SLA", self.slaversion
##        if self.slaversion == "1.3.4" or  "1.3.5" in self.slaversion:
##            version=True
##        else:
##            version = False
##        return version
#        return True

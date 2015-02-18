# -*- coding: utf-8 -*-

# Copyright (C) 2005-2015 by Promotux
# di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
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

from decimal import *
import xml.etree.cElementTree as ElementTree
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.lib.utils import *
import promogest.ui.Login
from fieldsDict import *


class PriceListModel:
    """PriceListModel class manages model's structure
        Ricarica il file pgx
    """

    def __init__(self, pathFile=None):
        self._file = pathFile
        self._fields = []
        self._defaultAttributes = {}
        myFieldsDict = {}
        if self._file is not None:
            root = self.parseFile('root')
            tree = self.parseFile('tree')
            if root.tag == 'model':
                self._name = root.attrib['name']
            parent_map = tree.getiterator()
            for p in parent_map:
                if p.tag == 'fieldsSeparator':
                    self._fieldsSeparator = p.attrib['value']
                elif p.tag == 'fieldsDelimiter':
                    self._fieldsDelimiter = p.attrib['value']
                elif p.tag == 'decimalSymbol':
                    self._decimalSymbol = p.attrib['value']
                elif p.tag == 'skipFirstLine':
                    if p.attrib['value'] == 'True':
                        self._skipFirstLine = True
                    else:
                        self._skipFirstLine = False
                elif p.tag == 'skipFirstColumn':
                    if p.attrib['value'] == 'True':
                        self._skipFirstColumn = True
                    else:
                        self._skipFirstColumn = False
                elif p.tag == 'field':
                    myFieldsDict[p.attrib['position']] = p.attrib['name']
                elif p.tag == 'default':
                    self._defaultAttributes[p.attrib['name']] = p.attrib['value']
            field_order = range(0, len(myFieldsDict.keys()))
            for p in field_order:
                self._fields.append(myFieldsDict[str(p)])

        else:
            self._name = 'Modello listino predefinito'
            self._fieldsSeparator = ','
            self._fieldsDelimiter = '"'
            self._decimalSymbol = '.'
            self._skipFirstColumn = False
            self._skipFirstLine = False
            self._fields = []
            self._defaultAttributes = {}

    def save(self, filename):
        """Saves the model into an xml file."""

        model_tag = Element("model")
        model_tag.attrib["name"] = self._name

        index = 0
        for n in self._fields:
            field_tag = SubElement(model_tag, "field")
            field_tag.attrib["name"] = n
            field_tag.attrib["position"] = str(index)
            index += 1

        fieldSeparatorTag = SubElement(model_tag, "fieldsSeparator")
        fieldSeparatorTag.attrib['value'] = str(self._fieldsSeparator)

        fieldsDelimiterTag = SubElement(model_tag, "fieldsDelimiter")
        fieldsDelimiterTag.attrib['value'] = str(self._fieldsDelimiter)

        decimalSymbolTag = SubElement(model_tag, "decimalSymbol")
        decimalSymbolTag.attrib['value'] = str(self._decimalSymbol)

        skipFirstLineTag = SubElement(model_tag, "skipFirstLine")
        skipFirstLineTag.attrib["value"] = str(self._skipFirstLine)

        skipFirstColumnTag = SubElement(model_tag, "skipFirstColumn")
        skipFirstColumnTag.attrib["value"] = str(self._skipFirstColumn)

        for d in self._defaultAttributes.keys():
            oneDefault = SubElement(model_tag, 'default')
            oneDefault.attrib["name"] = str(d)
            oneDefault.attrib["value"] = str(self._defaultAttributes[d])
        ElementTree(model_tag).write(filename, encoding='utf-8')

    def parseFile(self, returnObject):
        """Parses xml file and returns, according to the value of returnObject,
        the entire tree or the root element of the tree"""
        file = open(self._file, 'r')
        tree = parse(file)
        if returnObject == 'root':
            root = tree.getroot()
            return root
        elif returnObject == 'tree':
            return tree

    def setDefaultFields(self):
        obbligatoryFields = ['Famiglia', 'Categoria', 'Aliquota iva',
                                                                'Unita base']
        for f in obbligatoryFields:
            if f not in self._fields:
                if f not in self._defaultAttributes.keys():
                    self._defaultAttributes[f] = None
            else:
                if f in self._defaultAttributes.keys():
                    try:
                        retVal = self._defaultAttributes.pop(f)
                    except:
                        print 'ATTENZIONE! si è cercato di rimuovere un campo inesistente da un modello di importazione listini.'
        return self._defaultAttributes.keys()

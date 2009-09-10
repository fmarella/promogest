# -*- coding: UTF-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import re, string, decimal
from decimal import *
import gtk, gobject, os
from datetime import datetime
import xml.etree.cElementTree as ElementTree
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.ui.AnagraficaListini import AnagraficaListini
from promogest.ui.AnagraficaAliquoteIva import AnagraficaAliquoteIva
from promogest.ui.AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
from promogest.ui.AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
from promogest.ui.AnagraficaFornitori import AnagraficaFornitori
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
import promogest.ui.Login
from fieldsDict import *

class PriceListModel:
    """PriceListModel class manages model's structure"""
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

        skipFirstLineTag = SubElement(model_tag,"skipFirstLine")
        skipFirstLineTag.attrib["value"] = str(self._skipFirstLine)

        skipFirstColumnTag = SubElement(model_tag,"skipFirstColumn")
        skipFirstColumnTag.attrib["value"] = str(self._skipFirstColumn)

        for d in self._defaultAttributes.keys():
            oneDefault = SubElement(model_tag,'default')
            oneDefault.attrib["name"] = str(d)
            oneDefault.attrib["value"] = str(self._defaultAttributes[d])
        ElementTree(model_tag).write(filename, encoding='utf-8')

    def parseFile(self,returnObject):
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
        obbligatoryFields = ['Famiglia','Categoria','Aliquota iva','Unita base']
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
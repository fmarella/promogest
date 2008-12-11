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
from ProductFromCSV import ProductFromCsv
from fieldsDict import *


class ImportPreview(GladeWidget):
    """create a preview window to check that import is being executed correctly"""

    # Table is the csv file data
    # Model is a priceListModel instance
    # ProductList is a list of dictionary that came from csv file
    # PromoPriceList is an existing "Listino" in the database. (what is it for?)
    def __init__(self, mainWindow, table, PLModel, productList, promoPriceList,Fornitore,data_listino):
        GladeWidget.__init__(self, 'import_preview_window')
        self.import_preview_window.set_title('Anteprima Importazione Dati')
        self._mainWindow = mainWindow
        self.window = self.getTopLevel()
        self.table = table
        self.PLModel = PLModel
        self.productList = productList
        self.promoPriceList = promoPriceList
        self.fornitore = Fornitore
        self.data_listino = data_listino
        self.draw()

    def draw(self):
        self.treeview = self.articoli_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)
        fields = self.PLModel._fields
        model = getDynamicStrListStore(len(fields))
        self.treeview.set_model(model)

        nc = 0
        for f in fields:
            column = gtk.TreeViewColumn(f, rendererSx, text=nc)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(True)
            column.set_min_width(250)
            self.treeview.append_column(column)
            nc += 1
        remodel = self.treeview.get_model()

        for row in self.table:
            remodel.append(row)

    def on_import_preview_confirm_clicked(self, button):
        import csv
        savedlines = 0
        err_count = 0
        csvErrorFile = csv.DictWriter(file(Environment.documentsDir+'/import_error_list.csv', 'wb'), fieldnames=self.PLModel._fields,dialect='excel')
        for product in self.productList:
            productFromCsv = ProductFromCsv(product=product, PLModel=self.PLModel, promoPriceList=self.promoPriceList, idfornitore=self.fornitore, dataListino=self.data_listino)
            #try: #product data dictionary is transmitted to the method that will generate (or update) the corrispondent product
            productFromCsv.save()
            #except:
                #err_count += 1
                #csvErrorFile.writerow(product)
            savedlines += 1
        if err_count > 0:
            msg = """Si è verificato un errore nel salvataggio dei dati di qualche prodotto.
È stato creato un nuovo file CSV con questi prodotti nella cartella documenti.
Verificare gli errori nel file e ritentare l'importazione"""
            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                   gtk.MESSAGE_ERROR,
                                                   gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            savedlines = savedlines - err_count
        print u'Import Procedure completed.'
        print u'Articoli salvati: '+str(savedlines)
        print u'Articoli di cui è fallito l\'import (completamente): '+str(err_count)
        if savedlines > 0:
            msg = u'Operazione completata.\nsono stati importati/aggiornati '+str(savedlines)+' articoli.'

            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                                                                gtk.MESSAGE_INFO,
                                                                gtk.BUTTONS_OK, msg)
            response = overDialog.run()
            overDialog.destroy()
            self.window.destroy()
            self._mainWindow.show_all()
        else:
            msg = u'Nessun articolo aggiornato/importato.'

            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                                                                gtk.MESSAGE_INFO,
                                                                gtk.BUTTONS_OK, msg)
            response = overDialog.run()
            overDialog.destroy()
        if response == gtk.BUTTONS_OK:
            self.window.destroy()
            self._mainWindow.show_all()
        else:
            self.window.destroy()
            self._mainWindow.show_all()

    def on_import_preview_window_close(self, widget, event=None):
        self.window.destroy()
        self._mainWindow.show_all()

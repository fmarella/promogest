# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

import csv
from decimal import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *
import promogest.ui.Login
from ProductFromCSV import ProductFromCsv
from fieldsDict import *


class ImportPreview(GladeWidget):
    """create a preview window to check that import is being executed correctly
    Table is the csv file data
    Model is a priceListModel instance
    ProductList is a list of dictionary that came from csv file
    PromoPriceList is an existing "Listino" in the database.(what is it for?)
    """

    def __init__(self, mainWindow, table, PLModel, productList, promoPriceList,
                                                    Fornitore, data_listino):
        GladeWidget.__init__(self, 'import_preview_window')
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
        """ Dynamic creation of a trevew model
        """
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
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
        """ cb di controllo dell'inizio delll'importazione"""
        savedlines = 0
        err_count = 0
        csvErrorFile = csv.DictWriter(file(Environment.documentsDir+\
                            '/import_error_list.csv', 'wb'),
                             fieldnames=self.PLModel._fields, dialect='excel')
        print "ISTANZIO LA CLASSE E PREPARO L'AMBIENTE "
        productFromCsv = ProductFromCsv(listaRighe=self.productList,
                                PLModel=self.PLModel,
                                promoPriceList=self.promoPriceList,
                                idfornitore=self.fornitore,
                                dataListino=self.data_listino,
                                createData= True)
        print "PRONTO A CICLARE RIGA PER RIGA"
        for product in self.productList: #andiamo a salvare il dato ....
            pbar(self.pbar,parziale=self.productList.index(product), totale=len(self.productList), text="IMPORTO CSV")
            ProductFromCsv(PLModel=self.PLModel,
                            promoPriceList=self.promoPriceList,
                            idfornitore=self.fornitore,
                            dataListino=self.data_listino,).save(product)
            savedlines += 1
        pbar(self.pbar,stop=True)
        if err_count > 0:
            msg = """Si è verificato un errore nel salvataggio dei dati di qualche prodotto.
È stato creato un nuovo file CSV con questi prodotti nella cartella documenti.
Verificare gli errori nel file e ritentare l'importazione"""
            messageError(msg=msg, transient=self.getTopLevel())
            savedlines = savedlines - err_count
        print u'Import Procedure completed.'
        print u'Articoli salvati: '+str(savedlines)
        print u'Articoli di cui è fallito l\'import (completamente): '+\
                                                            str(err_count)
        if savedlines > 0:
            msg = u'Operazione completata.\nsono stati importati/aggiornati '+\
                                                str(savedlines)+' articoli.'
            messageInfo(msg=msg, transient=self.getTopLevel())
            self.window.destroy()
            self._mainWindow.show_all()
        else:
            msg = u'Nessun articolo aggiornato/importato.'
            messageInfo(msg=msg, transient=self.getTopLevel())
            self.window.destroy()
            self._mainWindow.show_all()


    def on_import_preview_window_close(self, widget, event=None):
        self.window.destroy()
        self._mainWindow.show_all()

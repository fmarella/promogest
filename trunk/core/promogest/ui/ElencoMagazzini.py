# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject
from GladeWidget import GladeWidget

from promogest import Environment
#from promogest.dao.Dao import Dao
#import promogest.dao.Magazzino
from promogest.dao.Magazzino import Magazzino

from utils import *



class ElencoMagazzini(GladeWidget):
    """ Elenco magazzini """

    def __init__(self, mainWindow,aziendaStr):
        self._mainWindow = mainWindow
        self.aziendaStr = aziendaStr
        self._currentDao = None
        GladeWidget.__init__(self, 'elenco_magazzini_frame', fileName='_elenco_magazzini_elements.glade')
        self.orderBy = 'denominazione'
        self.draw()


    def draw(self):
        # Colonne della Treeview dell' elenco
        treeview = self.elenco_magazzini_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'localita')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        treeview.set_search_column(1)

        model = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str)
        treeview.set_model(model)

        self.refresh()


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'elenco """
        self._elenco_magazzini_elements.show_all()


    def refresh(self):
        # Aggiornamento Treeview
        model = self.elenco_magazzini_treeview.get_model()
        model.clear()

        mags = Magazzino().select(offset=None, batchSize=None)
        for m in mags:
            model.append((m,
                          (m.denominazione or ''),
                          (m.localita or '')))


    def _changeOrderBy(self, widget, campi):
        self.orderBy = campi
        self.refresh()


    def on_elenco_magazzini_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            self._currentDao = model.get_value(iterator,0)


    def on_magazzini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        denominazione = None
        if self._currentDao is not None:
            denominazione = self._currentDao.denominazione
        from AnagraficaMagazzini import AnagraficaMagazzini
        anag = AnagraficaMagazzini(denominazione, self.aziendaStr)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)


    def on_stoccaggi_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        idMagazzino = None
        if self._currentDao is not None:
            idMagazzino = self._currentDao.id
        from AnagraficaStoccaggi import AnagraficaStoccaggi
        anag = AnagraficaStoccaggi(None, idMagazzino, self.aziendaStr)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)


    def on_movimenti_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        idMagazzino = None
        if self._currentDao is not None:
            idMagazzino = self._currentDao.id
        from AnagraficaMovimenti import AnagraficaMovimenti
        anag = AnagraficaMovimenti(idMagazzino, self.aziendaStr)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)


    def on_inventario_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if "Inventario" in Environment.modulesList:
            return


            if self._currentDao is not None:
                idMagazzino = self._currentDao.id
                from promogest.modules.Inventario.ui.GestioneInventario import GestioneInventario
                anag = GestioneInventario(idMagazzino)
                anagWindow = anag.getTopLevel()

                showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)
            else:
                toggleButton.set_active(False)
                obligatoryField(self._mainWindow,
                                None,
                                '\nSelezionare un magazzino !')
        else:
            fenceDialog()
            toggleButton.set_active(False)

    def on_statistiche_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if "Statistiche" in Environment.modulesList:
            #return

            if self._currentDao is not None:
                idMagazzino = self._currentDao.id
                from promogest.modules.Statistiche.ui.StatisticheMagazzino import StatisticheMagazzino
                anag = StatisticheMagazzino(idMagazzino)
                anagWindow = anag.getTopLevel()

                showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)
            else:
                toggleButton.set_active(False)
                obligatoryField(self._mainWindow,
                                None,
                                '\nSelezionare un magazzino !')
        else:
            fenceDialog()
            toggleButton.set_active(False)

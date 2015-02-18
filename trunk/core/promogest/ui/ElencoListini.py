# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest import Environment
from promogest.dao.Listino import Listino
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import *


class ElencoListini(GladeWidget):
    """ Elenco listini """

    def __init__(self, mainWindow, aziendaStr):
        self._mainWindow = mainWindow
        self.aziendaStr = aziendaStr
        self._currentDao = None
        GladeWidget.__init__(self, root='elenco_listini_frame',
                        path='_elenco_listini_elements.glade')
        self.orderBy = 'denominazione'

    def draw(self):
        # Colonne della Treeview dell' elenco
        listini = Listino().select(visibileCheck=True, batchSize=None)
        for l in listini:
            l.visible = True
            l.persist()
        self.refresh()
        return self

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'elenco """
        self._elenco_listini_elements.show_all()

    def refresh(self):
        # Aggiornamento Treeview
        visibili = self.visibile_list_check.get_active()
        if visibili:
            visibili = None
        else:
            visibili = True
        self.elenco_listini_listore.clear()

        liss = Listino().select(
                                visibili = visibili,
                                orderBy='denominazione',
                                batchSize=None,
                                offset=None)
        for l in liss:
            self.elenco_listini_listore.append([l,
                          l.denominazione or '',
                          l.descrizione or '',
                          dateToString(l.data_listino),
                          str(len(l.listinoarticolo))])

    def _changeOrderBy(self, widget, campi):
        self.orderBy = campi
        self.refresh()

    def on_elenco_listini_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        if sel:
            (model, iterator) = sel.get_selected()
            if iterator is not None:
                self._currentDao = model.get_value(iterator,0)

    def on_elenco_listini_treeview_row_activated(self, treeview, path, column):
        self.articoli_listino_togglebutton.set_active(True)

    def on_stampa_frontaline_togglebutton_clicked(self, toggleButton):
        if posso("LA"):
            from promogest.modules.Label.ui.ManageLabelsToPrint import ManageLabelsToPrint
            a = ManageLabelsToPrint(mainWindow=self,daos=[])
            anagWindow = a.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            fencemsg()

    def on_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        denominazione = None
        #if self._currentDao:
            #denominazione = self._currentDao.denominazione
        from AnagraficaListini import AnagraficaListini
        anag = AnagraficaListini(denominazione, self.aziendaStr)
        anagWindow = anag.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()
        if toggleButton.get_active():
            toggleButton.set_active(False)

    def on_articoli_listino_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        idListino = None
        if self._currentDao:
            idListino = self._currentDao.id
            from AnagraficaListiniArticoli import AnagraficaListiniArticoli
            anag = AnagraficaListiniArticoli(None, idListino, self.aziendaStr)
            anagWindow = anag.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            messageInfo(msg= "ATTENZIONE!,\n Selezionare un Listino dalla lista")
        if toggleButton.get_active():
            toggleButton.set_active(False)

    def on_importazione_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("IPL"):
            from promogest.modules.ImportPriceList.ui.ImportPriceList import ImportPriceList
            idListino = None
            if self._currentDao:
                idListino = self._currentDao.id
            anag = ImportPriceList(self._mainWindow)
            anagWindow = anag.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
            if toggleButton.get_active():
                toggleButton.set_active(False)
        else:
            fencemsg()
            toggleButton.set_active(False)

    def on_aggiorna_listini_button_clicked(self, button):
        self.refresh()

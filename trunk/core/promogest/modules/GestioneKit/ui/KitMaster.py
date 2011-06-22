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

import gtk
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.modules.GestioneKit.dao.ArticoloKit import ArticoloKit
from promogest.dao.Articolo import Articolo

class KitMaster(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self, dao):
        self._articolo_master = dao
        self._htmlTemplate = None
        self.editRiga = None

        GladeWidget.__init__(self, 'master_kit_window',
                fileName="GestioneKit/gui/kit_master.glade", isModule=True)
        self._window = self.master_kit_window
        self.placeWindow(self._window)
        self.draw()

    def draw(self):
        stringa = '<span size="12000">ARTICOLO: ' + b(self._articolo_master.codice + " - "+ self._articolo_master.denominazione) +"</span>"
        self.articolo_master_label.set_markup(stringa)
        self.quantita_componente_kit_entry.set_text("1")
        self._refresh()

    def _refresh(self):
        self.articoli_componenti_listore.clear()
        for art in self._articolo_master.articoli_kit:
            articonte = leggiArticolo(art.id_articolo_filler)
            self.articoli_componenti_listore.append((
            art,
            dateToString(art.data_inserimento),
            articonte["codice"],
            articonte["denominazione"],
            str(art.quantita or 0),
            str(art.attivo) or 0,
            art.note,
            "",
            ))
        for artcompo  in self._articolo_master.componente_in_kit:
            articonte2 = leggiArticolo(artcompo.id_articolo_wrapper)
            self.articolo_componente_listore.append((
            artcompo,
            dateToString(artcompo.data_inserimento),
            articonte2["codice"],
            articonte2["denominazione"],
            str(artcompo.quantita or 0),
            str(artcompo.attivo) or 0,
            artcompo.note,
            "",
            ))

    def on_aggiungi_componente_button_clicked(self, button):
        """ Aggiunge la riga con i campi di denominazione e valore cassa o banca
            entrata o uscita """
        if self.id_articolo_componente_customcombobox.getId() == None:
            obligatoryField(self.dialogTopLevel, self.self.id_articolo_componente_customcombobox,
            msg="Campo obbligatorio: ARTICOLO!")

        if self.data_aggiunta_componente_datewidget.get_text() == "" or \
            self.data_aggiunta_componente_datewidget.get_text() == None:
            obligatoryField(self.dialogTopLevel, self.data_aggiunta_componente_datewidget,
            msg="Campo obbligatorio: DATA AGGIUNTA!")

        model = self.articoli_componenti_listore
        if self.editRiga:
            riga = self.editRiga
        else:
            riga = ArticoloKit()
        riga.numero = 1
        data_inserimento = self.data_aggiunta_componente_datewidget.get_text()
        riga.data_inserimento = stringToDate(data_inserimento)
        note = self.note_componente_kit_entry.get_text()
        riga.note = note
        quantita = Decimal(self.quantita_componente_kit_entry.get_text().replace(",", ".").strip() or 0)
        riga.quantita = quantita
        attivo = self.attivo_componente_check.get_active()
        riga.attivo = attivo
        riga.id_articolo_filler = self.id_articolo_componente_customcombobox.getId()
        riga.id_articolo_wrapper = self._articolo_master.id
        arti = leggiArticolo(self.id_articolo_componente_customcombobox.getId())
        col_tipo = ""
        dati = (riga,
                        data_inserimento,
                        arti["codice"],
                        arti["denominazione"],
                        str(quantita or 0 ),
                        str(attivo),
                        note,
                        col_tipo)
        if self.editRiga:
            self.rigaIter[0] = riga
            self.rigaIter[1] = data_inserimento
            self.rigaIter[2] = arti["codice"] or ""
            self.rigaIter[3] = arti["denominazione"]
            self.rigaIter[4] =  str(quantita or 0 )
            self.rigaIter[5] = str(attivo)
            self.rigaIter[6] = note
        else:
            model.append(dati)

        self.articoli_componenti_treeview.set_model(model)
        self.editRiga = None
        self.clear()


    def clear(self):
        self.quantita_componente_kit_entry.set_text("")
        self.note_componente_kit_entry.set_text("")
        self.data_aggiunta_componente_datewidget.set_text("")
        self.id_articolo_componente_customcombobox.set_active(-1)

    def on_articoli_componenti_treeview_row_activated(self, treeview, path, column):
        sel = self.articoli_componenti_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model
        self.data_aggiunta_componente_datewidget.set_text(self.rigaIter[1])
        self.quantita_componente_kit_entry.set_text(self.rigaIter[4])
        self.id_articolo_componente_customcombobox.setId(self.rigaIter[0].id_articolo_filler)
        self.editRiga = self.rigaIter[0]
        self.note_componente_kit_entry.set_text(self.rigaIter[6])

    def on_elimina_componente_button_clicked(self, button):
        rpn = None
        if self.editRiga:
            dao = ArticoloKit().getRecord(id=self.editRiga.id)
            if dao:
                dao.delete()
            self._editModel.remove(self._editIterator)
            self.clear()

    def on_chiudi_kit_button_clicked(self, button):
        self.destroy()

    def on_ok_kit_button_clicked(self, button):
        for m in self.articoli_componenti_listore:
            m[0].persist()
        self.clear()

    def on_articolo_componente_treeview_row_activated(self, treeview, path, column):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        articolocomp = self.rigaIter[0]
        articolo = Articolo().getRecord(id=articolocomp.id_articolo_wrapper)
        anag = KitMaster(articolo)
        anagWindow = anag.getTopLevel()
        anagWindow.show_all()
        #showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

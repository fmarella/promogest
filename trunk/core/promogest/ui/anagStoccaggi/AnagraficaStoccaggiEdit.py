# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.dao.Stoccaggio import Stoccaggio
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *

if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *


class AnagraficaStoccaggiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'anagrafica_stoccaggi_detail_table',
                'Dati stoccaggi',
                gladeFile='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_customcombobox
        if not posso("PW"):
            self.promowear_frame.destroy()

    def draw(self, cplx=False):
        self.id_articolo_customcombobox.setSingleValue()

        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                     on_id_magazzino_customcombobox_clicked)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_customcombobox.set_sensitive(False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                                                self._anagrafica._idMagazzino)
            self.id_magazzino_customcombobox.set_sensitive(False)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Stoccaggio()
            self.newDao = True
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Stoccaggio().getRecord(id=dao.id)
            self.newDao = False
        self._refresh()
        return self.dao

    def _refresh(self):
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        self.id_magazzino_customcombobox.combobox.set_active(-1)
        self.id_magazzino_customcombobox.set_sensitive(True)
        if self.dao.id_magazzino is None:
            if self._anagrafica._magazzinoFissato:
                self.dao.id_magazzino = self._anagrafica._idMagazzino
                self.id_magazzino_customcombobox.set_sensitive(False)
        else:
            self.id_magazzino_customcombobox.set_sensitive(False)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                                                    self.dao.id_magazzino)
        self.scorta_minima_entry.set_text(str(self.dao.scorta_minima or 0))
        self.livello_riordino_entry.set_text(
                    str(self.dao.livello_riordino or 0))
        self.data_fine_scorte_entry.set_text(
                    dateToString(self.dao.data_fine_scorte))
        self.data_prossimo_ordine_entry.set_text(
                    dateToString(self.dao.data_prossimo_ordine))
        if posso("PW"):
            self.colore_label.set_text(self.dao.denominazione_colore or "")
            self.stagione_label.set_text(self.dao.stagione or "")
            self.genere_label.set_text(self.dao.genere or "")
            try:
                tggruppotaglia = self.dao.denominazione_gruppo_taglia\
                                             + " " + \
                                            self.dao.denominazione_taglia
            except:
                tggruppotaglia = ""
            self.taglia_label.set_markup(tggruppotaglia)

    def saveDao(self, tipo=None):
        if findIdFromCombobox(
                        self.id_magazzino_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                    self.id_magazzino_customcombobox.combobox)
        idMagazzino = findIdFromCombobox(
                    self.id_magazzino_customcombobox.combobox)
        idArticolo = self.id_articolo_customcombobox.getId()
        if not idArticolo:
            obligatoryField(self.dialogTopLevel,
                    self.id_articolo_customcombobox)
        elif idArticolo:
            a = Stoccaggio().select(idArticolo=idArticolo,
                                    idMagazzino=idMagazzino)
            if a:
                a[0].scorta_minima = int(
                    self.scorta_minima_entry.get_text() or 0)
                a[0].livello_riordino = int(
                    self.livello_riordino_entry.get_text() or 0)
                a[0].data_fine_scorte = stringToDate(
                    self.data_fine_scorte_entry.get_text())
                a[0].data_prossimo_ordine = stringToDate(
                    self.data_prossimo_ordine_entry.get_text())
                a[0].persist()
                return
        self.dao.id_magazzino = idMagazzino
        self.dao.id_articolo = idArticolo
        self.dao.scorta_minima = int(
                    self.scorta_minima_entry.get_text() or 0)
        self.dao.livello_riordino = int(
                    self.livello_riordino_entry.get_text() or 0)
        self.dao.data_fine_scorte = stringToDate(
                    self.data_fine_scorte_entry.get_text())
        self.dao.data_prossimo_ordine = stringToDate(
                    self.data_prossimo_ordine_entry.get_text())
        self.dao.persist()

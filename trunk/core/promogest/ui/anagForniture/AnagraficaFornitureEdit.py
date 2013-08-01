# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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

from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit

from promogest import Environment
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.dao.Articolo import Articolo
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaFornitureEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle forniture """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
            anagrafica,
            'Dati fornitura',
            root='anagrafica_forniture_detail_table',
            path='_anagrafica_fornitura_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_articolo_fornitore_entry
        self._percentualeIva = 0
        self.taglia_colore_table.hide()
        self.taglia_colore_table.set_no_show_all(True)
        self.number_format = '%-14.'+ str(setconf("Numbers", "decimals")) +'f'

    def draw(self,cplx=False):
        #self.id_articolo_customcombobox.setSingleValue()
        #self.id_articolo_customcombobox.setOnChangedCall(self.on_id_articolo_customcombobox_changed)
        #self.id_fornitore_customcombobox.setSingleValue()

        self.sconti_widget.button.connect('toggled',
                                        self.on_sconti_widget_button_toggled)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_customcombobox.set_sensitive(False)
            res = self.id_articolo_customcombobox.getData()
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text(str(mN(self._percentualeIva,0)) + ' %')
        if self._anagrafica._fornitoreFissato:
            self.id_fornitore_customcombobox.setId(self._anagrafica._idFornitore)
            self.id_fornitore_customcombobox.set_sensitive(False)

        #fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
        #self.id_multiplo_customcombobox.connect('clicked',
                                                #self.on_id_multiplo_customcombobox_button_clicked)

        self.prezzo_lordo_entry.connect('focus_out_event', self._calcolaPrezzoNetto)


    def on_id_multiplo_customcombobox_button_clicked(self, widget, button):
        on_id_multiplo_customcombobox_clicked(widget, button, self.id_articolo_customcombobox.getId())


    def on_id_articolo_customcombobox_changed(self):
        res = self.id_articolo_customcombobox.getData()
        if res:
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text('%5.2f' % self._percentualeIva + ' %')
            #fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
            if posso("PW"):
                self._refreshTagliaColore(res["id"])

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = Fornitura()
        self._refresh()
        return self.dao

    def _refresh(self):
        self.clear()
        #self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        res = self.id_articolo_customcombobox.getData()
        self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
        self._percentualeIva = res["percentualeAliquotaIva"]
        self.percentuale_aliquota_iva_label.set_text('%5.2f' % self._percentualeIva + ' %')
        #self.id_fornitore_customcombobox.refresh(clear=True, filter=False)
        self.id_fornitore_customcombobox.set_sensitive(True)
        if self.dao.id_fornitore is None:
            if self._anagrafica._fornitoreFissato:
                self.dao.id_fornitore = self._anagrafica._idFornitore
                self.id_fornitore_customcombobox.set_sensitive(False)
        else:
            self.id_fornitore_customcombobox.set_sensitive(False)
        self.id_fornitore_customcombobox.setId(self.dao.id_fornitore)
        self.codice_articolo_fornitore_entry.set_text(self.dao.codice_articolo_fornitore or '')
        self.prezzo_lordo_entry.set_text(self.number_format % float(self.dao.prezzo_lordo or 0))
        self.prezzo_netto_label.set_text(self.number_format % float(self.dao.prezzo_netto or 0))
        self.scorta_minima_entry.set_text('%-6d' % int(self.dao.scorta_minima or 0))
        self.tempo_arrivo_merce_entry.set_text('%-6d' % float(self.dao.tempo_arrivo_merce or 0))
        self.fornitore_preferenziale_checkbutton.set_active(self.dao.fornitore_preferenziale or False)
        self.data_fornitura_entry.set_text(dateToString(self.dao.data_fornitura))
        self.data_prezzo_entry.set_text(dateToString(self.dao.data_prezzo))

        self.lotto_entry.set_text(self.dao.numero_lotto or '')
        #fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self.id_articolo_customcombobox.getId())
        #findComboboxRowFromId(self.id_multiplo_customcombobox.combobox,
                              #self.dao.id_multiplo)
        self.sconti_widget.setValues(self.dao.sconti, self.dao.applicazione_sconti)
        self._calcolaPrezzoNetto()
        if posso("PW"):
            self._refreshTagliaColore(self.dao.id_articolo)

    def _refreshTagliaColore(self, idArticolo):
        articoloTagliaColore = Articolo().getRecord(id=idArticolo)
        self.taglia_colore_table.hide()
        if articoloTagliaColore is not None:
            gruppoTaglia = articoloTagliaColore.denominazione_gruppo_taglia or ''
            taglia = articoloTagliaColore.denominazione_taglia or ''
            colore = articoloTagliaColore.denominazione_colore or ''
            anno = articoloTagliaColore.anno or ''
            stagione = articoloTagliaColore.stagione or ''
            genere = articoloTagliaColore.genere or ''
            self.taglia_label.set_markup('<span weight="bold">%s (%s)  %s</span>'
                                         % (taglia, gruppoTaglia, genere))
            self.colore_label.set_markup('<span weight="bold">%s</span>'
                                         % (colore))
            self.stagione_label.set_markup('<span weight="bold">%s  %s</span>'
                                           % (stagione, anno))
            self.taglia_colore_table.show()


    def _calcolaPrezzoNetto(self, widget = None, event = None):
        self.prezzo_netto_label.set_text('')
        if self.prezzo_lordo_entry.get_text() == '':
            self.prezzo_lordo_entry.set_text(self.number_format % float(0))
        prezzoLordo = prezzoNetto = float(self.prezzo_lordo_entry.get_text())
        sconti = self.sconti_widget.getSconti()
        applicazione = self.sconti_widget.getApplicazione()
        for s in sconti:
            if s["tipo"] == 'percentuale':
                if applicazione == 'scalare':
                    prezzoNetto = prezzoNetto * (1 - float(s["valore"]) / 100)
                elif applicazione == 'non scalare':
                    prezzoNetto = prezzoNetto - prezzoLordo * float(s["valore"]) / 100
            elif s["tipo"] == 'valore':
                prezzoNetto = prezzoNetto - float(s["valore"])
        self.prezzo_netto_label.set_text(self.number_format % float(prezzoNetto or 0))

    def clear(self):
        ####################self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        ####################self.id_fornitore_customcombobox.refresh(clear=True, filter=False)
        self.data_prezzo_entry.set_text('')
        self.data_fornitura_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        self.prezzo_lordo_entry.set_text('')
        self.prezzo_netto_label.set_text('')
        self.scorta_minima_entry.set_text('')
        self.tempo_arrivo_merce_entry.set_text('')
        self.fornitore_preferenziale_checkbutton.set_active(False)
        self.lotto_entry.set_text('')

    def saveDao(self, tipo=None):
        if self.id_articolo_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)

        if self.id_fornitore_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_fornitore_customcombobox)

        if (self.prezzo_lordo_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.prezzo_lordo_entry)

        if (self.prezzo_netto_label.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.prezzo_netto_label)

        self.dao.id_articolo = self.id_articolo_customcombobox.getId()
        self.dao.id_fornitore = self.id_fornitore_customcombobox.getId()
        self.dao.data_prezzo = stringToDate(self.data_prezzo_entry.get_text())
        self.dao.data_fornitura = stringToDate(self.data_fornitura_entry.get_text())
        self.dao.codice_articolo_fornitore = self.codice_articolo_fornitore_entry.get_text()
        #self.dao.id_multiplo = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        self.dao.prezzo_lordo = float(self.prezzo_lordo_entry.get_text())
        self.dao.prezzo_netto = float(self.prezzo_netto_label.get_text())
        self.dao.scorta_minima = int(self.scorta_minima_entry.get_text() or 1)
        self.dao.tempo_arrivo_merce = int(self.tempo_arrivo_merce_entry.get_text() or 1)
        self.dao.fornitore_preferenziale = self.fornitore_preferenziale_checkbutton.get_active()
        self.dao.percentuale_iva = float(self._percentualeIva)
        self.dao.numero_lotto = self.lotto_entry.get_text()

        sconti = []
        self.dao.applicazione_sconti = self.sconti_widget.getApplicazione()
        for s in self.sconti_widget.getSconti():
            daoSconto = ScontoFornitura()
            daoSconto.id_fornitura = self.dao.id
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti.append(daoSconto)
        self.dao.sconti = sconti
        self.dao.persist()


    def on_sconti_widget_button_toggled(self, button):
        if not button.get_property('active'):
            self._calcolaPrezzoNetto()

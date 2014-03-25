# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2014 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from promogest.ui.gtk_compat import *
import datetime
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit

from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.lib.utils import *
from utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId

if posso("PW"):
    from promogest.modules.PromoWear.ui.AnagraficaListinoArticoliExpand import *


class AnagraficaListiniArticoliEdit(AnagraficaEdit):
    """
    Modifica un record dell'anagrafica degli articoli dei listini
    """
    def __init__(self, anagrafica):
        """ Gestione la modifica e l'editing dei listino articolo """
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati articolo nel listino',
                                root='anagrafica_listini_articoli_detail_table',
                                path='_anagrafica_listini_articoli_elements.glade')
        self._widgetFirstFocus = self.id_articolo_customcombobox
        self._percentualeIva = 0
        if not posso("PW"):
            self.taglia_colore_table.hide()
            self.taglia_colore_table.set_no_show_all(True)

        decimals = int(setconf(key="decimals", section="Numbers"))
        self.nformat = '%-14.' + str(decimals) + 'f'

    def on_sconti_dettaglio_widget_button_toggled(self, button):
        """ Gestione sconti dettaglio  con custom Widget """
        if button.get_property('active') is True:
            return
        _scontoDettaglio= self.sconti_dettaglio_widget.getSconti()

    def on_sconti_ingrosso_widget_button_toggled(self, button):
        """ Gestione sconti dettaglio  con custom Widget """
        if button.get_property('active') is True:
            return
        _scontoIngrosso= self.sconti_ingrosso_widget.getSconti()


    def on_calcola_costo_ultimo_da_dettaglio_button_clicked(self, button):
        #self.calcolaDettaglioDaRicarico()
        cu= calcolaCostoUltimodaDettaglio(dettaglio=self.prezzo_dettaglio_entry.get_text(),
                                        ricarico= self.percentuale_ricarico_dettaglio_entry.get_text(),
                                        iva= self._percentualeIva)
        self.ultimo_costo_entry.set_text('%-6.3f' % cu)

    def on_calcola_costo_ultimo_da_ingrosso_button_clicked(self, button):
        #self.calcolaDettaglioDaRicarico()
        cu= calcolaCostoUltimodaIngrosso(ingrosso=self.prezzo_ingrosso_entry.get_text(),
                                        ricarico= self.percentuale_ricarico_ingrosso_entry.get_text(),
                                        )
        self.ultimo_costo_entry.set_text('%-6.3f' % cu)


    def calcolaPercentualiDettaglio(self, widget=None, event=None):
        """ calcolaPercentualiDettaglio """
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(
                                        self.ultimo_costo_entry.get_text(),
                                        self.prezzo_dettaglio_entry.get_text(),
                                        self._percentualeIva))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(
                                        self.ultimo_costo_entry.get_text(),
                                        self.prezzo_dettaglio_entry.get_text(),
                                        self._percentualeIva))

    def confermaCalcolaPercentualiDettaglio(self, widget=None, event=None):
        """ confermaCalcolaPercentualiDettaglio """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaPercentualiDettaglio()

    def calcolaPercentualiIngrosso(self, widget=None, event=None):
        """ calcolaPercentualiIngrosso """
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(
                                    self.ultimo_costo_entry.get_text(),
                                    self.prezzo_ingrosso_entry.get_text()))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(
                                    self.ultimo_costo_entry.get_text(),
                                    self.prezzo_ingrosso_entry.get_text()))

    def confermaCalcolaPercentualiIngrosso(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaPercentualiIngrosso()

    def aggiornaCostoIvato(self, widget=None, event=None):
        """ """
        self.ultimo_costo_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                                self.ultimo_costo_entry.get_text(),
                                                self._percentualeIva))
        return False

    def aggiornaDaCosto(self, widget=None, event=None):
        """        """
        self.aggiornaCostoIvato()

    def confermaAggiornaDaCosto(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.aggiornaDaCosto()

    def calcolaDettaglioDaRicarico(self, widget=None, event=None):
        """        """
        prezzoDettaglio=self.nformat % calcolaListinoDaRicarico(
                                        self.ultimo_costo_entry.get_text(),
                                        self.percentuale_ricarico_dettaglio_entry.get_text(),
                                        self._percentualeIva)
        self.prezzo_dettaglio_entry.set_text(prezzoDettaglio)
        self.prezzo_dettaglio_noiva_label.set_text(self.nformat % calcolaPrezzoIva(
                                                                prezzoDettaglio,
                                                                ((-1)*self._percentualeIva)))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(
                                        self.ultimo_costo_entry.get_text(),
                                        prezzoDettaglio,
                                        self._percentualeIva))

    def confermaCalcolaDettaglioDaRicarico(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaDettaglioDaRicarico()

    def calcolaDettaglioDaMargine(self, widget=None, event=None):
        """        """
        self.prezzo_dettaglio_entry.set_text(self.nformat % calcolaListinoDaMargine(
                                        self.ultimo_costo_entry.get_text(),
                                        self.percentuale_margine_dettaglio_entry.get_text(),
                                        self._percentualeIva))
        self.prezzo_dettaglio_noiva_label.set_text(self.nformat % calcolaPrezzoIva(
                                        self.prezzo_dettaglio_entry.get_text(),
                                        ((-1)*self._percentualeIva)))
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(
                                        self.ultimo_costo_entry.get_text(),
                                        self.prezzo_dettaglio_entry.get_text(),
                                        self._percentualeIva))

    def confermaCalcolaDettaglioDaMargine(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaDettaglioDaMargine()

    def aggiornaDaDettaglio(self, widget=None, event=None):
        """        """
        self.prezzo_dettaglio_noiva_label.set_text(self.nformat % calcolaPrezzoIva(
                                        self.prezzo_dettaglio_entry.get_text(),
                                        ((-1)*self._percentualeIva)))
        przD = float(self.prezzo_dettaglio_noiva_label.get_text() or 0)
        przI = float(self.prezzo_ingrosso_entry.get_text() or 0)
        if przI == float(0):
            self.prezzo_ingrosso_entry.set_text(self.nformat % przD)
            self.prezzo_ingrosso_ivato_label.set_text(self.prezzo_dettaglio_entry.get_text())
        else:
            if przD != przI:
                msg = 'Attenzione! Aggiornare anche il listino ingrosso ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.prezzo_ingrosso_entry.set_text(self.nformat % przD)
                    self.prezzo_ingrosso_ivato_label.set_text(self.prezzo_dettaglio_entry.get_text())
        return False

    def calcolaIngrossoDaRicarico(self, widget=None, event=None):
        """        """
        self.prezzo_ingrosso_entry.set_text(self.nformat % calcolaListinoDaRicarico(
                                        self.ultimo_costo_entry.get_text(),
                                        self.percentuale_ricarico_ingrosso_entry.get_text()))
        self.prezzo_ingrosso_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                        self.prezzo_ingrosso_entry.get_text(),
                                        self._percentualeIva))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(
                                        self.ultimo_costo_entry.get_text(),
                                        self.prezzo_ingrosso_entry.get_text()))

    def confermaCalcolaIngrossoDaRicarico(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaIngrossoDaRicarico()

    def calcolaIngrossoDaMargine(self, widget=None, event=None):
        """        """
        self.prezzo_ingrosso_entry.set_text(self.nformat % calcolaListinoDaMargine(
                                        self.ultimo_costo_entry.get_text(),
                                        self.percentuale_margine_ingrosso_entry.get_text()))
        self.prezzo_ingrosso_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                        self.prezzo_ingrosso_entry.get_text(),
                                        self._percentualeIva))
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(
                                        self.ultimo_costo_entry.get_text(),
                                        self.prezzo_ingrosso_entry.get_text()))

    def confermaCalcolaIngrossoDaMargine(self, widget=None, event=None):
        """        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.calcolaIngrossoDaMargine()

    def aggiornaDaIngrosso(self, widget=None, event=None):
        """        """
        self.prezzo_ingrosso_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                        self.prezzo_ingrosso_entry.get_text(),
                                        self._percentualeIva))
        przI = float(self.prezzo_ingrosso_ivato_label.get_text() or 0)
        przD = float(self.prezzo_dettaglio_entry.get_text() or 0)
        if przD == float(0):
            self.prezzo_dettaglio_entry.set_text(self.nformat % przI)
            self.prezzo_dettaglio_noiva_label.set_text(self.prezzo_ingrosso_entry.get_text())
        else:
            if przI != przD:
                msg = 'Attenzione! Aggiornare anche il listino dettaglio ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.prezzo_dettaglio_entry.set_text(self.nformat % przI)
                    self.prezzo_dettaglio_noiva_label.set_text(self.prezzo_ingrosso_entry.get_text())
        return False

    def draw(self, cplx=False):
        """        """
        self.id_articolo_customcombobox.setSingleValue()
        self.id_articolo_customcombobox.setOnChangedCall(self.on_id_articolo_customcombobox_changed)

        fillComboboxListini(self.id_listino_customcombobox.combobox)
        self.id_listino_customcombobox.connect('clicked',
                                               on_id_listino_customcombobox_clicked,
                                               None, None)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            res = self.id_articolo_customcombobox.getData()
            self.id_articolo_customcombobox.set_sensitive(False)
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text(str(mN(self._percentualeIva,0)) + ' %')
        if self._anagrafica._listinoFissato:
            findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._anagrafica._idListino)
            self.id_listino_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.giveAnag(self)
        self.sconti_dettaglio_widget.setValues()
        self.sconti_ingrosso_widget.setValues()



    def on_id_articolo_customcombobox_changed(self):
        """        """
        re = self.id_articolo_customcombobox.getData()
        res = None
        if re:
            res = leggiArticolo(re.id)
        if res:
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text(str(mN(self._percentualeIva,0)) + ' %')

        fornitura = leggiFornitura(self.id_articolo_customcombobox.getId())
        self.ultimo_costo_entry.set_text(self.nformat % float(fornitura["prezzoNetto"]))

        self.aggiornaCostoIvato()
        self.calcolaDettaglioDaRicarico()
        self.calcolaIngrossoDaRicarico()


    def setDao(self, dao):
        """
        """
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = ListinoArticolo()
            if Environment.listinoFissato and self._anagrafica._idListino:
                Environment.listinoFissato = None
        self._refresh()
        return self.dao

    def _refresh(self):
        """        """
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.sconti_dettaglio_widget.setValues(sco=self.dao.sconto_vendita_dettaglio)
        self.sconti_ingrosso_widget.setValues(sco=self.dao.sconto_vendita_ingrosso)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        res = self.id_articolo_customcombobox.getData()
        if res:
            self.descrizione_breve_aliquota_iva_label.set_text(res["denominazioneBreveAliquotaIva"])
            self._percentualeIva = res["percentualeAliquotaIva"]
            self.percentuale_aliquota_iva_label.set_text(str(self.nformat % self._percentualeIva) + ' %')
        self.id_listino_customcombobox.combobox.set_active(-1)
        self.id_listino_customcombobox.set_sensitive(True)
        if self.dao.id_listino is None:
            if self._anagrafica._listinoFissato:
                self.dao.id_listino = self._anagrafica._idListino
                self.id_listino_customcombobox.set_sensitive(False)
        else:
            self.id_listino_customcombobox.set_sensitive(False)
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self.dao.id_listino)

        if self.dao.ultimo_costo is None:
            fornitura = leggiFornitura(self.id_articolo_customcombobox.getId())
            self.ultimo_costo_entry.set_text(self.nformat % float(fornitura["prezzoNetto"]))
        else:
            self.ultimo_costo_entry.set_text(self.nformat % float(self.dao.ultimo_costo or 0))
        self.data_listino_articolo_label.set_text(dateToString(self.dao.data_listino_articolo))
        self.prezzo_dettaglio_entry.set_text(self.nformat % float(self.dao.prezzo_dettaglio or 0))
        self.prezzo_ingrosso_entry.set_text(self.nformat % float(self.dao.prezzo_ingrosso or 0))
        self.percentuale_ricarico_dettaglio_entry.set_text('%-6.3f' % calcolaRicarico(
                                                    self.dao.ultimo_costo,
                                                    self.dao.prezzo_dettaglio,
                                                    self._percentualeIva))
        self.percentuale_margine_dettaglio_entry.set_text('%-6.3f' % calcolaMargine(
                                                    self.dao.ultimo_costo,
                                                    self.dao.prezzo_dettaglio,
                                                    self._percentualeIva))
        self.percentuale_ricarico_ingrosso_entry.set_text('%-6.3f' % calcolaRicarico(
                                                    self.dao.ultimo_costo,
                                                    self.dao.prezzo_ingrosso))
        self.percentuale_margine_ingrosso_entry.set_text('%-6.3f' % calcolaMargine(
                                                    self.dao.ultimo_costo,
                                                    self.dao.prezzo_ingrosso))

        self.ultimo_costo_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                                    self.dao.ultimo_costo,
                                                    self._percentualeIva))
        a = calcolaPrezzoIva(self.dao.prezzo_dettaglio,((-1)*self._percentualeIva))
        self.prezzo_dettaglio_noiva_label.set_text(self.nformat % calcolaPrezzoIva(
                                                    self.dao.prezzo_dettaglio,
                                                    ((-1)*self._percentualeIva)))

        self.prezzo_ingrosso_ivato_label.set_text(self.nformat % calcolaPrezzoIva(
                                                    self.dao.prezzo_ingrosso,
                                                    self._percentualeIva))

        self.sconti_dettaglio_widget.setValues(self.dao.sconto_vendita_dettaglio,
                                    self.dao.applicazione_sconti_dettaglio)
        self.sconti_ingrosso_widget.setValues(self.dao.sconto_vendita_ingrosso,
                                    self.dao.applicazione_sconti_ingrosso)

        if posso("PW"):
            self._refreshTagliaColore(self.dao.id_articolo)

    def _refreshTagliaColore(self, idArticolo):
        """        """
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

    def saveDao(self, tipo=None):
        """        """
        creaentryvarianti = False
        articolo = None
        if findIdFromCombobox(self.id_listino_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_listino_customcombobox.combobox)

        if self.id_articolo_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)

        listin = findIdFromCombobox(self.id_listino_customcombobox.combobox)

        self.dao.id_listino = listin
        self.dao.id_articolo = self.id_articolo_customcombobox.getId()

        if posso("PW"):
            articolo = Articolo().getRecord(id=self.dao.id_articolo)
            if articleType(articolo) == "father":
                msg = 'Attenzione! Si sta aggiungengo un Articolo Padre, creare le voci listino anche delle varianti?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    Environment.pg2log.info("CREO LE ENTRY DELLE VARIANTI DI LISTINO PERCHE' SI STA INSERENDO UN PADRE")
                    for art in articolo.articoliVarianti:
                        daoVariante = ListinoArticolo().select(idListino=listin,
                                                        idArticolo=art.id)
                        if daoVariante:
                            #daoVariante[0].delete()
                            daoVariante =daoVariante[0]
                        else:
                            daoVariante = ListinoArticolo()
                        if Environment.listinoFissato and self._anagrafica._idListino:
                            Environment.listinoFissato = None
                        daoVariante.id_articolo = art.id

                        daoVariante.id_listino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
                        daoVariante.listino_attuale = True
                        daoVariante.ultimo_costo = float(self.ultimo_costo_entry.get_text())
                        daoVariante.prezzo_dettaglio = float(self.prezzo_dettaglio_entry.get_text())
                        daoVariante.prezzo_ingrosso = float(self.prezzo_ingrosso_entry.get_text())
                        daoVariante.data_listino_articolo = datetime.datetime.today()


                        sconti_dettaglio = []
                        daoVariante.applicazione_sconti = "scalare"
                        for s in self.sconti_dettaglio_widget.getSconti():
                            daoSconto = ScontoVenditaDettaglio()
                            daoSconto.valore = s["valore"]
                            daoSconto.tipo_sconto = s["tipo"]
                            sconti_dettaglio.append(daoSconto)

                        sconti_ingrosso = []
                        daoVariante.applicazione_sconti = "scalare"
                        for s in self.sconti_ingrosso_widget.getSconti():
                            daoSconto = ScontoVenditaIngrosso()
                            daoSconto.valore = s["valore"]
                            daoSconto.tipo_sconto = s["tipo"]
                            sconti_ingrosso.append(daoSconto)
                        daoVariante.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})
                            #self.articolo_padre = articolo
                            #creaentryvarianti = True

        self.dao.listino_attuale = True
        self.dao.ultimo_costo = float(self.ultimo_costo_entry.get_text())
        self.dao.prezzo_dettaglio = float(self.prezzo_dettaglio_entry.get_text())
        self.dao.prezzo_ingrosso = float(self.prezzo_ingrosso_entry.get_text())
        self.dao.data_listino_articolo = datetime.datetime.today()

        sconti_dettaglio = []
        self.dao.applicazione_sconti = "scalare"
        for s in self.sconti_dettaglio_widget.getSconti():
            daoSconto = ScontoVenditaDettaglio()
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti_dettaglio.append(daoSconto)

        sconti_ingrosso = []
        self.dao.applicazione_sconti = "scalare"
        for s in self.sconti_ingrosso_widget.getSconti():
            daoSconto = ScontoVenditaIngrosso()
            daoSconto.valore = s["valore"]
            daoSconto.tipo_sconto = s["tipo"]
            sconti_ingrosso.append(daoSconto)
        #TODO :riportarlo alle property , risulta molto più pulito
        self.dao.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})

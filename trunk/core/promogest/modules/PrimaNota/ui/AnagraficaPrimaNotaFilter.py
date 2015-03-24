# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.dao.Setconf import SetConf
from promogest.dao.Banca import Banca
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaPrimaNotaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella prima nota cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          root='anagrafica_prima_nota_filter_table',
                          path='PrimaNota/gui/_anagrafica_primanota_elements.glade',
                          isModule=True)
        self._widgetFirstFocus = self.a_numero_filter_entry
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear)
        from promogest.dao.BancheAzienda import gen_banche_azienda
        fill_combobox_with_data(self.id_banche_filter_combobox, gen_banche_azienda, short=20)
        self.aggiornamento=False


    def draw(self):
        """ """
        if not setconf("PrimaNota", "valore_saldo_parziale_cassa_primanota") and \
            not setconf("PrimaNota", "data_saldo_parziale_cassa_primanota") and \
            not setconf("PrimaNota", "valore_saldo_parziale_banca_primanota") and \
            not setconf("PrimaNota", "data_saldo_parziale_banca_primanota"):
            self.inizializzaValoriPrimaNotaSaldo()

        stringa = "<b>Per i totali parziali e complessivi usare 'report a video'</b>"
        self._anagrafica.info_anag_complessa_label.set_markup(stringa)
        self.refresh()


    def _reOrderBy(self, column):
        if column.get_name() == "numero":
            return self._changeOrderBy(column,(None,TestataPrimaNota.numero))
        if column.get_name() == "data_inizio":
            return self._changeOrderBy(column,(None,TestataPrimaNota.data_inizio))


    def inizializzaValoriPrimaNotaSaldo(self):
        tpn = TestataPrimaNota().select(aDataInizio=stringToDate('01/01/' + Environment.workingYear), batchSize=None)
        tot = calcolaTotaliPrimeNote(tpn, tpn)

        bb = SetConf().select(key="valore_saldo_parziale_cassa_primanota", section="PrimaNota")
        if not bb:
            kbb = SetConf()
            kbb.key = "valore_saldo_parziale_cassa_primanota"
            kbb.value = 0.0 #str(tot["saldo_cassa"])
            kbb.section = "PrimaNota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore saldo parziale cassa prima nota"
            kbb.active = True
            kbb.tipo = "float"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="data_saldo_parziale_cassa_primanota", section="PrimaNota")
        if not bb:
            kbb = SetConf()
            kbb.key = "data_saldo_parziale_cassa_primanota"
            kbb.value = '01/01/' + Environment.workingYear
            kbb.section = "PrimaNota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore saldo parziale cassa prima nota"
            kbb.active = True
            kbb.tipo = "date"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="valore_saldo_parziale_banca_primanota", section="PrimaNota")
        if not bb:
            kbb = SetConf()
            kbb.key = "valore_saldo_parziale_banca_primanota"
            kbb.value = 0.0 #str(tot["saldo_banca"])
            kbb.section = "PrimaNota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore saldo parziale banca prima nota"
            kbb.active = True
            kbb.tipo = "float"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="data_saldo_parziale_banca_primanota", section="PrimaNota")
        if not bb:
            kbb = SetConf()
            kbb.key = "data_saldo_parziale_banca_primanota"
            kbb.value = '01/01/' + Environment.workingYear
            kbb.section = "PrimaNota"
            kbb.tipo_section = "Generico"
            kbb.description = "Data saldo parziale banca prima nota"
            kbb.active = True
            kbb.tipo = "date"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)
        Environment.session.commit()

    def on_banca_filter_check_clicked(self,check):
        if self.banca_filter_check.get_active():
            self.id_banche_filter_combobox.set_sensitive(True)
        else:
            self.id_banche_filter_combobox.set_active(0)
            self.id_banche_filter_combobox.set_sensitive(False)


    def clear(self):
        # Annullamento filtro
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear)
        self.a_numero_filter_entry.set_text('')
        self.da_numero_filter_entry.set_text('')
        self.denominazione_filter_entry.set_text('')
        self.a_data_inizio_datetimewidget.set_text('')
        self.id_banche_filter_combobox.set_active(0)

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        anumero = prepareFilterString(self.a_numero_filter_entry.get_text())
        danumero = prepareFilterString(self.da_numero_filter_entry.get_text())
        da_data_inizio = stringToDate(self.da_data_inizio_datetimewidget.get_text())
        if Environment.tipodb == "sqlite":
            a_data_inizio = stringToDateBumped(self.a_data_inizio_datetimewidget.get_text())
        else:
            a_data_inizio = stringToDate(self.a_data_inizio_datetimewidget.get_text())
        Environment.da_data_inizio_primanota = self.da_data_inizio_datetimewidget.get_text()
        Environment.a_data_inizio_primanota = self.a_data_inizio_datetimewidget.get_text()
        deno = prepareFilterString(self.denominazione_filter_entry.get_text())
        tipo_banca = self.banca_filter_check.get_active()
        tipo = None
        if not tipo_banca:
            tipoBanca = "banca"
        else:
            tipoBanca = None
        tipo_cassa = self.cassa_filter_check.get_active()
        if not tipo_cassa:
            tipoCassa = "cassa"
        else:
            tipoCassa = None

        segno_entrate = self.entrate_filter_check.get_active()
        if not segno_entrate:
            segnoEntrate = "entrata"
        else:
            segnoEntrate = None
        segno_uscite = self.uscite_filter_check.get_active()
        if not segno_uscite:
            segnoUscite = "uscita"
        else:
            segnoUscite = None

        banca = findIdFromCombobox(self.id_banche_filter_combobox)

        def filterCountClosure():
            banca = findIdFromCombobox(self.id_banche_filter_combobox)
            return TestataPrimaNota().count(aNumero=anumero,
                                daNumero=danumero,
                                daDataInizio=da_data_inizio,
                                aDataInizio=a_data_inizio,
                                tipoCassa = tipoCassa,
                                tipoBanca = tipoBanca,
                                segnoEntrate = segnoEntrate,
                                segnoUscite = segnoUscite,
                                denominazione = deno,
                                idBanca = banca)
        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            banca = findIdFromCombobox(self.id_banche_filter_combobox)
            return TestataPrimaNota().select(aNumero=anumero,
                                            daNumero=danumero,
                                            daDataInizio=da_data_inizio,
                                            aDataInizio=a_data_inizio,
                                            tipoCassa = tipoCassa,
                                            tipoBanca = tipoBanca,
                                            segnoEntrate = segnoEntrate,
                                            segnoUscite = segnoUscite,
                                            denominazione = deno,
                                            idBanca = banca,
                                            orderBy=self.orderBy,
                                            offset=offset,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self.primanota_filter_listore.clear()
        valore = 0
        for i in valis:
            col_valore = None
            col_tipo = None

            if mN(i.totali["totale"]) >0:
                col_valore = "#CCFFAA"
            else:
                col_valore = "#FFD7D7"

            if len(i.righeprimanota) >1:
                denom = i.note
                note = "( Più operazioni )"
                a = [l for l in i.righeprimanota]
                if len(a)==1:
                    tipo = i.righeprimanota[0].tipo
                else:
                    tipo = "misto"
                banca = i.righeprimanota[0].banca[0:15] or ""
            elif len(i.righeprimanota) ==1:
                denom = i.righeprimanota[0].denominazione
                note = i.note
                tipo = i.righeprimanota[0].tipo
                banca = i.righeprimanota[0].banca[0:15] or ""
            else:
                print "ATTENZIONE TESTATA PRIMA NOTA SENZA RIGHE", i, i.note, i.data_inizio
                denom ="SENZARIGHE"
                note = i.note
                banca = ""
            if tipo == "cassa":
                col_tipo = "#FFF2C7"
            elif tipo=="banca":
                col_tipo = "#CFF5FF"
            else:
                col_tipo = "#FFFFFF"
            self.primanota_filter_listore.append((i,
                                        col_valore,
                                        str(i.numero) or '',
                                        dateToString(i.data_inizio) or '',
                                        denom or '',
                                        str(mNLC(i.totali["totale"],2).encode("utf-8")) or "0",
                                        tipo,
                                        banca,
                                        note or "",
                                        col_tipo
                                        ))

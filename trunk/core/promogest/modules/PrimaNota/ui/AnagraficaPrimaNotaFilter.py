# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaPrimaNotaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella prim nota cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_prima_nota_filter_table',
                          gladeFile='PrimaNota/gui/_anagrafica_primanota_elements.glade',
                          module=True)
        self._widgetFirstFocus = self.a_numero_filter_entry
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear)
        fillComboboxBanche(self.id_banche_filter_combobox, short=20)
        self.aggiornamento=False


    def draw(self):
        """ """
        #pns = TestataPrimaNota().select(batchSize=None)
        #for i in pns:
            #self.checkOldPN(i)
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
        messageInfo(msg="Nessun riporto settato, imposto uno standard al primo gennaio")
        tpn = TestataPrimaNota().select(aDataInizio=stringToDate('01/01/' + Environment.workingYear), batchSize=None)
        tot = calcolaTotaliPrimeNote(tpn, tpn)

        bb = SetConf().select(key="valore_saldo_parziale_cassa_primanota", section="Primanota")
        if not bb:
            kbb = SetConf()
            kbb.key = "valore_saldo_parziale_cassa_primanota"
            kbb.value = 0 #str(tot["saldo_cassa"])
            kbb.section = "Primanota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore Saldo parziale prima nota"
            kbb.active = True
            kbb.tipo = "float"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="data_saldo_parziale_cassa_primanota", section="Primanota")
        if not bb:
            kbb = SetConf()
            kbb.key = "data_saldo_parziale_cassa_primanota"
            kbb.value = '01/01/' + Environment.workingYear
            kbb.section = "Primanota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore Saldo parziale prima nota"
            kbb.active = True
            kbb.tipo = "date"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="valore_saldo_parziale_banca_primanota", section="Primanota")
        if not bb:
            kbb = SetConf()
            kbb.key = "valore_saldo_parziale_banca_primanota"
            kbb.value = 0 #str(tot["saldo_banca"])
            kbb.section = "Primanota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore Saldo parziale prima nota"
            kbb.active = True
            kbb.tipo = "float"
            kbb.date = datetime.datetime.now()
            Environment.session.add(kbb)

        bb = SetConf().select(key="data_saldo_parziale_banca_primanota", section="Primanota")
        if not bb:
            kbb = SetConf()
            kbb.key = "data_saldo_parziale_banca_primanota"
            kbb.value = '01/01/' + Environment.workingYear
            kbb.section = "Primanota"
            kbb.tipo_section = "Generico"
            kbb.description = "Valore Saldo parziale prima nota"
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
            if tipo =="cassa":
                col_tipo = "#FFF2C7"
            elif tipo=="banca":
                col_tipo = "#CFF5FF"
            else:
                col_tipo = ""
            self.primanota_filter_listore.append((i,
                                        col_valore,
                                        (str(i.numero) or ''),
                                        (dateToString(i.data_inizio) or ''),
                                        denom or '',
                                        (str(mNLC(i.totali["totale"],2)) or "0"),
                                        tipo,
                                        banca,
                                        note or "",
                                        col_tipo
                                        ))

    def checkOldPN(self, dao):
        numero = None
        numeroSEL = None
        date = []
        if len(dao.righeprimanota)>1 :
            for f in dao.righeprimanota:
                if f.data_registrazione not in date:
                    date.append(f.data_registrazione)
            if len(date)>1:
                if not self.aggiornamento:
                    messageInfo(msg="""ATTENZIONE! Alcune parti del modulo PrimaNota sono
state modificate ed è necessario un aggiornamento di quelle precedentemente
inserite. Saranno salvaguardati i riferimenti interni e quelli con i pagamenti documenti.
La differenza sarà che principalmente verrà creata una primanota per ogni operazione
di cassa o di banca effettuata. Non ci sarà la "chiusura" della prima nota.
Si potranno ancora fare PrimeNote con più operazioni. Rimandiamo comunque alla
lettura delle novità sul sito del programma o nella sezione news interna.
Si avvisa che la migrazione potrebbe richiedere anche qualche minuto""")
                    self.aggiornamento = True
                for r in dao.righeprimanota:
                    print "DATA REGISTRAZIONE", r.numero, r.data_registrazione.day, r.data_registrazione.month, r.data_registrazione.year
                    a = TestataPrimaNota()
                    a.data_inizio = r.data_registrazione
                    date = Environment.workingYear
                    numeroSEL= TestataPrimaNota().select(complexFilter=(and_(TestataPrimaNota.data_inizio.between(datetime.date(int(r.data_registrazione.year), 1, 1), datetime.date(int(r.data_registrazione.year) + 1, 1, 1)))), batchSize=None)
                    if numeroSEL:
                        numero = max([p.numero for p in numeroSEL]) +1
                    else:
                        numero = 1
                    a.numero = numero
                    a.persist()
                    r.id_testata_prima_nota = a.id
                    r.persist()
                dao.delete()
        elif len(dao.righeprimanota) ==0:
            dao.delete()

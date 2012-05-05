# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
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

from promogest.lib.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget


class AnagraficaPrimaNotaSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, 'PrimaNota/gui/_anagrafica_primanota_setup_frame',
                                    'PrimaNota/gui/_anagrafica_primanota_setup.glade',
                                    isModule=True)
        self.maino = maino
        self._draw()

    def _draw(self):
        """ Riempiamo le combo """
        return

    def _refresh(self):
        """
        Carichiamo i dati in interfaccia
        """
        self.data_cassa_DateWidget.set_text(str(setconf("PrimaNota", "data_saldo_parziale_cassa_primanota") or '01/01/' + Environment.workingYear))
        self.valore_cassa_SignedMoneyEntryField.set_text(str(setconf("PrimaNota", "valore_saldo_parziale_cassa_primanota") or 0.0))
        self.data_banca_DateWidget.set_text(str(setconf("PrimaNota", "data_saldo_parziale_banca_primanota") or '01/01/' + Environment.workingYear))
        self.valore_banca_SignedMoneyEntryField.set_text(str(setconf("PrimaNota", "valore_saldo_parziale_banca_primanota") or 0.0))

        try:
            self.aggiungi_partita_iva_check.set_active(int(setconf("PrimaNota", "aggiungi_partita_iva")))
        except:
            self.aggiungi_partita_iva_check.set_active(0)

        try:
            self.inserisci_totali_generali_in_report_check.set_active(int(setconf("PrimaNota", "saldi_periodo")))
        except:
            self.inserisci_totali_generali_in_report_check.set_active(0)

        try:
            self.inserisci_senza_data_pagamento_check.set_active(int(setconf("PrimaNota", "inserisci_senza_data_pagamento")))
        except:
            self.inserisci_senza_data_pagamento_check.set_active(0)

        self.vecchia_data_cassa = str(self.data_cassa_DateWidget.get_text()).strip()
        self.vecchio_valore_cassa = str(self.valore_cassa_SignedMoneyEntryField.get_text()).strip()
        self.vecchia_data_banca = str(self.data_banca_DateWidget.get_text()).strip()
        self.vecchio_valore_banca = str(self.valore_banca_SignedMoneyEntryField.get_text()).strip()

    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        changed = (self.vecchia_data_cassa != self.data_cassa_DateWidget.get_text()) or \
                  (self.vecchio_valore_cassa != self.valore_cassa_SignedMoneyEntryField.get_text()) or \
                  (self.vecchia_data_banca != self.data_banca_DateWidget.get_text()) or \
                  (self.vecchio_valore_banca != self.valore_banca_SignedMoneyEntryField.get_text())
        if changed and YesNoDialog(msg="Sei sicuro di voler modificare le date e i valori di Prima Nota?"):
            # CASSA
            c = SetConf().select(key="data_saldo_parziale_cassa_primanota", section="PrimaNota")
            if c:
                c = c[0]
            else:
                c = SetConf()
            c.key = "data_saldo_parziale_cassa_primanota"
            c.section = "PrimaNota"
            c.value = str(self.data_cassa_DateWidget.get_text())
            c.tipo = "date"
            c.description = "Data saldo parziale di cassa per prima nota"
            c.tipo_section = "Generico"
            c.active = True
            c.visible = True
            c.date = datetime.datetime.now()
            Environment.session.add(c)

            c = SetConf().select(key="valore_saldo_parziale_cassa_primanota", section="PrimaNota")
            if c:
                c = c[0]
            else:
                c = SetConf()
            c.key = "valore_saldo_parziale_cassa_primanota"
            c.section = "PrimaNota"
            c.value = str(self.valore_cassa_SignedMoneyEntryField.get_text())
            c.tipo = "float"
            c.description = "Valore saldo parziale di cassa per prima nota"
            c.tipo_section = "Generico"
            c.active = True
            c.visible = True
            c.date = datetime.datetime.now()
            Environment.session.add(c)

            # BANCA
            c = SetConf().select(key="data_saldo_parziale_banca_primanota", section="PrimaNota")
            if c:
                c = c[0]
            else:
                c = SetConf()
            c.key = "data_saldo_parziale_banca_primanota"
            c.section = "PrimaNota"
            c.value = str(self.data_banca_DateWidget.get_text())
            c.tipo = "date"
            c.description = "Data saldo parziale di banca per prima nota"
            c.tipo_section = "Generico"
            c.active = True
            c.visible = True
            c.date = datetime.datetime.now()
            Environment.session.add(c)

            c = SetConf().select(key="valore_saldo_parziale_banca_primanota", section="PrimaNota")
            if c:
                c = c[0]
            else:
                c = SetConf()
            c.key = "valore_saldo_parziale_banca_primanota"
            c.section = "PrimaNota"
            c.value = str(self.valore_banca_SignedMoneyEntryField.get_text())
            c.tipo = "float"
            c.description = "Valore saldo parziale di banca per prima nota"
            c.tipo_section = "Generico"
            c.active = True
            c.visible = True
            c.date = datetime.datetime.now()
            Environment.session.add(c)

            # Salvo i vecchi valori
            self.vecchia_data_cassa = str(self.data_cassa_DateWidget.get_text()).strip()
            self.vecchio_valore_cassa = str(self.valore_cassa_SignedMoneyEntryField.get_text()).strip()
            self.vecchia_data_banca = str(self.data_banca_DateWidget.get_text()).strip()
            self.vecchio_valore_banca = str(self.valore_banca_SignedMoneyEntryField.get_text()).strip()

        c = SetConf().select(key="aggiungi_partita_iva", section="PrimaNota")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "aggiungi_partita_iva"
        c.section = "PrimaNota"
        c.value = str(self.aggiungi_partita_iva_check.get_active())
        c.tipo = "bool"
        c.description = "Aggiungere la partita IVA di un cliente/fornitore e/o il codice fiscale di un cliente in descrizione operazione"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)

        c = SetConf().select(key="inserisci_senza_data_pagamento", section="PrimaNota")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "inserisci_senza_data_pagamento"
        c.section = "PrimaNota"
        c.value = str(self.inserisci_senza_data_pagamento_check.get_active())
        c.tipo = "bool"
        c.description = "Inserire la prima nota senza data di scadenza"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)

        c = SetConf().select(key="saldi_periodo", section="PrimaNota")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "saldi_periodo"
        c.section = "PrimaNota"
        c.value = str(self.inserisci_totali_generali_in_report_check.get_active())
        c.tipo = "bool"
        c.description = "Inserire i saldi per periodo nel report"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)

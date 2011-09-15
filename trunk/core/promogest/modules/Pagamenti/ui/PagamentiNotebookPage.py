# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest.ui.gtk_compat import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget

from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
from promogest.modules.Pagamenti.ui.AnagraficadocumentiPagamentExt import INFO_SCADENZA_PAGE, PRIMA_SCADENZA_PAGE, \
SECONDA_SCADENZA_PAGE, TERZA_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE, ACCONTO_PAGE

class PagamentiNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, 'pagamenti_vbox',
                                    'Pagamenti/gui/pagamenti_notebook.glade',
                                    isModule=True)
        self.rowBackGround = None
        self.ana = mainnn
        #self.dao_articolo_adr = None
        self.draw()

    def draw(self):
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
                            on_id_pagamento_customcombobox_clicked)
        self.id_pagamento_customcombobox.combobox.connect('changed',
            self.id_pagamento_customcombobox_changed)

        self.aggiorna_pagamenti_button.connect('clicked',
            self.on_aggiorna_pagamenti_button_clicked)
        self.calcola_importi_scadenza_button.connect('clicked',
            self.on_calcola_importi_scadenza_button_clicked)
        self.chiudi_pagamento_documento_button.connect('clicked',
            self.on_chiudi_pagamento_documento_button_clicked)
        self.apri_pagamento_documento_button.connect('clicked',
            self.on_apri_pagamento_documento_button_clicked)
        self.aggiungi_scheda_acconto_button.connect('clicked',
            self.on_aggiungi_scheda_acconto_button_clicked)

        self.pulisci_acconto_button.connect('clicked',
            self.on_pulisci_acconto_button_clicked)
        self.pulisci_prima_rata_button.connect('clicked',
            self.on_pulisci_prima_rata_button_clicked)
        self.pulisci_seconda_rata_button.connect('clicked',
            self.on_pulisci_seconda_rata_button_clicked)
        self.pulisci_terza_rata_button.connect('clicked',
            self.on_pulisci_terza_rata_button_clicked)
        self.pulisci_quarta_rata_button.connect('clicked',
            self.on_pulisci_quarta_rata_button_clicked)

        # Popola la pagina dei pagamenti

        self.data_pagamento_prima_scadenza_entry.entry.connect('changed',
                self.on_data_pagamento_prima_scadenza_entry_changed)
        self.data_pagamento_seconda_scadenza_entry.entry.connect('changed',
                self.on_data_pagamento_seconda_scadenza_entry_changed)
        self.data_pagamento_terza_scadenza_entry.entry.connect('changed',
                self.on_data_pagamento_terza_scadenza_entry_changed)
        self.data_pagamento_quarta_scadenza_entry.entry.connect('changed',
                self.on_data_pagamento_quarta_scadenza_entry_changed)

        self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
            0)+'</span></b>')
        self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
            0)+'</span></b>')
        self.importo_primo_documento_entry.set_text('')
        self.importo_secondo_documento_entry.set_text('')
        self.numero_primo_documento_entry.set_text('')
        self.numero_secondo_documento_entry.set_text('')

        fillComboboxPagamenti(self.id_pagamento_acconto_customcombobox.combobox)
        fillComboboxPagamenti(self.id_pagamento_prima_scadenza_customcombobox.combobox)
        fillComboboxPagamenti(self.id_pagamento_seconda_scadenza_customcombobox.combobox)
        fillComboboxPagamenti(self.id_pagamento_terza_scadenza_customcombobox.combobox)
        fillComboboxPagamenti(self.id_pagamento_quarta_scadenza_customcombobox.combobox)

        fillComboboxBanche(self.id_banca_acconto_ccb.combobox, short=20)
        fillComboboxBanche(self.id_banca_prima_scadenza_ccb.combobox, short=20)
        fillComboboxBanche(self.id_banca_seconda_scadenza_ccb.combobox, short=20)
        fillComboboxBanche(self.id_banca_terza_scadenza_ccb.combobox, short=20)
        fillComboboxBanche(self.id_banca_quarta_scadenza_ccb.combobox, short=20)
        self._clear()

    def id_pagamento_customcombobox_changed(self, combobox):
        if self.ana._loading:
            return
        self.on_calcola_importi_scadenza_button_clicked(None)

    def _clear(self):
        self.id_pagamento_customcombobox.combobox.set_active(-1)

    def on_data_pagamento_prima_scadenza_entry_changed(self, entry):
        """ Reimposta i totali saldato e da saldare alla modifica della data
            di pagamento della prima scadenza """
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_data_pagamento_seconda_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_data_pagamento_terza_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_data_pagamento_quarta_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_aggiorna_pagamenti_button_clicked(self, button):
        """Aggiorna la parte dei pagamenti"""
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_seleziona_prima_nota_button_clicked(self, button):
        """ Seleziona la prima nota da utilizzare come riferimento """
        if self.ana.numero_primo_documento_entry.get_text() != "":
                response = AnagraficadocumentiPagamentExt.impostaDocumentoCollegato(int(self.ana.numero_primo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False

        if response:
            self.ana.importo_primo_documento_entry.set_text(str(response))
            AnagraficadocumentiPagamentExt.dividi_importo(self.ana)
            AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)
            self.ana.numero_secondo_documento_entry.set_sensitive(True)
            self.ana.seleziona_seconda_nota_button.set_sensitive(True)
            self.ana.importo_secondo_documento_entry.set_sensitive(True)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        if self.ana.numero_secondo_documento_entry.get_text() != "":
            response = AnagraficadocumentiPagamentExt.impostaDocumentoCollegato(int(self.ana.numero_secondo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False
        if response:
            self.ana.importo_primo_documento_entry.set_text(str(response))
            AnagraficadocumentiPagamentExt.dividi_importo(self.ana)
            AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_calcola_importi_scadenza_button_clicked(self, button):
        """calcola importi scadenza pagamenti """
        id_pag = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        if id_pag == -1 or id_pag==0 or id_pag==None:
            messageInfo(msg=_("NESSUN METODO DI PAGAMENTO SELEZIONATO\n NON POSSO AGIRE"))
            notebook_tab_show(self.scadenze_notebook, INFO_SCADENZA_PAGE)
            notebook_tabs_hide(self.scadenze_notebook, (ACCONTO_PAGE, PRIMA_SCADENZA_PAGE,SECONDA_SCADENZA_PAGE, TERZA_SCADENZA_PAGE, QUARTA_SCADENZA_PAGE,))
            return
        if self.ana.dao.documento_saldato:
            msg = _('Attenzione! Stai per riaprire un documento già saldato.\n Continuare ?')
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.stato_label.set_markup(_('<b><span foreground="#B40000" size="24000">APERTO</span></b>'))
            else:
                return
        AnagraficadocumentiPagamentExt.attiva_scadenze(self.ana)
        AnagraficadocumentiPagamentExt.dividi_importo(self.ana)
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self.ana)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        """ Seleziona la seconda nota di credito da utilizzare come riferimento """
        AnagraficadocumentiPagamentExt.on_seleziona_seconda_nota_button_clicked(self, button)

    def on_primanota_button_clicked(self, button):
        AnagraficadocumentiPagamentExt.on_primanota_button_clicked(self, button)

    def on_chiudi_pagamento_documento_button_clicked(self, button):
        """ Chiude un pagamento
        """
        if (self.importo_prima_scadenza_entry.get_text() =="" or \
        self.importo_prima_scadenza_entry.get_text() ==str(0)) and\
        (self.importo_seconda_scadenza_entry.get_text() =="" or \
        self.importo_seconda_scadenza_entry.get_text() ==str(0)) and\
        (self.importo_terza_scadenza_entry.get_text() =="" or \
        self.importo_terza_scadenza_entry.get_text() ==str(0)) and\
        (self.importo_quarta_scadenza_entry.get_text() =="" or \
        self.importo_quarta_scadenza_entry.get_text() ==str(0)) and\
        (self.importo_acconto_scadenza_entry.get_text() =="" or \
        self.importo_acconto_scadenza_entry.get_text() ==str(0)):
            msg = 'Attenzione! Stai per chiudere un documento dove non figura incassato niente.\n Continuare?'
            procedi = YesNoDialog(msg=msg, transient=None)
            if procedi:
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')
                self.chiudi_pagamento_documento_button.set_sensitive(False)
                self.apri_pagamento_documento_button.set_sensitive(True)
        else:
            self.stato_label.set_markup('<b><span foreground="#338000" size="24000">PAGATO</span></b>')

    def on_apri_pagamento_documento_button_clicked(self, button):
        """ Apre il pagamento
        """
        msg=_('Attenzione! Stai per riaprire un documento considerato già pagato.\n Continuare?')
        procedi = YesNoDialog(msg=msg)
        if procedi:
            self.stato_label.set_markup(_('<b><span foreground="#B40000" size="24000">APERTO</span></b>'))
            self.apri_pagamento_documento_button.set_sensitive(False)
            self.chiudi_pagamento_documento_button.set_sensitive(True)

    def on_pulisci_acconto_button_clicked(self, button):
        """ Pulizia dei campi relativi all'acconto
        """
        self.data_acconto_entry.set_text("")
        self.importo_acconto_scadenza_entry.set_text("")
        self.id_pagamento_acconto_customcombobox.combobox.set_active(-1)
        self.id_banca_acconto_ccb.combobox.set_active(-1)
        self.data_pagamento_acconto_entry.set_text("")
        textview_set_text(self.note_acconto_textview, "")

    def on_pulisci_prima_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla prima rata
        """
        self.data_prima_scadenza_entry.set_text("")
        self.id_pagamento_prima_scadenza_customcombobox.combobox.set_active(-1)
        self.id_banca_prima_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_prima_scadenza_entry.set_text("")
        self.importo_prima_scadenza_entry.set_text("")
        textview_set_text(self.note_prima_scadenza_textview, "")

    def on_pulisci_seconda_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla seconda rata
        """
        self.data_seconda_scadenza_entry.set_text("")
        self.importo_seconda_scadenza_entry.set_text("")
        self.id_pagamento_seconda_scadenza_customcombobox.combobox.set_active(-1)
        self.id_banca_seconda_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_seconda_scadenza_entry.set_text("")
        textview_set_text(self.note_seconda_scadenza_textview, "")

    def on_pulisci_terza_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla terza rata
        """
        self.data_terza_scadenza_entry.set_text("")
        self.importo_terza_scadenza_entry.set_text("")
        self.id_pagamento_terza_scadenza_customcombobox.combobox.set_active(-1)
        self.id_banca_terza_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_terza_scadenza_entry.set_text("")
        textview_set_text(self.note_terza_scadenza_textview, "")

    def on_pulisci_quarta_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla quarta rata
        """
        self.data_quarta_scadenza_entry.set_text("")
        self.importo_quarta_scadenza_entry.set_text("")
        self.id_pagamento_quarta_scadenza_customcombobox.combobox.set_active(-1)
        self.id_banca_quarta_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_quarta_scadenza_entry.set_text("")
        textview_set_text(self.note_quarta_scadenza_textview, "")

    def on_aggiungi_scheda_acconto_button_clicked(self, button):
        if not self.ana.acconto:
            notebook_tabs_show(self.scadenze_notebook, (ACCONTO_PAGE,))
            self.aggiungi_scheda_acconto_button.set_label("Rimuovi acconto")
            self.ana.acconto = True
        else:
            notebook_tabs_hide(self.scadenze_notebook, (ACCONTO_PAGE,))
            self.aggiungi_scheda_acconto_button.set_label("Aggiungi acconto")
            self.ana.acconto = False

    def on_pulisci_scadenza_button_clicked(self, button):
        """ Pulizia di tutti i campi relativi alla tab pagamenti
        """
        msg = _('Attenzione! Stai per rimuovere i riferimenti già inseriti. Continuare?')
        procedi = YesNoDialog(msg=msg)
        if procedi:
            self.numero_primo_documento_entry.set_text('')
            self.numero_secondo_documento_entry.set_text('')
            self.importo_primo_documento_entry.set_text('')
            self.importo_secondo_documento_entry.set_text('')

    def on_controlla_rate_scadenza_button_clicked(self, button):
        """ bottone che controlla le rate scadenza """
        AnagraficadocumentiPagamentExt.controlla_rate_scadenza(self, True)
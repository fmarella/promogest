# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/

# Author: Francesco Meloni  <francesco@promotux.it>

#import datetime
#from AnagraficaComplessa import AnagraficaEdit
#from AnagraficaDocumentiEdit import AnagraficaDocumentiEdit
#import gtk
#from promogest.dao.TestataDocumento import TestataDocumento
#from promogest.dao.TestataMovimento import TestataMovimento
#from promogest.dao.RigaDocumento import RigaDocumento
#from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
#from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
#from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
#from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
#from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
#from promogest.dao.Articolo import Articolo
#from promogest.dao.Magazzino import Magazzino
#from promogest.dao.Operazione import Operazione
#from utils import *
#from utilsCombobox import *
#from promogest.dao.DaoUtils import giacenzaArticolo
#from GladeWidget import GladeWidget
#from promogest import Environment
#from promogest.modules.Pagamenti.Pagamenti import Pagamenti


class AnagraficadocumentiPagamentExt():
    def __init__(self,ui, dao=None):
        self.ui = ui
        self.dao = dao

    def on_pulisci_scadenza_button_clicked(self,ui,button):
        """
        Pulisce tutti i campi relativi alla tab pagamenti
        """
        self.ui.Pagamenti.attiva_prima_scadenza(False,False)
        self.ui.Pagamenti.attiva_seconda_scadenza(False,False)
        self.ui.Pagamenti.attiva_terza_scadenza(False,False)
        self.ui.Pagamenti.attiva_quarta_scadenza(False,False)
        self.ui.numero_primo_documento_entry.set_text('')
        self.ui.numero_secondo_documento_entry.set_text('')
        self.ui.importo_primo_documento_entry.set_text('')
        self.ui.importo_secondo_documento_entry.set_text('')

    def on_seleziona_prima_nota_button_clicked(self,ui, button):
        if self.ui.numero_primo_documento_entry.get_text() != "":
                response = self.ui.Pagamenti.impostaDocumentoCollegato(
                        int(self.ui.numero_primo_documento_entry.get_text()))
                print "on_seleziona_prima_nota: response = ", response
        else:
            self.ui.showMessage("Inserisci il numero del documento")
            response = False

        if response != False:
            self.ui.importo_primo_documento_entry.set_text(str(response))
            self.ui.Pagamenti.dividi_importo()
            self.ui.Pagamenti.ricalcola_sospeso_e_pagato()
            self.ui.numero_secondo_documento_entry.set_sensitive(True)
            self.ui.seleziona_seconda_nota_button.set_sensitive(True)
            self.ui.importo_secondo_documento_entry.set_sensitive(True)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        if self.ui.numero_secondo_documento_entry.get_text() != "":
            response = self.ui.Pagamenti.impostaDocumentoCollegato(
                    int(self.ui.numero_secondo_documento_entry.get_text()))
        else:
            self.ui.showMessage("Inserisci il numero del documento")
            response = False
        if response != False:
            self.ui.Pagamenti.importo_primo_documento_entry.set_text(str(response))
            self.ui.Pagamenti.dividi_importo()
            self.ui.Pagamenti.ricalcola_sospeso_e_pagato()
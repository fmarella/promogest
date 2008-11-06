# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
 """

import gtk
import gobject
from GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Azienda
from promogest.dao.Azienda import Azienda

from utils import dateToString, stringToDate, checkCodFisc, checkPartIva, showAnagraficaRichiamata
#from utilsCombobox import *



class AnagraficaAziende(GladeWidget):
    """ Anagrafica aziende """

    def __init__(self, mainWindow):
        self._mainWindow = mainWindow
        self.dao = Azienda().getRecord()
        GladeWidget.__init__(self, 'anagrafica_aziende_scrolledwindow',fileName='_anagrafica_aziende_elements.glade')
        self.draw()


    def draw(self):
        # Popolamento campi in maschera dal dao
        self.setDao()
        self.denominazione_entry.grab_focus()


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'anagrafica """
        self._anagrafica_aziende_elements.show_all()


    def setDao(self):
        # Creazione dao azienda corrente
        self.dao = Azienda(id=Environment.params["schema"]).getRecord()
        self._refresh()


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.ragione_sociale_entry.set_text(self.dao.ragione_sociale or '')
        self.localita_sede_operativa_entry.set_text(self.dao.sede_operativa_localita or '')
        self.indirizzo_sede_operativa_entry.set_text(self.dao.sede_operativa_indirizzo or '')
        self.numero_sede_operativa_entry.set_text(self.dao.sede_operativa_numero or '')
        self.cap_sede_operativa_entry.set_text(self.dao.sede_operativa_cap or '00000')
        self.provincia_sede_operativa_entry.set_text(self.dao.sede_operativa_provincia or '')
        self.localita_sede_legale_entry.set_text(self.dao.sede_legale_localita or '')
        self.indirizzo_sede_legale_entry.set_text(self.dao.sede_legale_indirizzo or '')
        self.numero_sede_legale_entry.set_text(self.dao.sede_legale_numero or '')
        self.cap_sede_legale_entry.set_text(self.dao.sede_legale_cap or '00000')
        self.provincia_sede_legale_entry.set_text(self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(self.dao.partita_iva or '00000000000')
        self.data_iscrizione_cciaa_entry.set_text(dateToString(self.dao.iscrizione_cciaa_data or ''))
        self.numero_iscrizione_cciaa_entry.set_text(self.dao.iscrizione_cciaa_numero or '')
        self.data_iscrizione_tribunale_entry.set_text(dateToString(self.dao.iscrizione_tribunale_data or ''))
        self.numero_iscrizione_tribunale_entry.set_text(self.dao.iscrizione_tribunale_numero or '')
        self.codice_rea_entry.set_text(self.dao.codice_rea or '')
        self.matricola_inps_entry.set_text(self.dao.matricola_inps or '')
        self.numero_conto_entry.set_text(self.dao.numero_conto or '')
        self.cin_entry.set_text(self.dao.cin or '')
        self.iban_entry.set_text(self.dao.iban or '')
        self.logo_filechooserbutton.set_filename(self.dao.percorso_immagine or '')
        self.logo_azienda.set_from_file(self.dao.percorso_immagine)

        #self.percorso_immagine_entry.set_text(self.dao.percorso_immagine or '')


    def saveDao(self):
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        self.dao.sede_operativa_localita = self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_indirizzo = self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_numero = self.numero_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_localita = self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_indirizzo = self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_numero = self.numero_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        self.dao.iscrizione_cciaa_data = stringToDate(self.data_iscrizione_cciaa_entry.get_text())
        self.dao.iscrizione_cciaa_numero = self.numero_iscrizione_cciaa_entry.get_text()
        self.dao.iscrizione_tribunale_data = stringToDate(self.data_iscrizione_tribunale_entry.get_text())
        self.dao.iscrizione_tribunale_numero = self.numero_iscrizione_tribunale_entry.get_text()
        self.dao.codice_rea = self.codice_rea_entry.get_text()
        self.dao.matricola_inps = self.matricola_inps_entry.get_text()
        self.dao.numero_conto = self.numero_conto_entry.get_text()
        self.dao.cin = self.cin_entry.get_text()
        self.dao.iban = self.iban_entry.get_text()
        self.dao.percorso_immagine = self.logo_filechooserbutton.get_filename()
        self.logo_azienda.set_from_file(self.dao.percorso_immagine)
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                return
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                return
        self.dao.persist()


    def on_apply_button_clicked(self, button):
        self.saveDao()


    def on_cancel_button_clicked(self, button):
        self.setDao()


    def on_contatti_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        from AnagraficaContatti import AnagraficaContatti
        anag = AnagraficaContatti(self.dao.schemaa, 'azienda')
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow.getTopLevel(), anagWindow, toggleButton)

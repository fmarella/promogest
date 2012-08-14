# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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
from promogest.ui.AnagraficaPGEdit import AnagraficaPGEdit
import promogest.dao.Fornitore
from promogest.dao.Fornitore import Fornitore
from promogest.dao.daoContatti.ContattoFornitore import ContattoFornitore
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaFornitoriEdit(AnagraficaEdit, AnagraficaPGEdit):
    """ Modifica un record dell'anagrafica dei fornitori """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                            anagrafica,
                            'anagrafica_fornitori_detail_notebook',
                            'Dati fornitore',
                            gladeFile='_anagrafica_fornitori_elements.glade')
        AnagraficaPGEdit.__init__(self, "fornitore")
        self._widgetFirstFocus = self.codice_entry

    def draw(self,cplx=False):
        fillComboBoxNazione(self.nazione_combobox, default="Italia")
        fillComboboxCategorieFornitori(self.id_categoria_fornitore_customcombobox.combobox)
        self.id_categoria_fornitore_customcombobox.connect('clicked',
                                                           on_id_categoria_fornitore_customcombobox_clicked)
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
                                                 on_id_pagamento_customcombobox_clicked)
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                                 on_id_magazzino_customcombobox_clicked)

        self.fornitore_insegna = setconf("Fornitori", "fornitore_insegna")
        if not self.fornitore_insegna:
            self.insegna_entry.destroy()
            self.insegna_label.destroy()
        self.nome_entry.destroy()
        self.cognome_entry.destroy()
        self.cognome_label.destroy()
        self.nome_label.destroy()


    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Fornitore()
            self.dao.codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()

        if dao is None:
            self.dao_contatto = ContattoFornitore()
        else:
            self.dao_contatto = ContattoFornitore().select(idFornitore=self.dao.id)
            if self.dao_contatto:
                self.dao_contatto = self.dao_contatto[0]
            else:
                self.dao_contatto = ContattoFornitore()
        self._refresh()
        return self.dao

    def showTotaliDareAvere(self):

        if self.dao.id:
            #Calcoliamo il totale annuale:
            totaleAvereAnnuale = TotaleAnnualeFornitore(id_fornitore=self.dao.id)
            self.totale_annuale_avere_entry.set_text('%.2f' % totaleAvereAnnuale)
            #Calcoliamo il totale sospeso:
            totaleAvereSospeso = TotaleFornitoreAperto(id_fornitore=self.dao.id)
            self.totale_avere_entry.set_text('%.2f' % totaleAvereSospeso)
        self.anagrafica_fornitori_detail_notebook.set_current_page(0)


    def saveDao(self, tipo=None):
        if (self.ragione_sociale_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.ragione_sociale_entry,
                            msg='Campo obbligatorio !\n\nRagione sociale')
        #cod = Fornitore().select(codicesatto=self.codice_entry.get_text().upper().strip())
        #if cod:
            #obligatoryField(self.dialogTopLevel,
                            #self.ragione_sociale_entry,
                            #msg='CODICE GIÀ PRESENTE')
        #self.dao.codice = self.codice_entry.get_text().upper()
#        self.dao.codice = omogeneousCode(section="Fornitori", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        if self.fornitore_insegna:
            self.dao.insegna = self.insegna_entry.get_text()
#        self.dao.cognome= self.cognome_entry.get_text()
#        self.dao.nome = self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio.
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            messageInfo(msg=msg)
            raise Exception, 'Operation aborted: Codice Fornitore obbligatorio'
        self.dao.sede_operativa_indirizzo = self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_localita = self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_indirizzo = self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_localita = self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        self.dao.note = textview_get_text(self.note_textview)
        #if self.dao.codice_fiscale != '':
            #codfis = checkCodFisc(self.dao.codice_fiscale)
            #if not codfis:
                #raise Exception, 'Operation aborted: Codice fiscale errato'
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        #if self.dao.partita_iva != '':
            #partiva = checkPartIva(self.dao.partita_iva)
            #if not partiva:
                #raise Exception, 'Operation aborted: Partita iva errata'
        self.dao.id_categoria_fornitore = findIdFromCombobox(self.id_categoria_fornitore_customcombobox.combobox)
        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox,0)
        self.dao.persist()


        self.aggiungi_contatto_pg(self, "fornitore")

        self.save_contatto_cellulare_principale(self, self.dao_contatto)
        self.save_contatto_telefono_principale(self, self.dao_contatto)
        self.save_contatto_fax_principale(self, self.dao_contatto)
        self.save_contatto_email_principale(self, self.dao_contatto)
        self.save_contatto_sito_principale(self, self.dao_contatto)

    def on_scheda_contabile_togglebutton_clicked(self, toggleButton):
        """
        Apre la finestra di registrazione documenti, ricercando solo
        i documenti del fornitore
        """

        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter visualizzare la registrazione documenti occorre salvare il fornitore.\n Salvare? '
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                    self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagDocumenti.AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        anag.filter.id_fornitore_filter_customcombobox.setId(self.dao.id)
        anag.filter.solo_contabili_check.set_active(True)
        anag.filter.refresh()


    def on_icon_press_primary(self,entry,position,event):
        if position.value_nick == "primary":
            codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()
            self.codice_entry.set_text(codice)

    def on_contatti_togglebutton_clicked(self, toggleButton):
        if posso("CN"):
            if not(toggleButton.get_active()):
                toggleButton.set_active(False)
                return

            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il fornitore.\n Salvare ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
                else:
                    toggleButton.set_active(False)
                    return

            from promogest.ui.Contatti.AnagraficaContatti import AnagraficaContatti
            anag = AnagraficaContatti(self.dao.id, 'fornitore')
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

    def on_forniture_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire delle forniture occorre salvare il fornitore.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagForniture.AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(None, self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

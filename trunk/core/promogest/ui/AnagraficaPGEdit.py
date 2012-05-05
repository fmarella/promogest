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

#from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
#from promogest.ui.AnagraficaPGEdit import AnagraficaPGEdit
import promogest.dao.Fornitore
#from promogest.dao.Fornitore import Fornitore
#from promogest.modules.Contatti.dao.ContattoFornitore import ContattoFornitore
from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
from promogest.modules.Contatti.dao.Contatto import Contatto
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaPGEdit(object):
    """ Modifica un record dell'anagrafica dei fornitori """

    def __init__(self, tipo):
        self.tipo = tipo

    def _refresh(self):
        if self.dao.ragione_sociale:
            rag_soc= self.dao.ragione_sociale
        elif self.dao.cognome or self.dao.nome:
            rag_soc = str(self.dao.cognome)+" "+str(self.dao.nome)
        elif self.dao.insegna:
            rag_soc = self.dao.insegna
        else:
            rag_soc = ""
        self.codice_entry.set_text(self.dao.codice or '')
        self.ragione_sociale_entry.set_text(rag_soc)
        if self.fornitore_insegna:
            self.insegna_entry.set_text(self.dao.insegna or '')
#        self.cognome_entry.set_text(self.dao.cognome or '')
#        self.nome_entry.set_text(self.dao.nome or '')
        self.indirizzo_sede_operativa_entry.set_text(self.dao.sede_operativa_indirizzo or '')
        self.cap_sede_operativa_entry.set_text(self.dao.sede_operativa_cap or '')
        self.localita_sede_operativa_entry.set_text(self.dao.sede_operativa_localita or '')
        self.provincia_sede_operativa_entry.set_text(self.dao.sede_operativa_provincia or '')
        self.indirizzo_sede_legale_entry.set_text(self.dao.sede_legale_indirizzo or '')
        self.cap_sede_legale_entry.set_text(self.dao.sede_legale_cap or '')
        self.localita_sede_legale_entry.set_text(self.dao.sede_legale_localita or '')
        self.provincia_sede_legale_entry.set_text(self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(self.dao.partita_iva or '')
        textview_set_text(self.note_textview, self.dao.note or '')
        findComboboxRowFromId(self.id_categoria_fornitore_customcombobox.combobox,
                              self.dao.id_categoria_fornitore)
        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox,
                              self.dao.id_pagamento)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                              self.dao.id_magazzino)
        findComboboxRowFromStr(self.nazione_combobox,self.dao.nazione, 0)
        self.showTotaliDareAvere()
        self.cellulare_principale_entry.set_text(self.dao.cellulare_principale)
        self.telefono_principale_entry.set_text(self.dao.telefono_principale)
        self.email_principale_entry.set_text(self.dao.email_principale)
        self.fax_principale_entry.set_text(self.dao.fax_principale)
        self.sito_web_principale_entry.set_text(self.dao.sito_principale)


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


    def on_promemoria_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("PR"):
            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il Fornitore.\n Salvare ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
                else:
                    toggleButton.set_active(False)
                    return

            from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
            if self.dao.ragione_sociale:
                stringa = self.dao.ragione_sociale
            elif self.dao.cognome:
                stringa = self.dao.cognome
            else:
                stringa = None
            anag = AnagraficaPromemoria(pg=stringa)
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

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

            from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
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

    def on_label_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter stampare una label occorre salvare l\' il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                            self.dialogTopLevel,
                            GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        if posso("LA"):
            from promogest.modules.Label.ui.ManageLabelsToPrintCliente import\
                                                ManageLabelsToPrintCliente
            a = ManageLabelsToPrintCliente(mainWindow=self, daos=[],
                                                        cliente=self.dao)
            anagWindow = a.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            fencemsg()
        toggleButton.set_active(False)

    def save_contatto_telefono_principale(self,anagrafica, daocontatto):
        recont = RecapitoContatto().select(idContatto=daocontatto.id,
                                                    tipoRecapito="Telefono")
        if recont:
            reco = recont[0]
            if anagrafica.telefono_principale_entry.get_text() == "" or\
                                                     reco.recapito == "":
                reco.delete()
            else:
                reco.id_contatto = daocontatto.id
                reco.tipo_recapito = "Telefono"
                reco.recapito = anagrafica.telefono_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = daocontatto.id
            reco.tipo_recapito = "Telefono"
            reco.recapito = anagrafica.telefono_principale_entry.get_text()
            reco.persist()

    def save_contatto_cellulare_principale(self,anagrafica, daocontatto):
        recont = RecapitoContatto().select(idContatto=daocontatto.id,
                                        tipoRecapito="Cellulare")
        if recont:
            reco = recont[0]
            if anagrafica.cellulare_principale_entry.get_text() == "" or\
                                                 reco.recapito == "":
                reco.delete()
            else:
                reco.id_contatto = daocontatto.id
                reco.tipo_recapito = "Cellulare"
                reco.recapito = anagrafica.cellulare_principale_entry.get_text()
                reco.persist()

        else:
            reco = RecapitoContatto()
            reco.id_contatto = daocontatto.id
            reco.tipo_recapito = "Cellulare"
            reco.recapito = anagrafica.cellulare_principale_entry.get_text()
            reco.persist()

    def save_contatto_fax_principale(self,anagrafica, daocontatto):
        recont = RecapitoContatto().select(idContatto=daocontatto.id,
                                                    tipoRecapito="Fax")
        if recont:
            reco = recont[0]
            if anagrafica.fax_principale_entry.get_text() == "" or \
                                                   reco.recapito == "":
                reco.delete()
            else:
                reco.id_contatto = daocontatto.id
                reco.tipo_recapito = "Fax"
                reco.recapito = anagrafica.fax_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = daocontatto.id
            reco.tipo_recapito = "Fax"
            reco.recapito = anagrafica.fax_principale_entry.get_text()
            reco.persist()

    def save_contatto_email_principale(self,anagrafica, daocontatto):
        recont = RecapitoContatto().select(idContatto=daocontatto.id,
                                                        tipoRecapito="Email")
        if recont:
            reco = recont[0]
            if anagrafica.email_principale_entry.get_text() =="" or reco.recapito=="":
                reco.delete()
            else:
                reco.id_contatto = daocontatto.id
                reco.tipo_recapito = "Email"
                reco.recapito = anagrafica.email_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = daocontatto.id
            reco.tipo_recapito = "Email"
            reco.recapito = anagrafica.email_principale_entry.get_text()
            reco.persist()

    def save_contatto_sito_principale(self,anagrafica, daocontatto):
        recontw = RecapitoContatto().select(idContatto=daocontatto.id,
                                                    tipoRecapito="Sito")
        if recontw:
            recow = recontw[0]
            if anagrafica.sito_web_principale_entry.get_text() =="" or recow.recapito=="":
                recow.delete()
            else:
                recow.id_contatto = daocontatto.id
                recow.tipo_recapito = "Sito"
                recow.recapito = anagrafica.sito_web_principale_entry.get_text()
                recow.persist()
        else:
            recow = RecapitoContatto()
            recow.id_contatto = daocontatto.id
            recow.tipo_recapito = "Sito"
            recow.recapito = anagrafica.sito_web_principale_entry.get_text()
            recow.persist()


    def aggiungi_contatto_pg(self, anagrafica, tipo):
        if Environment.tipo_eng == "sqlite" and not self.dao_contatto.id:
            forMaxId = Contatto().select(batchSize=None)
            if not forMaxId:
                anagrafica.dao_contatto.id = 1
            else:
                idss = []
                for l in forMaxId:
                    idss.append(l.id)
                anagrafica.dao_contatto.id = (max(idss)) + 1
        appa = ""
        if anagrafica.dao.ragione_sociale:
            appa = appa + " " + anagrafica.dao.ragione_sociale
        if anagrafica.dao.cognome:
            appa = appa + " " + anagrafica.dao.cognome
        anagrafica.dao_contatto.cognome = appa
        if anagrafica.dao.nome:
            anagrafica.dao_contatto.nome = anagrafica.dao.nome
        anagrafica.dao_contatto.tipo_contatto = tipo
        anagrafica.dao_contatto.id_cliente = anagrafica.dao.id
        anagrafica.dao_contatto.persist()

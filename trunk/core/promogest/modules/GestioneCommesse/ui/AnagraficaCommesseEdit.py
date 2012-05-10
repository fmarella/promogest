# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import sys
from decimal import *
from promogest import Environment
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.modules.GestioneCommesse.dao.RigaCommessa import RigaCommessa
from promogest.dao.Cliente import Cliente
from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitore import Fornitore
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Vettore import Vettore
from promogest.dao.Promemoria import Promemoria
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *

class AnagraficaCommesseEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle commessa """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_commessa_detail_vbox',
                                'Dati della commessa cliente.',
                                gladeFile='GestioneCommesse/gui/_anagrafica_commessa_elements.glade',
                                module=True)
        self._widgetFirstFocus = self.titolo_commessa_entry
        self.anagrafica = anagrafica
        self.editRiga = None
        self.daoo = None
        self.dao_temp = None
        self.dao_class = None
        self.dao_id = None
        self.num = None
        self.aziendaStr = Environment.azienda

    def draw(self, cplx=False):

        fillComboboxStadioCommessa(self.stadio_commessa_combobox.combobox)
        self.stadio_commessa_combobox.connect('clicked',
                                            on_stadio_commessa_combobox_clicked)
        model = self.tipo_combobox.get_model()
        model.clear()
        self.tipiDict = {"":None,
                "DOCUMENTO":"TestataDocumento",
                "PROMEMORIA":"Promemoria",
                "FORNITORE":"Fornitore",
                "ARTICOLO":"Articolo",
                "VETTORE":"Vettore",
                "MAGAZZINO":"Magazzino",
                "CLIENTE":"Cliente",
                "AGENTE":"Agente"}
        for t in self.tipiDict.keys():
            model.append((t,))
        self.open_button.set_sensitive(False)
        self.trova_button.set_sensitive(False)
        self.new_dao_button.set_sensitive(False)
        self.stampa_dao_button.set_sensitive(False)


    def composeInfoDaoLabel(self, dao):
        info = ""
        if not dao:
            info = ""
        elif dao.__class__.__name__ == "TestataDocumento":
            info = "<b>%s</b>  - <b>del</b> %s <b>N°</b> %s - <b>Da/A</b> %s  - <b>TOT: €</b> %s" %(str(dao.operazione),
                                                                dateToString(dao.data_documento),
                                                                str(dao.numero),
                                                                dao.intestatario,
                                                                str(mN(dao._totaleScontato,2)))
        elif dao.__class__.__name__ == "Promemoria":
            info = "Promemoria <b>del</b> %s  <b>Descr:</b> %s" %(str(dateToString(dao.data_inserimento)),
            dao.descrizione[0:50])
        elif dao.__class__.__name__ in ["Cliente", "Fornitore", "Vettore", "Agente"]:
            info = "<b>%s</b>,  %s , %s %s" %(str(dao.__class__.__name__),
                                        dao.ragione_sociale,
                                        dao.cognome,
                                        dao.nome)
        elif dao.__class__.__name__ =="Magazzino":
            info = "Magazzino: %s , %s " %(str(dao.denominazione), str(dao.pvcode))
        self.info_dao_label.set_markup(info)


    def on_tipo_combobox_changed(self, combobox):
        """ """
        self.open_button.set_sensitive(False)
        self.trova_button.set_sensitive(False)
        self.new_dao_button.set_sensitive(False)
        self.stampa_dao_button.set_sensitive(False)
        self.tipo_dao = combobox.get_model().get_value(combobox.get_active_iter(), 0).lower()
        if self.tipo_dao:
#            self.open_button.set_sensitive(True)
            self.trova_button.set_sensitive(True)
            self.new_dao_button.set_sensitive(True)
#            self.stampa_dao_button.set_sensitive(True)
        else:
            self.composeInfoDaoLabel(None)

    def on_new_dao_button_clicked(self, button):
        if self.tipo_dao == "DOCUMENTO".lower():
            from promogest.ui.AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()
        elif self.tipo_dao == "ARTICOLO".lower():
            from promogest.ui.anagArti.AnagraficaArticoli import AnagraficaArticoli
            anag = AnagraficaArticoli(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()
        elif self.tipo_dao == "CLIENTE".lower():
            from promogest.ui.AnagraficaClienti import AnagraficaClienti
            anag = AnagraficaClienti(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()
        elif self.tipo_dao == "VETTORE".lower():
            from promogest.ui.AnagraficaVettori import AnagraficaVettori
            anag = AnagraficaVettori(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()
        elif self.tipo_dao == "FORNITORE".lower():
            from promogest.ui.AnagraficaFornitori import AnagraficaFornitori
            anag = AnagraficaFornitori(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()
        elif self.tipo_dao == "PROMEMORIA".lower():
            from promogest.ui.anagPromemoria.AnagraficaPromemoria import AnagraficaPromemoria
            anag = AnagraficaPromemoria(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag)
            anag.on_record_new_activate()

#        from promogest.ui.Contatti.AnagraficaContatti import AnagraficaContatti
#        anag = AnagraficaContatti(self.aziendaStr)
#        showAnagrafica(self.getTopLevel(), anag)
#        anag.on_record_new_activate()

    def on_trova_button_clicked(self, button):
#        self.new_dao_button.set_sensitive(False)
        def returnDao(anagWindow):
            if anag.dao:
                self.dao_temp = anag.dao
                self.composeInfoDaoLabel(anag.dao)
                self.open_button.set_sensitive(True)
                self.stampa_dao_button.set_sensitive(True)
            else:
                self.dao_temp = None

        if self.tipo_dao !="":
            if self.tipo_dao =="DOCUMENTO".lower():
                from promogest.ui.SimpleSearch.RicercaDocumenti import RicercaDocumenti
                anag = RicercaDocumenti()
            elif self.tipo_dao =="PROMEMORIA".lower():
                from promogest.ui.SimpleSearch.RicercaPromemoria import RicercaPromemoria
                anag = RicercaPromemoria()
            elif self.tipo_dao =="FORNITORE".lower():
                from promogest.ui.SimpleSearch.RicercaFornitori import RicercaFornitori
                anag = RicercaFornitori()
            elif self.tipo_dao =="ARTICOLO".lower():
                from promogest.ui.SimpleSearch.RicercaArticoli import RicercaArticoli
                anag = RicercaArticoli()
            elif self.tipo_dao =="VETTORE".lower():
                from promogest.ui.SimpleSearch.RicercaVettori import RicercaVettori
                anag = RicercaVettori()
            elif self.tipo_dao =="MAGAZZINO".lower():
                from promogest.ui.SimpleSearch.RicercaMagazzini import RicercaMagazzini
                anag = RicercaMagazzini()
            elif self.tipo_dao =="CLIENTE".lower():
                from promogest.ui.SimpleSearch.RicercaClienti import RicercaClienti
                anag = RicercaClienti()
            elif self.tipo_dao =="AGENTE".lower():
                from promogest.ui.SimpleSearch.RicercaAgenti import RicercaAgenti
                anag = RicercaAgenti()
            anagWindow = anag.getTopLevel()
            anagWindow.show_all()
            anagWindow.connect("hide",returnDao)


    def setDao(self, dao):
        if dao is None:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataCommessa()
            a = select([func.max(TestataCommessa.numero)]).execute().fetchall() or 0
            numero = 0
            if a:
                numero = a[0][0] or 0
            self.dao.numero = numero+1
        else:
            self.dao = TestataCommessa().getRecord(id=dao.id)
        self._refresh()
        return self.dao


    def _refresh(self):
        """ Funzione che ricarica i dati in gui"""
        self.data_inizio_commessa_entry.set_text(dateToString(self.dao.data_inizio))
        self.data_fine_commessa_entry.set_text(dateToString(self.dao.data_fine))
        self.titolo_commessa_entry.set_text(self.dao.denominazione or "")
        bufferNote= self.commessa_testo.get_buffer()
        bufferNote.set_text(self.dao.note or "")
        self.commessa_testo.set_buffer(bufferNote)
        findComboboxRowFromId(self.stadio_commessa_combobox.combobox, self.dao.id_stadio_commessa)
#        findComboboxRowFromId(self.id_cliente_combobox, self.dao.id_cliente)
        self.id_cliente_combobox.setId(self.dao.id_cliente)
        self.id_articolo_combobox.setId(self.dao.id_articolo)
#        self.stadio_commessa_combobox.setId( self.dao.id_stadio_commessa)
#        findComboboxRowFromId(self.id_articolo_combobox, self.dao.id_articolo)

        model = self.riga_commessa_treeview.get_model()
        model.clear()
        for r in self.dao.righecommessa:
            if r.dao_class=="TestataDocumento":
                td = TestataDocumento().getRecord(id=r.id_dao)
                dc = td.operazione
            else:
                dc = r.dao_class
            model.append((r, str(len(model)+1),
                        dateToString(r.data_registrazione),
                        r.denominazione,
                        dc,
                        r.note,
                        r.dao_class,
                        str(r.id_dao)))


    def clear(self):
        self.data_ins_riga.set_text("")
        bufferNoteRiga= self.riga_testo.get_buffer()
        bufferNoteRiga.set_text("")
        self.riga_testo.set_buffer(bufferNoteRiga)
        self.info_dao_label.set_text("-")
        self.titolo_riga_commessa_entry.set_text("")
        self.tipo_combobox.set_active(0)
        self.composeInfoDaoLabel(None)

    def on_delete_row_button_clicked(self, button):
        """ Elimina la riga commessa selezionata"""
        rpn = None
        if self.editRiga:
            dao = RigaCommessa().getRecord(id=self.editRiga.id)
            if dao:
                dao.delete()
            self._editModel.remove(self._editIterator)
            self.clear()


    def on_add_row_button_clicked(self, button):
        """ Aggiunge la riga """
        titolo_riga = self.titolo_riga_commessa_entry.get_text()
        if not titolo_riga:
            titolo_riga = self.info_dao_label.get_text()
        bufferNoteRiga= self.riga_testo.get_buffer()
        note_riga = bufferNoteRiga.get_text(bufferNoteRiga.get_start_iter(), bufferNoteRiga.get_end_iter(),True) or ""
        if self.dao_temp:
            self.dao_id = self.dao_temp.id
            self.dao_class = self.dao_temp.__class__.__name__

        if titolo_riga =="" or titolo_riga =="-":
            obligatoryField(self.dialogTopLevel, self.titolo_riga_commessa_entry,
            msg="Campo obbligatorio: TITOLO RIGA!")
        data_ins_riga = dateToString(self.data_ins_riga.get_text())

        model = self.riga_commessa_treeview.get_model()
        if self.editRiga:
            riga = self.editRiga
            riga.numero = self.editRiga.numero
        else:
            riga = RigaCommessa()
            riga.numero = len(model)+1
        riga.dao_class = self.dao_class
        riga.id_dao = self.dao_id
        riga.data_registrazione = stringToDate(data_ins_riga)
        riga.denominazione = titolo_riga
        riga.note = note_riga
        if self.dao_class =="TestataDocumento":
            dc = self.dao_temp.operazione
        else:
            dc = self.dao_class
        dati = (riga,str(len(model)+1),data_ins_riga,
                        titolo_riga,
                        str(dc),
                        note_riga,
                        self.dao_class,
                        str(self.dao_id))
        if self.editRiga:
            if riga.dao_class=="TestataDocumento":
                td = TestataDocumento().getRecord(id=riga.id_dao)
                dc = td.operazione
            else:
                dc = riga.dao_class
            self.rigaIter[0] = riga
            self.rigaIter[1] = str(riga.numero)
            self.rigaIter[2] = dateToString(riga.data_registrazione)
            self.rigaIter[3] = riga.denominazione[0:100]
            self.rigaIter[4] =  dc
            self.rigaIter[5] =  riga.note
            self.rigaIter[6] =  riga.dao_class
            self.rigaIter[7] =  riga.id_dao
        else:
            model.append(dati)
        self.riga_commessa_treeview.set_model(model)
        self.editRiga = None

        self.clear()

    def daoRetreive(self,daoId, daoName):
        """Funzione che restituisce un dao, dato una classe come stringa, ed un id
        """
        if daoName:
            return getattr(sys.modules[__name__], daoName)().getRecord(id=daoId)
        else:
            return None

    def on_rimuovi_button_clicked(self, button):
        """ Elimina la riga di prima nota selezionata
        """
        if self.editRiga:
            dao = RigaCommessa().getRecord(id=self.editRiga.id)
            dao.delete()
            self._editModel.remove(self._editIterator)
            self.clear()

    def on_riga_commessa_treeview_row_activated(self,treeview, path, column):
        """Selezione della riga nella treeview
        """
        self.composeInfoDaoLabel(None)
        self.dao_temp = None
        sel = self.riga_commessa_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model
        self.data_ins_riga.set_text(self.rigaIter[2] or "")
        self.titolo_riga_commessa_entry.set_text(self.rigaIter[3] or "")
        bufferNoteRiga= self.riga_testo.get_buffer()
        bufferNoteRiga.set_text(self.rigaIter[5] or "")
        self.riga_testo.set_buffer(bufferNoteRiga)
        self.dao_id = self.rigaIter[7]
        self.dao_class = self.rigaIter[6]
        self.dao_temp = self.daoRetreive(self.dao_id, self.dao_class)
        self.composeInfoDaoLabel(self.dao_temp)
        model = self.tipo_combobox.get_model()
        for r in model:
            if self.tipiDict[r[0]] == self.dao_class:
                self.tipo_combobox.set_active_iter(r.iter)

        self.editRiga = self.rigaIter[0]


    def saveDao(self, chiusura=False, tipo=None):
        """ Salvataggio della commessa nel tabase
        """
        model = self.riga_commessa_treeview.get_model()
        righe_ = []
        for m in model:
            righe_.append(m[0])
        self.dao.data_inizio = stringToDate(self.data_inizio_commessa_entry.get_text())
        if (self.dao.data_inizio == ''or self.dao.data_inizio==None):
            obligatoryField(self.dialogTopLevel,
                    self.data_inizio_commessa_entry,
                    'Inserire la data della commessa !')
        self.dao.data_fine = stringToDate(self.data_fine_commessa_entry.get_text())
        self.dao.denominazione = self.titolo_commessa_entry.get_text()
        if self.dao.denominazione =="":
            obligatoryField(self.dialogTopLevel, self.titolo_commessa_entry,
            msg="Campo obbligatorio: TITOLO COMMESSA!")
        bufferNoteRiga= self.commessa_testo.get_buffer()
        self.dao.note = bufferNoteRiga.get_text(bufferNoteRiga.get_start_iter(), bufferNoteRiga.get_end_iter(),True) or ""
        self.dao.righecommessa = righe_
        self.dao.id_stadio_commessa = findIdFromCombobox(self.stadio_commessa_combobox.combobox)
        self.dao.id_cliente = findIdFromCombobox(self.id_cliente_combobox)
        self.dao.id_articolo =findIdFromCombobox(self.id_articolo_combobox)
        if self.dao.id_cliente == None:
            obligatoryField(self.dialogTopLevel, self.id_cliente_combobox,
            msg="Campo obbligatorio: CLIENTE!")
        self.dao.persist()
        self.clear()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
#    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button,mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
#    anagWindow.set_transient_for(window)
#    setattr(anagWindow, "mainClass",mainClass)
    anagWindow.show_all()

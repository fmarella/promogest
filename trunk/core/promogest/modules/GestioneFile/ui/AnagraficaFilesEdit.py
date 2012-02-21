# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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


from decimal import *
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaFilesEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle prima nota cassa """
    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'anagrafica_gestione_file_detail_vbox',
                'Informazioni File.',
                gladeFile='GestioneFile/gui/_anagrafica_gestione_file_elements.glade',
                module=True)
        self._widgetFirstFocus = self.data_inserimento_datewidget
        self.anagrafica = anagrafica
        self.editRiga = None
#        self.rotazione = setconf("rotazione_primanota", "Primanota")
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
                                 on_id_banca_customcombobox_clicked)

    def on_come_combobox_changed(self, combobox):
        come = findStrFromCombobox(self.come_combobox,0).lower()
        if come =="banca":
            self.id_banca_customcombobox.set_sensitive(True)
        else:
            self.id_banca_customcombobox.set_sensitive(False)


    def draw(self, cplx=False):
#        self.banca_viewport.set_property("visible",False)
        return

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = TestataPrimaNota()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataPrimaNota().getRecord(id=dao.id)
        self._refresh()
        return self.dao


    def _refresh(self):
#        self.id_banca_customcombobox.hide()
        self.note_entry.set_sensitive(False)
        self.numero_label.set_text(str(self.dao.numero or ""))
        self.note_entry.set_text(self.dao.note or "")
        self.data_inserimento_datewidget.set_text(dateToString(self.dao.data_inizio) or "")
        self.primanota_riga_listore.clear()
        riferimento = ""
        if self.dao.note or len(self.dao.righeprimanota):
            self.note_entry.set_sensitive(True)
        for r in self.dao.righeprimanota:
            if r.segno == "uscita":
                col_valore = "#FFD7D7"
                valore = -1*mN(r.valore)
            else:
                col_valore = "#CCFFAA"
                valore =mN(r.valore)
            if r.tipo =="cassa":
                col_tipo = "#FFF2C7"
            elif r.tipo=="banca":
                col_tipo = "#CFF5FF"
            else:
                col_tipo = ""
            banca = ""
            if r.id_banca:
                banca = getDenominazioneBanca(r.id_banca)
            self.primanota_riga_listore.append((r,
                                                r.denominazione,
                                                str(valore),
                                                str(r.tipo),
                                                str(banca) or "",
                                                riferimento or "",
                                                col_valore,
                                                col_tipo))

    def saldo(self):
        tutte = TestataPrimaNota().select(batchSize=None)
        saldo_precedente = 0
        for t in tutte:
            if t.numero < self.dao.numero:
                saldo_precedente += t.totali["totale"]
        return mN(saldo_precedente)

    def clear(self):
        self.valore_entry.set_text("")
        self.denominazione_entry.set_text("")
        self.id_banca_customcombobox.combobox.set_active(-1)
        textview_set_text(self.note_textview, '')
        self.aggiungi_button.set_label("Aggiungi")
        image = GTK_IMAGE_NEW_FROM_STOCK(gtk.STOCK_ADD, GTK_ICON_SIZE_BUTTON)
        self.aggiungi_button.set_image(image)

    def on_aggiungi_button_clicked(self, button):
        """ Aggiunge la riga con i campi di denominazione e valore cassa o banca
            entrata o uscita """
        if self.denominazione_entry.get_text() == '' or \
            self.denominazione_entry.get_text == None:
            obligatoryField(self.dialogTopLevel, self.denominazione_entry,
            msg="Campo obbligatorio: DENOMINAZIONE!")

        if self.data_inserimento_datewidget.get_text() == "" or \
            self.data_inserimento_datewidget.get_text() == None:
            obligatoryField(self.dialogTopLevel, self.data_inserimento_datewidget,
            msg="Campo obbligatorio: DATA INSERIMENTO!")

        model = self.primanota_riga_listore
        if self.editRiga:
            riga = self.editRiga
        else:
            riga = RigaPrimaNota()
        riga.numero = 1
        data_registrazione = stringToDate(self.data_inserimento_datewidget.get_text())
        riga.data_registrazione = data_registrazione
        denominazione = self.denominazione_entry.get_text()
        riga.denominazione = denominazione
        if self.valore_entry.get_text().replace(",", ".").strip() in ["", None, "0"]:
            messageInfo(msg="ATTENZIONE!\n\nVALORE  = <b>zero</b>")

        valore = Decimal(self.valore_entry.get_text().replace(",", ".").strip() or 0)
        riga.valore = valore
        tipo_operazione = "entrata"
        riga.segno = tipo_operazione
        col_valore = "#CCFFAA"
        if self.tipo_uscita_radio.get_active():
            tipo_operazione = "uscita"
            if valore >0:
                valore = valore*(-1)
            col_valore = "#FFD7D7"
            riga.segno = tipo_operazione

        riga.operazione = tipo_operazione
        come = findStrFromCombobox(self.come_combobox,0).lower()
        riga.tipo = come
        if come =="cassa":
            col_tipo = "#FFF2C7"
        elif come=="banca":
            col_tipo = "#CFF5FF"
        else:
            col_tipo = ""
        riferimento = None
#            if (findIdFromCombobox(self.id_banca_customcombobox.combobox) is None):
#                obligatoryField(self.dialogTopLevel,
#                        self.id_banca_customcombobox,
#                        'Inserire un riferimento ad una banca !')

        riga.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        banca = ""
        if riga.id_banca:
            banca = getDenominazioneBanca(riga.id_banca)
        riga.note_primanota = textview_get_text(self.note_textview)
        dati = (riga,
                        denominazione,
                        str(mN(valore,2)),
                        str(come),
                        str(banca),
                        riferimento or "",
                        col_valore,
                        col_tipo)
        if self.editRiga:
            self.rigaIter[0] = riga
            self.rigaIter[1] = denominazione
            self.rigaIter[2] = str(valore) or ""
            self.rigaIter[3] = str(come)
            self.rigaIter[4] = str(banca) or ""
            self.rigaIter[5] = str(riferimento)
        else:
            model.append(dati)
        if len(model) >1:
            self.note_entry.set_sensitive(True)
            messageInfo(msg="Ricordiamo che con più operazioni si deve inserire una nota nel campo note")
            self.note_entry.grab_focus()

        self.riga_primanota_treeview.set_model(model)
        self.editRiga = None
        self.clear()

    def on_attiva_note_toggled_toggled(self, button):
        if button.get_active():
            self.note_entry.set_sensitive(True)
        else:
            self.note_entry.set_sensitive(False)

    def on_rimuovi_button_clicked(self, button):
        """ Elimina la riga di prima nota selezionata"""
        rpn = None
        if self.editRiga:
            dao = RigaPrimaNota().getRecord(id=self.editRiga.id)
            if dao:
                rpn = RigaPrimaNotaTestataDocumentoScadenza().select(idRigaPrimaNota=dao.id)
            if rpn:
                for r in rpn:
                    r.delete()
            if dao:
                dao.delete()
            self._editModel.remove(self._editIterator)
            self.clear()

    def on_riga_primanota_treeview_row_activated(self, treeview, path, column):
        self.aggiungi_button.set_label("Aggiorna")
        image = GTK_IMAGE_NEW_FROM_STOCK(gtk.STOCK_REFRESH, GTK_ICON_SIZE_BUTTON)
        self.aggiungi_button.set_image(image)
        sel = self.riga_primanota_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model
#        self.data_inserimento_datewidget.set_text(self.rigaIter[3])
        if self.rigaIter[0].segno == "entrata":
            self.tipo_entrata_radio.set_active(True)
            self.valore_entry.set_text(self.rigaIter[2])
        else:
            self.tipo_uscita_radio.set_active(True)
            if Decimal(self.rigaIter[2]) > 0:
                self.valore_entry.set_text(self.rigaIter[2])
            else:
                self.valore_entry.set_text(str(-1*(Decimal(self.rigaIter[2]))))


        if self.rigaIter[4] != "":
#            self.uscita_banca_radio.set_active(True)
            findComboboxRowFromStr(self.come_combobox,"BANCA",0)
            findComboboxRowFromId(self.id_banca_customcombobox.combobox, self.rigaIter[0].id_banca)
            self.id_banca_customcombobox.set_sensitive(True)

        self.denominazione_entry.set_text(self.rigaIter[1])
        textview_set_text(self.note_textview, self.rigaIter[0].note_primanota or '')
        self.editRiga = self.rigaIter[0]

    def saveDao(self, chiusura=False, tipo=None):
        if not self.dao.numero:
            date = Environment.workingYear
            numeroSEL= TestataPrimaNota().select(complexFilter=(and_(TestataPrimaNota.data_inizio.between(datetime.date(int(date), 1, 1), datetime.date(int(date) + 1, 1, 1)))), batchSize=None)
            if numeroSEL:
                numero = max([p.numero for p in numeroSEL]) +1
            else:
                numero = 1
            self.dao.numero = numero
        self.dao.data_inizio = stringToDate(self.data_inserimento_datewidget.get_text())
        if self.dao.data_inizio == '' or self.dao.data_inizio ==None:
            obligatoryField(None,self.data_inserimento_datewidget)
        righe_ = []
        for m in self.primanota_riga_listore:
            righe_.append(m[0])
        if (len(righe_)==0):
            messageInfo(msg="L'INSERIMENTO DI UNA OPERAZIONE È OBBLIGATORIO")
            raise Exception, 'Operation aborted campo obbligatorio'
        self.dao.note = self.note_entry.get_text()
        self.dao.righeprimanota = righe_
        self.dao.persist()
        self.clear()

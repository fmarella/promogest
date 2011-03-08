# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005,2006,2007,2008,2009,2010,2011,
#                         by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
from promogest.ui.utils import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.InfoPeso.dao.TipoTrattamento import TipoTrattamento
from promogest.modules.InfoPeso.dao.TestataInfoPeso import TestataInfoPeso
from promogest.modules.InfoPeso.dao.RigaInfoPeso import RigaInfoPeso

from promogest.modules.InfoPeso.dao.ClienteGeneralita import ClienteGeneralita


class InfoPesoNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn, azienda):
        GladeWidget.__init__(self, 'infopeso_frame',
                                    'InfoPeso/gui/infopeso_notebook.glade',
                                    isModule=True)
        self.rowBackGround = None
        self.ana = mainnn
        self.aziendaStr = azienda or ""
        self.editRiga = None
        self.draw()

    def draw(self):
        """
        TreeView creata con GLADE
        MODEL: (object, str, str, str, str, str, str, str, str, str)
        'Data Pesata', rendererCtr, text=1, background=9
        'Peso', renderer, text=2, background=9
        'Diff Peso', renderer, text=3, background=9
        'M.Grassa', rendererCtr, text=4, background=9
        'M.Magra&Acq.', rendererCtr, text=5, background=9
        'Acqua', renderer, text=6, background=9
        'Tipo Trattamento', renderer, text=7, background=9
        'Note', renderer, text=8, background=9
        """
        fillComboboxTipoTrattamento(self.id_tipo_trattamento_customcombobox.combobox)
        self.id_tipo_trattamento_customcombobox.connect('clicked',
                                 on_id_tipo_trattamento_customcombobox_clicked)
        self.nome_cognome_label.set_text("")
        self._clear()

    def _calcolaDifferenzaPeso(self):
        model = self.righe_pesata_treeview.get_model()
        diff_peso = []
        for m in model:
            diff_peso.append((stringToDate(m[1]), m[2], m, m[0], m[9]))
        diff_peso.sort()
        for i in range(1, len(diff_peso)):
            if i < len(diff_peso):
                for m in model:
                    if m[0] == diff_peso[i][3]:
                        diffe = (Decimal(diff_peso[i][1]) - Decimal(diff_peso[i-1][1]))
                        m[3] = str(diffe)
                        if diffe<0:
                            m[9] = "#CCFFAA"
                        elif diffe>0 :
                            m[9] = "#FFD7D7"
        self.righe_pesata_treeview.set_model(model)


    def on_aggiungi_pesata_button_clicked(self, button):

        data_pesata = self.data_pesata_datewidget.get_text()
        peso = self.peso_pesata_entry.get_text() or "0"
        mgrassa = self.massa_grassa_entry.get_text() or "0"
        mmagraeacqua = self.massa_magra_e_acqua_entry.get_text() or "0"
        acqua = self.acqua_entry.get_text() or "0"
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        note_riga = bufferNoteRiga.get_text(bufferNoteRiga.get_start_iter(), bufferNoteRiga.get_end_iter()) or ""

        if not data_pesata:
            obligatoryField(None,
                    self.data_pesata_datewidget,
                    'Inserire una data pesata !')
        if not peso:
            obligatoryField(None,
                    self.peso_pesata_entry,
                    'Inserire un peso !')

        if float(mgrassa.replace(",","."))+float(mmagraeacqua.replace(",",".")) > float(peso.replace(",",".")):
            messageInfo(msg = "ATTENZIONE! La somma di M.GRASSA , M.MAGRA e ACQUA\n è superiore al peso totale")
            return

        if float(mmagraeacqua.replace(",",".")) < float(acqua.replace(",",".")):
            messageInfo(msg = "ATTENZIONE! La M.MAGRA e ACQUA\n è inferiore alla sola ACQUA")
            return

        model = self.righe_pesata_treeview.get_model()
        modelo = len(model)
        if self.editRiga:
            riga = self.editRiga
            riga.numero = self.editRiga.numero
        else:
            riga = RigaInfoPeso()
            riga.numero =len(model)+1

        tipo_tratt = findStrFromCombobox(self.id_tipo_trattamento_customcombobox.combobox,2)
        riga.id_tipo_trattamento = findIdFromCombobox(self.id_tipo_trattamento_customcombobox.combobox)
        riga.data_registrazione = stringToDate(data_pesata)
        riga.note = note_riga
        riga.peso = Decimal(peso.replace(",","."))
        riga.massa_grassa = Decimal(mgrassa.replace(",","."))
        riga.massa_magra_e_acqua = Decimal(mmagraeacqua.replace(",","."))
        riga.acqua = Decimal(acqua.replace(",","."))
        if self.editRiga:
            self.rigaIter[0] = riga
#            self.rigaIter[1] = str(riga.numero)
            self.rigaIter[1] = dateToString(riga.data_registrazione)
            self.rigaIter[2] = str(mN(riga.peso,1))
            self.rigaIter[3] = str(0)
            self.rigaIter[4] = str(mN(riga.massa_grassa,1))
            self.rigaIter[5] = str(mN(riga.massa_magra_e_acqua,1))
            self.rigaIter[6] = str(mN(riga.acqua,1))
            self.rigaIter[7] = str(tipo_tratt)
            self.rigaIter[8] = str(riga.note)
        else:
            riga = (riga,
                        dateToString(data_pesata),
                        str(mN(peso,1)) or "",
                        str("0"),
                        str(mN(mgrassa,1)) or "",
                        str(mN(mmagraeacqua,1)) or "",
                        str(mN(acqua,1)) or "",
                        str(tipo_tratt),
                        str(note_riga.replace("\n"," ")[0:100]),
                        "#FFFFFF")
            a = 0
            for m in model:
                if stringToDate(data_pesata) < stringToDate(m[1]):
                    a =a+1
                elif stringToDate(data_pesata) > stringToDate(m[1]):
                    model.insert(a,riga)
                    break
        self.righe_pesata_treeview.set_model(model)
        self._calcolaDifferenzaPeso()

        self._clear()
        if len(model)>0:
            self.righe_pesata_treeview.scroll_to_cell("0")
#        self.righe_pesata_treeview.scroll_to_cell(str(modelo-1))

    def _clear(self):
        self.data_pesata_datewidget.set_text("")
        self.peso_pesata_entry.set_text("")
        self.massa_grassa_entry.set_text("")
        self.massa_magra_e_acqua_entry.set_text("")
        self.acqua_entry.set_text("")
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        bufferNoteRiga.set_text("")
        self.id_tipo_trattamento_customcombobox.combobox.set_active(-1)

    def on_elimina_pesata_button_clicked(self, button):
        rpn = None
        if self.editRiga:
            dao = RigaInfoPeso().getRecord(id=self.editRiga.id)
            if dao:
                dao.delete()
            self._editModel.remove(self._editIterator)
            self._clear()
        self._calcolaDifferenzaPeso()

    def on_righe_pesata_treeview_row_activated(self, treeview, path, column):
        (model, iterator) = self.righe_pesata_treeview.get_selection().get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model

        self.data_pesata_datewidget.set_text(self.rigaIter[1] or "")
        self.peso_pesata_entry.set_text(self.rigaIter[2] or "")
        self.massa_grassa_entry.set_text(self.rigaIter[4] or "")
        self.massa_magra_e_acqua_entry.set_text(self.rigaIter[5] or "")
        self.acqua_entry.set_text(self.rigaIter[6] or "")
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        bufferNoteRiga.set_text(self.rigaIter[8] or "")
        self.note_riga_pesata_textview.set_buffer(bufferNoteRiga)

        findComboboxRowFromStr(self.id_tipo_trattamento_customcombobox.combobox, self.rigaIter[7] or "",2)

        self.editRiga = self.rigaIter[0]

    def infoPesoSetDao(self, dao):
        """ Estensione del SetDao principale"""
        self.editRiga = None
        if not dao.id:
            self.dao_testata_infopeso = TestataInfoPeso()
            self.dao_generalita_infopeso = ClienteGeneralita()
        else:
            self.dao_testata_infopeso = TestataInfoPeso().select(idCliente=dao.id)
            self.dao_generalita_infopeso = ClienteGeneralita().select(idCliente = dao.id)
            if self.dao_testata_infopeso:
                self.dao_testata_infopeso = self.dao_testata_infopeso[0]
            else:
                self.dao_testata_infopeso = TestataInfoPeso()
            if self.dao_generalita_infopeso:
                self.dao_generalita_infopeso = self.dao_generalita_infopeso[0]
            else:
                self.dao_generalita_infopeso = ClienteGeneralita()
        self.infoPeso_refresh()

    def infoPeso_refresh(self):
        self.editRiga= None
        self.data_infopeso_datewidget.set_text(dateToString(self.dao_testata_infopeso.data_inizio) or dateToString(datetime.date.today))
        self.data_fine_datewidget.set_text(dateToString(self.dao_testata_infopeso.data_fine))
        self.privacy_check.set_active(int(self.dao_testata_infopeso.privacy or 0))
        bufferNote = self.note_textview.get_buffer()
        bufferNote.set_text(self.dao_testata_infopeso.note or "")
        self.note_textview.set_buffer(bufferNote)
        self.citta_centro_entry.set_text(self.dao_testata_infopeso.citta or "")

        self.data_nascita_datewidget.set_text(dateToString(self.dao_generalita_infopeso.data_nascita))
        self.altezza_entry.set_text(str(mN(self.dao_generalita_infopeso.altezza,1) or ""))
        if self.dao_generalita_infopeso.genere =="Donna":
            self.donna_radio.set_active(True)
        else:
            self.donna_radio.set_active(False)

        model = self.righe_pesata_treeview.get_model()
        model.clear()
        for m in self.dao_testata_infopeso.righeinfopeso:
            model.append((m,
                        dateToString(m.data_registrazione),
                        str(mN(m.peso,1)) or "",
                        str("0"),
                        str(mN(m.massa_grassa,1)) or "",
                        str(mN(m.massa_magra_e_acqua,1)) or "",
                        str(mN(m.acqua,1)) or "",
                        str(m.tipotrattamento),
                        str(m.note.replace("\n"," ")[0:100]),
                        "#FFFFFF"
                        ))
        self.righe_pesata_treeview.set_model(model)
        if len(model)>0:
            self.righe_pesata_treeview.scroll_to_cell("0")
        self._calcolaDifferenzaPeso()
        self._clear()

    def infoPesoSaveDao(self):
        self.dao_testata_infopeso.data_inizio= stringToDate(self.data_infopeso_datewidget.get_text())
        self.dao_testata_infopeso.data_fine = stringToDate(self.data_fine_datewidget.get_text())
        self.dao_testata_infopeso.privacy = self.privacy_check.get_active()
        bufferNote= self.note_textview.get_buffer()
        self.dao_testata_infopeso.note = bufferNote.get_text(bufferNote.get_start_iter(), bufferNote.get_end_iter()) or ""
        self.dao_testata_infopeso.citta = self.citta_centro_entry.get_text()

        self.dao_generalita_infopeso.data_nascita = stringToDate(self.data_nascita_datewidget.get_text())
        self.dao_generalita_infopeso.altezza = self.altezza_entry.get_text().replace(",",".") or 0

        if self.donna_radio.get_active():
            self.dao_generalita_infopeso.genere = "Donna"
        else:
            self.dao_generalita_infopeso.genere = "Uomo"

        righe = []
        model = self.righe_pesata_treeview.get_model()
        for m in model:
            righe.append(m[0])

        self.dao_testata_infopeso.righeinfopeso = righe
        return (self.dao_generalita_infopeso, self.dao_testata_infopeso)

def fillComboboxTipoTrattamento(combobox, filter=False):
    """ Riempi combo degli stadi commessa """
    model = gtk.ListStore(object, int, str)
    stcom = TipoTrattamento().select(batchSize=None)
    if not filter:
        emptyRow = ''
    model.append((None, 0, emptyRow))
    for c in stcom:
        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def on_id_tipo_trattamento_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica tipo trattamento
    """
    def on_anagrafica_tipo_trattamento_articoli_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxTipoTrattamento(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.InfoPeso.ui.AnagraficaTipotrattamento import AnagraficaTipoTrattamento
    anag = AnagraficaTipoTrattamento()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_tipo_trattamento_articoli_destroyed)

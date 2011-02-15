# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
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
        """
        """
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

class InfoPesoNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn, azienda):
        GladeWidget.__init__(self, 'infopeso_frame',
                                    'InfoPeso/gui/infopeso_notebook.glade',
                                    isModule=True)
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.ana = mainnn
        self.aziendaStr = azienda or ""
        self.editRiga = None
        print self.ana.ragione_sociale_entry.get_text()
        print self.ana.insegna_entry.get_text()
        print self.ana.cognome_entry.get_text()
        print self.ana.nome_entry.get_text()
        self.draw()

    def draw(self):
        """
        disegna questo frame nella finestra principale
        """
        treeview = self.righe_pesata_treeview
        renderer = gtk.CellRendererText()
        rendererCtr = gtk.CellRendererText()
        rendererCtr.set_property('xalign', 0.5)

        column = gtk.TreeViewColumn('Data Pesata', rendererCtr, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(120)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Peso', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Diff Peso', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('M.Grassa', rendererCtr, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('M.Magra&Acq.', rendererCtr, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Acqua', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo Trattamento', renderer, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
#        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Note', renderer, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        model = gtk.ListStore(object, str, str, str, str, str, str, str, str)
        treeview.set_model(model)

        fillComboboxTipoTrattamento(self.id_tipo_trattamento_customcombobox.combobox)
        self.id_tipo_trattamento_customcombobox.connect('clicked',
                                 on_id_tipo_trattamento_customcombobox_clicked)
        self.nome_cognome_label.set_text("")

    def on_aggiungi_pesata_button_clicked(self, button):

        data_pesata = self.data_pesata_datewidget.get_text()
        peso = self.peso_pesata_entry.get_text() or "0"
        mgrassa = self.massa_grassa_entry.get_text() or "0"
        mmagraeacqua = self.massa_magra_e_acqua_entry.get_text() or "0"
        acqua = self.acqua_entry.get_text() or "0"
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        note_riga = bufferNoteRiga.get_text(bufferNoteRiga.get_start_iter(), bufferNoteRiga.get_end_iter()) or ""

        model = self.righe_pesata_treeview.get_model()
        if self.editRiga:
            riga = self.editRiga
            riga.numero = self.editRiga.numero
        else:
            riga = RigaInfoPeso()
            riga.numero =len(model)+1

#        riga.id_testata_info_peso =
        riga.id_tipo_trattamento = findIdFromCombobox(self.id_tipo_trattamento_customcombobox.combobox)
        riga.data_registrazione = stringToDate(data_pesata)
        riga.note = note_riga
        riga.peso = Decimal(peso)
        riga.massa_grassa = Decimal(mgrassa)
        riga.massa_magra_e_acqua = Decimal(mmagraeacqua)
        riga.acqua = Decimal(acqua)
        if self.editRiga:
            self.rigaIter[0] = riga
#            self.rigaIter[1] = str(riga.numero)
            self.rigaIter[1] = dateToString(riga.data_registrazione)
            self.rigaIter[2] = riga.peso
            self.rigaIter[3] = riga.massa_grassa
            self.rigaIter[4] = riga.massa_magra_e_acqua
            self.rigaIter[5] = riga.acqua
            self.rigaIter[6] = riga.note
        else:
            model.append((riga,
                        dateToString(data_pesata),
                        str(peso) or "",
                        str(" differenza"),
                        str(mgrassa) or "",
                        str(mmagraeacqua) or "",
                        str(acqua) or "",
                        str("TIPO"),
                        str(note_riga.replace("\n"," ")[0:100])
                        ))
        self.righe_pesata_treeview.set_model(model)
        self._clear()
        print "AGGIUNGI"

    def _clear(self):
        self.data_pesata_datewidget.set_text("")
        self.peso_pesata_entry.set_text("")
        self.massa_grassa_entry.set_text("")
        self.massa_magra_e_acqua_entry.set_text("")
        self.acqua_entry.set_text("")
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        bufferNoteRiga.set_text("")

    def on_elimina_pesata_button_clicked(self, button):
        print "ELIMINA"

    def on_righe_pesata_treeview_row_activated(self, treeview, path, column):
        print "APAPAPAPAAPAPAPAP"
        sel = self.righe_pesata_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model

        self.data_pesata_datewidget.set_text(self.rigaIter[2] or "")
        self.peso_pesata_entry.set_text(self.rigaIter[3] or "")
        bufferNoteRiga= self.note_riga_pesata_textview.get_buffer()
        bufferNoteRiga.set_text(self.rigaIter[8] or "")
        self.note_riga_pesata_textview.set_buffer(bufferNoteRiga)

        findComboboxRowFromStr(self.rigaIter[6] or "")

        self.editRiga = self.rigaIter[0]

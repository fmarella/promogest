# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.lib.utils import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget

from promogest.modules.CSA.dao.GasRefrigerante import GasRefrigerante
from promogest.modules.CSA.dao.TipoApparecchio import TipoApparecchio
from promogest.modules.CSA.dao.ArticoloCSA import ArticoloCSA


class CSANotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, root='csa_frame',
                                    path='CSA/gui/csa_notebook.glade',
                                    isModule=True)
        self.rowBackGround = None
        self.ana = mainnn
        self.dao_articolo_csa = None
        self.draw()

    def draw(self):
        fillComboboxGasRefrigerante(self.id_gas_refrigerante_csa_customcombobox.combobox)
        self.id_gas_refrigerante_csa_customcombobox.connect('clicked',
                                 id_gas_refrigerante_csa_customcombobox_clicked)

        fillComboboxTipoApparecchio(self.id_tipo_apparecchio_csa_customcombobox.combobox)
        self.id_tipo_apparecchio_csa_customcombobox.connect('clicked',
                                 id_tipo_apparecchio_csa_customcombobox_clicked)

        self._clear()

    def _clear(self):
        self.sigla_csa_entry.set_text("")
        self.id_gas_refrigerante_csa_customcombobox.combobox.set_active(-1)
        self.id_tipo_apparecchio_csa_customcombobox.combobox.set_active(-1)


    def csaSetDao(self, dao):
        """ Estensione del SetDao principale"""
        if not dao.id:
            self.dao_articolo_csa = ArticoloCSA()
        else:
            if dao.APCSA is None:
                dao.APCSA = ArticoloCSA()
            self.dao_articolo_csa = dao.APCSA

    def csa_refresh(self):
        if self.dao_articolo_csa:
            self.sigla_csa_entry.set_text(self.dao_articolo_csa.sigla or "")
            self.potenza_csa_entry.set_text(self.dao_articolo_csa.potenza or "")
            self.id_gas_refrigerante_csa_customcombobox.combobox.set_active(self.dao_articolo_csa.id_gas_refrigerante or -1)
            self.id_tipo_apparecchio_csa_customcombobox.combobox.set_active(self.dao_articolo_csa.id_tipo_apparecchio or -1)


    def csaSaveDao(self):
        self.dao_articolo_csa.sigla = self.sigla_csa_entry.get_text() or ''
        self.dao_articolo_csa.potenza = self.potenza_csa_entry.get_text() or ''
        self.dao_articolo_csa.id_gas_refrigerante = self.id_gas_refrigerante_csa_customcombobox.combobox.get_active()
        self.dao_articolo_csa.id_tipo_apparecchio = self.id_tipo_apparecchio_csa_customcombobox.combobox.get_active()
        return self.dao_articolo_csa

# Categoria trasporto

def fillComboboxTipoApparecchio(combobox, filter=False):
    """ Riempi combo degli stadi commessa """
    model = gtk.ListStore(object, int, str)
    stcom = TipoApparecchio().select(batchSize=None)
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

def fillComboboxGasRefrigerante(combobox, filter=False):
    """ Riempi combo degli stadi commessa """
    model = gtk.ListStore(object, int, str)
    stcom = GasRefrigerante().select(batchSize=None)
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

def id_gas_refrigerante_csa_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica categoria trasporto
    """
    def on_anagrafica_gas_refrigerante_csa_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxGasRefrigerante(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.CSA.ui.AnagraficaGasRefrigerante import AnagraficaGasRefrigerante
    anag = AnagraficaGasRefrigerante()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_gas_refrigerante_csa_destroyed)

def id_tipo_apparecchio_csa_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica tipo apparecchio
    """
    def on_anagrafica_tipo_apparecchio_csa_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxTipoApparecchio(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.CSA.ui.AnagraficaTipoApparecchio import AnagraficaTipoApparecchio
    anag = AnagraficaTipoApparecchio()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_tipo_apparecchio_csa_destroyed)

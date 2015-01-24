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

from promogest.modules.ADR.dao.CategoriaTrasporto import CategoriaTrasporto
from promogest.modules.ADR.dao.CodiceClassificazione import CodiceClassificazione
from promogest.modules.ADR.dao.GruppoImballaggio import GruppoImballaggio
from promogest.modules.ADR.dao.ClassePericolo import ClassePericolo
from promogest.modules.ADR.dao.Galleria import Galleria
from promogest.modules.ADR.dao.ArticoloADR import ArticoloADR


class ADRNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, root='adr_frame',
                                    path='ADR/gui/adr_notebook.glade',
                                    isModule=True)
        self.rowBackGround = None
        self.ana = mainnn
        self.dao_articolo_adr = None
        self.draw()

    def draw(self):
        fillComboboxCategoriaTrasporto(self.id_categoria_trasporto_adr_customcombobox.combobox)
        self.id_categoria_trasporto_adr_customcombobox.connect('clicked',
                                 id_categoria_trasporto_customcombobox_clicked)

        fillComboboxCodiceClassificazione(self.id_codice_classificazione_adr_customcombobox.combobox)
        self.id_codice_classificazione_adr_customcombobox.connect('clicked',
                                 id_codice_classificazione_customcombobox_clicked)

        fillComboboxGruppoImballaggio(self.id_gruppo_imballaggio_adr_customcombobox.combobox)
        self.id_gruppo_imballaggio_adr_customcombobox.connect('clicked',
                                 id_gruppo_imballaggio_adr_customcombobox_clicked)

        fillComboboxClassePericolo(self.id_classe_pericolo_adr_customcombobox.combobox)
        self.id_classe_pericolo_adr_customcombobox.connect('clicked',
                                 id_classe_pericolo_adr_customcombobox_clicked)

        fillComboboxGalleria(self.id_galleria_adr_customcombobox.combobox)
        self.id_galleria_adr_customcombobox.connect('clicked',
                                 id_galleria_adr_customcombobox_clicked)

        self._clear()

    def _clear(self):
        self.numero_un_adr_entry.set_text("")
        self.id_gruppo_imballaggio_adr_customcombobox.combobox.set_active(-1)
        self.id_codice_classificazione_adr_customcombobox.combobox.set_active(-1)
        self.id_categoria_trasporto_adr_customcombobox.combobox.set_active(-1)
        self.id_classe_pericolo_adr_customcombobox.combobox.set_active(-1)
        self.id_galleria_adr_customcombobox.combobox.set_active(-1)

    def adrSetDao(self, dao):
        """ Estensione del SetDao principale"""
        if not dao.id:
            self.dao_articolo_adr = ArticoloADR()
        else:
            if dao.APADR is None:
                dao.APADR = ArticoloADR()
            self.dao_articolo_adr = dao.APADR

    def adr_refresh(self):
        if self.dao_articolo_adr:
            self.numero_un_adr_entry.set_text(self.dao_articolo_adr.numero_un or "")
            self.id_gruppo_imballaggio_adr_customcombobox.combobox.set_active(self.dao_articolo_adr.id_gruppo_imballaggio or -1)
            self.id_codice_classificazione_adr_customcombobox.combobox.set_active(self.dao_articolo_adr.id_codice_classificazione or -1)
            self.id_classe_pericolo_adr_customcombobox.combobox.set_active(self.dao_articolo_adr.id_classe or -1)
            self.id_galleria_adr_customcombobox.combobox.set_active(self.dao_articolo_adr.id_galleria or -1)
            self.id_categoria_trasporto_adr_customcombobox.combobox.set_active(self.dao_articolo_adr.id_categoria_trasporto or -1)

    def adrSaveDao(self):
        numero_un = self.numero_un_adr_entry.get_text() or ''
        if not numero_un:
            return None
        self.dao_articolo_adr.numero_un = numero_un
        self.dao_articolo_adr.id_gruppo_imballaggio = self.id_gruppo_imballaggio_adr_customcombobox.combobox.get_active()
        self.dao_articolo_adr.id_codice_classificazione = self.id_codice_classificazione_adr_customcombobox.combobox.get_active()
        self.dao_articolo_adr.id_classe = self.id_classe_pericolo_adr_customcombobox.combobox.get_active()
        self.dao_articolo_adr.id_galleria = self.id_galleria_adr_customcombobox.combobox.get_active()
        self.dao_articolo_adr.id_categoria_trasporto = self.id_categoria_trasporto_adr_customcombobox.combobox.get_active()
        return self.dao_articolo_adr

# Categoria trasporto

def fillComboboxCategoriaTrasporto(combobox, filter=False):
    """ Riempi combo degli stadi commessa """
    model = gtk.ListStore(object, int, str)
    stcom = CategoriaTrasporto().select(batchSize=None)
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


def id_categoria_trasporto_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica categoria trasporto
    """
    def on_anagrafica_categoria_trasporto_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategoriaTrasporto(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.ADR.ui.AnagraficaCategoriaTrasporto import AnagraficaCategoriaTrasporto
    anag = AnagraficaCategoriaTrasporto()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_categoria_trasporto_destroyed)

# Codice classificazione

def fillComboboxCodiceClassificazione(combobox, filter=False):
    """ Riempi combo dei codici di classificazione """
    model = gtk.ListStore(object, int, str)
    stcom = CodiceClassificazione().select(batchSize=None)
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

def id_codice_classificazione_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica dei codici di classificazione
    """
    def on_anagrafica_codice_classificazione_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCodiceClassificazione(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.ADR.ui.AnagraficaCodiceClassificazione import AnagraficaCodiceClassificazione
    anag = AnagraficaCodiceClassificazione()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_codice_classificazione_destroyed)

# Gruppo imballaggio

def fillComboboxGruppoImballaggio(combobox, filter=False):
    """ Riempi combo dei gruppi di imballaggio """
    model = gtk.ListStore(object, int, str)
    stcom = GruppoImballaggio().select(batchSize=None)
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

def id_gruppo_imballaggio_adr_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica dei gruppi di imballaggio
    """
    def on_anagrafica_gruppo_imballaggio_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxGruppoImballaggio(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.ADR.ui.AnagraficaGruppoImballaggio import AnagraficaGruppoImballaggio
    anag = AnagraficaGruppoImballaggio()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_gruppo_imballaggio_destroyed)

# Classe pericolosità

def fillComboboxClassePericolo(combobox, filter=False):
    """ Riempi combo delle classi di pericolosità """
    model = gtk.ListStore(object, int, str)
    stcom = ClassePericolo().select(batchSize=None)
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

def id_classe_pericolo_adr_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica delle classi di pericolosità
    """
    def on_anagrafica_classe_pericolo_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxClassePericolo(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.ADR.ui.AnagraficaClassePericolo import AnagraficaClassePericolo
    anag = AnagraficaClassePericolo()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_classe_pericolo_destroyed)

# Galleria

def fillComboboxGalleria(combobox, filter=False):
    """ Riempi combo galleria """
    model = gtk.ListStore(object, int, str)
    stcom = Galleria().select(batchSize=None)
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

def id_galleria_adr_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica galleria
    """
    def on_anagrafica_galleria_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxGalleria(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.ADR.ui.AnagraficaGalleria import AnagraficaGalleria
    anag = AnagraficaGalleria()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_galleria_destroyed)

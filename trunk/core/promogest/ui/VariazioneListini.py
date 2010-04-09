# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import gtk
from GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.ListinoArticolo import ListinoArticolo

from utils import *


class VariazioneListini(GladeWidget):

    def __init__(self, idArticolo=None, ultimoCosto = 0, nuovoCosto = 0):

        self._idArticolo = idArticolo
        self._ultimoCosto = ultimoCosto
        self._nuovoCosto = nuovoCosto
        self._percentualeIva = 0
        self._selectAll = False

        GladeWidget.__init__(self, 'variazione_listini_articoli_window')
        self.placeWindow(self.getTopLevel())


        treeview = self.listini_treeview
        model = gtk.ListStore(object, bool, str, str, str, str, str, str, str, str)
        treeview.set_model(model)

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.on_selected, treeview.get_model())
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Seleziona', renderer, active=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.sel_unsel_all)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Costo base', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricar. dettaglio', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Marg. dettaglio', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricar. ingrosso', rendererDx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Marg. ingrosso', rendererDx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(2)

        self.mantieni_prezzo_dettaglio_radiobutton.connect('toggled',
                                                           self.on_dettaglio_radiobutton_toggled)
        self.mantieni_ricarico_dettaglio_radiobutton.connect('toggled',
                                                             self.on_dettaglio_radiobutton_toggled)
        self.mantieni_margine_dettaglio_radiobutton.connect('toggled',
                                                            self.on_dettaglio_radiobutton_toggled)
        self.cambia_prezzo_dettaglio_radiobutton.connect('toggled',
                                                         self.on_dettaglio_radiobutton_toggled)
        self.mantieni_prezzo_ingrosso_radiobutton.connect('toggled',
                                                          self.on_ingrosso_radiobutton_toggled)
        self.mantieni_ricarico_ingrosso_radiobutton.connect('toggled',
                                                            self.on_ingrosso_radiobutton_toggled)
        self.mantieni_margine_ingrosso_radiobutton.connect('toggled',
                                                           self.on_ingrosso_radiobutton_toggled)
        self.cambia_prezzo_ingrosso_radiobutton.connect('toggled',
                                                        self.on_ingrosso_radiobutton_toggled)

        self.mantieni_ricarico_dettaglio_radiobutton.set_active(True)
        self.mantieni_ricarico_ingrosso_radiobutton.set_active(True)

        articolo = leggiArticolo(self._idArticolo)
        self._percentualeIva = articolo["percentualeAliquotaIva"]
        self.articolo_label.set_text(articolo["codice"] + "   " + articolo["denominazione"])
        if self._ultimoCosto is not None:
            uc = ('%14.' + Environment.conf.decimals + 'f') % self._ultimoCosto
            uci = ('%14.' + Environment.conf.decimals + 'f') % calcolaPrezzoIva(float(self._ultimoCosto),
                                                                                float(self._percentualeIva))
        else:
            uc = '-'
            uci = '-'
        self.ultimo_costo_no_iva_label.set_text(uc)
        self.ultimo_costo_iva_label.set_text(uci)
        if self._nuovoCosto is not None:
            nc = ('%14.' + Environment.conf.decimals + 'f') % self._nuovoCosto
            nci = ('%14.' + Environment.conf.decimals + 'f') % calcolaPrezzoIva(float(self._nuovoCosto),
                                                                                float(self._percentualeIva))
        else:
            nc = '-'
            nci = '-'
        self.nuovo_costo_no_iva_label.set_text(nc)
        self.nuovo_costo_iva_label.set_text(nci)

        self.refresh()


    def refresh(self):
        treeview = self.listini_treeview
        model = treeview.get_model()
        model.clear()

        liss = ListinoArticolo().select(orderBy='id_listino',
                                                    idListino=None,
                                                    idArticolo=self._idArticolo,
                                                    offset=None,
                                                    batchSize=None)


        for l in liss:
            ultCosto = ('%14.' + Environment.conf.decimals + 'f') % (l.ultimo_costo or 0)
            przDett = ('%14.' + Environment.conf.decimals + 'f') % (l.prezzo_dettaglio or 0)
            przIngr = ('%14.' + Environment.conf.decimals + 'f') % (l.prezzo_ingrosso or 0)
            ricDett = '%-6.3f' % calcolaRicarico(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_dettaglio or 0),
                                                 float(l.percentuale_iva or 0))
            margDett = '%-6.3f' % calcolaMargine(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_dettaglio or 0),
                                                 float(l.percentuale_iva or 0))
            ricIngr = '%-6.3f' % calcolaRicarico(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_ingrosso or 0))
            margIngr = '%-6.3f' % calcolaMargine(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_ingrosso or 0))

            model.append((l,
                          False,
                          (l.denominazione or ''),
                          ultCosto,
                          ricDett, margDett, przDett,
                          ricIngr, margIngr, przIngr))

        self.getTopLevel().show_all()


    def on_dettaglio_radiobutton_toggled(self, widget=None):
        if not(self.cambia_prezzo_dettaglio_radiobutton.get_active()):
            self.prezzo_dettaglio_entry.set_text('')
            self.prezzo_dettaglio_entry.set_sensitive(False)
        else:
            self.prezzo_dettaglio_entry.set_sensitive(True)
            self.prezzo_dettaglio_entry.grab_focus()


    def on_ingrosso_radiobutton_toggled(self, widget=None):
        if not(self.cambia_prezzo_ingrosso_radiobutton.get_active()):
            self.prezzo_ingrosso_entry.set_text('')
            self.prezzo_ingrosso_entry.set_sensitive(False)
        else:
            self.prezzo_ingrosso_entry.set_sensitive(True)
            self.prezzo_ingrosso_entry.grab_focus()


    def on_selected(self, cell, path, model):
        model[path][1] = not model[path][1]
        return


    def sel_unsel_all(self, widget):
        flg = not self._selectAll
        self._selectAll = flg
        model = self.listini_treeview.get_model()
        for r in model:
            iterator = model.get_iter(r.path)
            model.set_value(iterator, 1, flg)


    def on_aggiorna_button_clicked(self, button=None):
        if ((self.cambia_prezzo_dettaglio_radiobutton.get_active() and
             not(float(self.prezzo_dettaglio_entry.get_text()) > 0)) or
            (self.cambia_prezzo_ingrosso_radiobutton.get_active() and
             not(float(self.prezzo_ingrosso_entry.get_text()) > 0))):
            msg = 'Attenzione! Almeno uno dei prezzi e\' stato impostato a 0.\n Continuare ?'
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response != gtk.RESPONSE_YES:
                return

        nuovoCosto = self._nuovoCosto
        vecchioCosto = 0
        model = self.listini_treeview.get_model()
        for r in model:
            if r[1]:
                idListino = r[0].id_listino
                daoListinoArticolo = ListinoArticolo().select(idListino=r[0].id_listino,
                                                idArticolo= self._idArticolo,
                                                batchSize=None, orderBy="id_listino")[0]
                vecchioCosto = daoListinoArticolo.ultimo_costo
                if nuovoCosto is not None:
                    daoListinoArticolo.ultimo_costo = nuovoCosto
                else:
                    nuovoCosto = vecchioCosto
                daoListinoArticolo.data_listino_articolo = None
                daoListinoArticolo.listino_attuale = True
                if self.mantieni_ricarico_dettaglio_radiobutton.get_active():
                    ricarico = calcolaRicarico(float(vecchioCosto),
                                               float(daoListinoArticolo.prezzo_dettaglio),
                                               float(self._percentualeIva))
                    daoListinoArticolo.prezzo_dettaglio = calcolaListinoDaRicarico(float(nuovoCosto),
                                                                                  float(ricarico),
                                                                                  float(self._percentualeIva))
                elif self.mantieni_margine_dettaglio_radiobutton.get_active():
                    margine = calcolaMargine(float(vecchioCosto),
                                             float(daoListinoArticolo.prezzo_dettaglio),
                                             float(self._percentualeIva))
                    daoListinoArticolo.prezzo_dettaglio = calcolaListinoDaMargine(float(daoListinoArticolo.ultimo_costo),
                                                                                  float(margine),
                                                                                  float(self._percentualeIva))
                elif self.cambia_prezzo_dettaglio_radiobutton.get_active():
                    daoListinoArticolo.prezzo_dettaglio = float(self.prezzo_dettaglio_entry.get_text())

                if self.mantieni_ricarico_ingrosso_radiobutton.get_active():
                    ricarico = calcolaRicarico(float(vecchioCosto),
                                               float(daoListinoArticolo.prezzo_ingrosso))
                    daoListinoArticolo.prezzo_ingrosso = calcolaListinoDaRicarico(float(nuovoCosto),
                                                                                  float(ricarico))
                elif self.mantieni_margine_ingrosso_radiobutton.get_active():
                    margine = calcolaMargine(float(vecchioCosto),
                                             float(daoListinoArticolo.prezzo_ingrosso))
                    daoListinoArticolo.prezzo_ingrosso = calcolaListinoDaMargine(float(daoListinoArticolo.ultimo_costo),
                                                                                 float(margine))
                elif self.cambia_prezzo_ingrosso_radiobutton.get_active():
                    daoListinoArticolo.prezzo_ingrosso = float(self.prezzo_ingrosso_entry.get_text())
                daoListinoArticolo.persist()

        self.refresh()


    def on_listini_treeview_row_activated(self, treeview, path, column):
        sel = self.listini_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        riga = model[iterator]

        returnWindow = self.getTopLevel()
        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(self._idArticolo, riga[0].id_listino)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, None, self.refresh)

        model = anag.anagrafica_filter_treeview.get_model()
        column = anag.anagrafica_filter_treeview.get_column(0)
        row = model[0]
        anag.anagrafica_filter_treeview.set_cursor(row.path, column, False)
        anag.on_record_edit_activate(anag.record_edit_button)


    def on_inserimento_button_clicked(self, button=None):
        returnWindow = self.getTopLevel()
        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(self._idArticolo)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, None, self.refresh)

        anag.on_record_new_activate(anag.record_edit_button)
        if self._nuovoCosto is not None:
            anag.editElement.ultimo_costo_entry.set_text(Environment.conf.number_format % self._nuovoCosto)
            anag.editElement.aggiornaCostoIvato()


    def on_variazione_listini_articoli_window_close(self, widget, event=None):
        self.destroy()
        return None

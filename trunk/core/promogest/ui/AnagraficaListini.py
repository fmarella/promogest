# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from AnagraficaComplessa import Anagrafica
from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest import Environment
from promogest.dao.Listino import Listino
from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
from promogest.dao.ListinoMagazzino import ListinoMagazzino
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.ui.AnagraficaVariazioniListini import AnagraficaVariazioniListini
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaListini(Anagrafica):
    """ Anagrafica listini """

    def __init__(self, denominazione=None, aziendaStr=None):
        self._denominazione = denominazione
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica listini',
                            recordMenuLabel='_Listini',
                            filterElement=AnagraficaListiniFilter(self),
                            htmlHandler=AnagraficaListiniHtml(self),
                            reportHandler=AnagraficaListiniReport(self),
                            editElement=AnagraficaListiniEdit(self),
                            aziendaStr=aziendaStr)
        self.duplica_button.set_sensitive(True)
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)

    def duplicate(self, dao):
        """ Duplica le informazioni relative ad un documento scelto su uno nuovo
        """
        if dao is None:
            return

        from DuplicazioneListino import DuplicazioneListino
        anag = DuplicazioneListino(dao, self)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.getTopLevel())
        anagWindow.show_all()

    def on_record_delete_activate(self, widget):
        dao = self.filter.getSelectedDao()
        tdoc = ListinoArticolo().select(idListino=dao.id, batchSize=None)
        if tdoc:
            messageWarning(msg=_("<big><b>Impossibile rimuovere il listino</b></big>\n\nAlcuni articoli compongono questo listino."))
        else:
            Anagrafica.on_record_delete_activate(self, widget)

class AnagraficaListiniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei listini """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_filter_table',
                                  gladeFile='_ricerca_semplice_listini.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self, cplx=False):
        # Colonne della Treeview per il filtro
        if self._anagrafica._denominazione:
            self.denominazione_filter_entry.set_text(self._anagrafica._denominazione)
        self.refresh()
        if self._anagrafica._denominazione:
            self._anagrafica.anagrafica_filter_treeview.grab_focus()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.visibile_filter_check.set_active(False)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        visibili = self.visibile_filter_check.get_active()
        if visibili:
            visibili = None
        else:
            visibili = True

        def filterCountClosure():
            return Listino().count(denominazione=denominazione,
                                   visibili=visibili)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()
        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Listino().select(denominazione=denominazione,
                                                visibili=visibili,
                                                orderBy=self.orderBy,
                                                offset=offset,
                                                batchSize=batchSize)
        self._filterClosure = filterClosure
        liss = self.runFilter()
        self.filter_listore.clear()
        for l in liss:
            self.filter_listore.append((l,
                                        (l.denominazione or ''),
                                        (l.descrizione or ''),
                                        dateToString(l.data_listino)))


class AnagraficaListiniHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'listino',
                                'Listino')


class AnagraficaListiniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  defaultFileName='listini',
                                  htmlTemplate='listini',
                                  sxwTemplate='listini')


class AnagraficaListiniEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei listini """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_detail_table',
                                  'Dati listino',
                                  gladeFile='_anagrafica_listini_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry
        add_image =self.add_image.get_stock()
        self.addpix = self.add_image.render_icon(add_image[0],add_image[1], None)
        remove_image =self.remove_image.get_stock()
        self.removepix = self.remove_image.render_icon(remove_image[0],remove_image[1], None)

    def draw(self, cplx=False):
        #Elenco categorie
        fillComboboxCategorieClienti(self.id_categoria_cliente_customcombobox.combobox)
        self.id_categoria_cliente_customcombobox.connect('clicked',
                    on_id_categoria_cliente_customcombobox_clicked)
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                    on_id_magazzino_customcombobox_clicked)
        fillComboboxListini(self.id_listino_customcombobox.combobox)
        self.id_listino_customcombobox.connect('clicked',
                    on_id_listino_customcombobox_clicked)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Listino()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Listino().select(id=dao.id)[0]
        self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.descrizione_entry.set_text(self.dao.descrizione or '')
        self.data_listino_entry.set_text(dateToString(self.dao.data_listino))
        self.visible_check.set_active(self.dao.visible or True)
        self._refreshCategorieClienti()
        self._refreshMagazzini()
        self._refreshListiniComplessi()

    def _refreshCategorieClienti(self):
        self.id_categoria_cliente_customcombobox.combobox.set_active(-1)
        model = self.categorie_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        categorie = self.dao.categorieCliente
        for c in categorie:
            model.append((c.id_categoria_cliente, c.categoria_cliente, None, None))

    def _refreshMagazzini(self):
        self.id_magazzino_customcombobox.combobox.set_active(-1)
        model = self.magazzini_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        magazzini = self.dao.magazzini
        for m in magazzini:
            model.append((m.id_magazzino, m.magazzino, None, None))

    def _refreshListiniComplessi(self):
        self.id_listino_customcombobox.combobox.set_active(-1)
        model = self.listino_complesso_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        listini = self.dao.listiniComplessi
        for m in listini:
            model.append((m.id_listino, m.listino_denominazione, None, None))

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.descrizione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.descrizione_entry)

        if (self.data_listino_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.data_listino_entry)
        # ATTENZIONE: incremento ottenuto richiamando esplicitamente la sequence, in quanto id non e' PK
        #             della tabella listino

        #daoEsistente = Listino().select(denominazioneEM=self.denominazione_entry.get_text(),
                                        #dataListino = stringToDateTime(self.data_listino_entry.get_text()))
        #if daoEsistente:
            #messageInfo(msg="""ATTENZIONE!!
#Una listino con lo stesso nome e data esiste già
#Verrà aggiornato il precedente.""")
            #del self.dao
            #self.dao = daoEsistente[0]

        if Environment.tipo_eng !="sqlite" and not self.dao.id:
            listino_sequence = Sequence("listino_id_seq", schema=Environment.params['schema'])
            self.dao.id = Environment.params['session'].connection().execute(listino_sequence)
        if Environment.tipo_eng =="sqlite" and not self.dao.id:
            listini = Listino().select(orderBy=Listino.id, batchSize=None)
            if not listini:
                self.dao.id = 1
            else:
                self.dao.id = max([p.id for p in listini]) +1
        self.dao.denominazione = self.denominazione_entry.get_text()
        listinoAtt = Listino().select(denominazione=self.dao.denominazione)
        if not listinoAtt:
            self.dao.listino_attuale = True
        else:
            for l in listinoAtt:
                l.listino_attuale = False
                l.persist()
            self.dao.listino_attuale = True

        self.dao.descrizione = self.descrizione_entry.get_text()
        self.dao.data_listino = stringToDate(self.data_listino_entry.get_text())
        self.dao.visible = self.visible_check.get_active()
        self.dao.persist()
        cleanListinoCategoriaCliente = ListinoCategoriaCliente()\
                                            .select(idListino=self.dao.id,
                                            batchSize=None)
        for lcc in cleanListinoCategoriaCliente:
            lcc.delete()
        for c in self.categorie_listore:
            if c[3] == 'deleted':
                pass
            else:
                daoListinoCategoriaCliente = ListinoCategoriaCliente()
                daoListinoCategoriaCliente.id_listino = self.dao.id
                daoListinoCategoriaCliente.id_categoria_cliente = c[0]
                daoListinoCategoriaCliente.persist()

        cleanMagazzini = ListinoMagazzino()\
                                            .select(idListino=self.dao.id,
                                            batchSize=None)
        for mag in cleanMagazzini:
            mag.delete()
        for m in self.magazzino_listore:
            if m[3] != 'deleted':
                daoListinoMagazzino = ListinoMagazzino()
                daoListinoMagazzino.id_listino = self.dao.id
                daoListinoMagazzino.id_magazzino = m[0]
                daoListinoMagazzino.persist()

        cleanListini = ListinoComplessoListino().select(idListinoComplesso=self.dao.id,
                                                        batchSize=None)
        #print "CLEAN LISTINI", cleanListini
        for lis in cleanListini:
            Environment.session.delete(lis)
        Environment.session.commit()
        for l in self.listino_complesso_listore:
            if l[3] != 'deleted':
                daoListinoComplessoListino = ListinoComplessoListino()
                daoListinoComplessoListino.id_listino_complesso = self.dao.id
                daoListinoComplessoListino.id_listino = l[0]
                daoListinoComplessoListino.persist()

        #self.dao.persist()

        self._refreshCategorieClienti()
        self._refreshMagazzini()
        self._refreshListiniComplessi()

    def on_add_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            categoria = findStrFromCombobox(self.id_categoria_cliente_customcombobox.combobox, 2)
            for c in self.categorie_listore:
                if c[0] == id:
                    return
            self.categorie_listore.append((id, categoria, self.addpix, 'added'))
        self.categorie_treeview.get_selection().unselect_all()

    def on_add_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id:
            magazzino = findStrFromCombobox(self.id_magazzino_customcombobox.combobox, 2)
            for m in self.magazzino_listore:
                if m[0] == id:
                    return
            self.magazzino_listore.append((id, magazzino, self.addpix, 'added'))
        self.magazzini_treeview.get_selection().unselect_all()

    def on_add_row_listino_complesso_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        if id:
            listino = findStrFromCombobox(self.id_listino_customcombobox.combobox, 2)
            for m in self.listino_complesso_listore:
                if m[0] == id:
                    return
            self.listino_complesso_listore.append((id, listino, self.addpix, 'added'))
        self.listino_complesso_treeview.get_selection().unselect_all()

    def on_delete_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id:
            for c in self.categorie_listore:
                if c[0] == id:
                    if c[2] is None:
                        c[2] = self.removepix
                        c[3] = 'deleted'
                    else:
                        self.categorie_listore.remove(c.iter)
        self.categorie_treeview.get_selection().unselect_all()

    def on_delete_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id:
            for m in self.magazzino_listore:
                if m[0] == id:
                    if m[2] is None:
                        m[2] = self.removepix
                        m[3] = 'deleted'
                    else:
                        self.magazzini_listore.remove(m.iter)
        self.magazzini_treeview.get_selection().unselect_all()

    def on_delete_row_listino_complesso_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        if id:
            for m in self.listino_complesso_listore:
                if m[0] == id:
                    if m[2] is None:
                        m[2] = self.removepix
                        m[3] = 'deleted'
                    else:
                        self.listino_complesso_listore.remove(m.iter)
        self.listino_complesso_treeview.get_selection().unselect_all()

    def on_undelete_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id:
            for c in self.categorie_listore:
                if c[0] == id:
                    if c[3] == 'deleted':
                        c[2] = None
                        c[3] = None
        self.categorie_treeview.get_selection().unselect_all()

    def on_undelete_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id:
            for m in self.magazzini_listore:
                if m[0] == id:
                    if m[3] == 'deleted':
                        m[2] = None
                        m[3] = None
        self.magazzini_treeview.get_selection().unselect_all()

    def on_undelete_row_listino_complesso_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        if id:
            for m in self.listino_complesso_listore:
                if m[0] == id:
                    if m[3] == 'deleted':
                        m[2] = None
                        m[3] = None
        self.listino_complesso_treeview.get_selection().unselect_all()

    def on_categorie_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idCategoriaCliente = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_categoria_cliente_customcombobox.combobox, idCategoriaCliente)
            status = model.get_value(iterator, 3)
            self.delete_row_categoria_button.set_sensitive(status != 'deleted')
            self.undelete_row_categoria_button.set_sensitive(status == 'deleted')

    def on_magazzini_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idMagazzino = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                                                         idMagazzino)
            status = model.get_value(iterator, 3)
            self.delete_row_magazzino_button.set_sensitive(status != 'deleted')
            self.undelete_row_magazzino_button.set_sensitive(status == 'deleted')

    def on_listino_complesso_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idListino = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_listino_customcombobox.combobox,
                                                             idListino)
            status = model.get_value(iterator, 3)
            self.delete_listino_button.set_sensitive(status != 'deleted')
            self.undelete_listino_button.set_sensitive(status == 'deleted')

    def on_listini_articoli_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire gli articoli occorre salvare il listino.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(idListino=self.dao.id)
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_variazioni_togglebutton_toggled(self, toggleButton):
        anag = AnagraficaVariazioniListini(idListino=self.dao.id)
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_check_pricelist_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter filtrare gli articoli occorre salvare il listino.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from CrossFilterPriceList import CrossFilterPriceList
        anag = CrossFilterPriceList(listino=self.dao)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

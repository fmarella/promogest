# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import gtk
import gobject
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, \
                            AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest.dao.TestataPrimaNota import TestataPrimaNota
from promogest.dao.RigaPrimaNota import RigaPrimaNota
from promogest.dao.Banca import Banca
from promogest.lib.relativedelta import relativedelta
from utils import *
from utilsCombobox import *


class AnagraficaPrimaNota(Anagrafica):
    """ Anagrafica Variazioni Listini """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Prima Nota Cassa',
                            recordMenuLabel='_Prima nota cassa',
                            filterElement=AnagraficaPrimaNotaFilter(self),
                            htmlHandler=AnagraficaPrimaNotaHtml(self),
                            reportHandler=AnagraficaPrimaNotaReport(self),
                            editElement=AnagraficaPrimaNotaEdit(self),
                            aziendaStr=aziendaStr)

class AnagraficaPrimaNotaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella prim nota cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_prima_nota_filter_table',
                          gladeFile='_anagrafica_primanota_elements.glade')
        self._widgetFirstFocus = self.numero_filter_entry


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Numero', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'numero'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Da Data', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_inizio'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('A Data', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_fine'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Saldo singolo', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str,str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.da_data_inizio_datetimewidget.set_text('')
        self.a_data_inizio_datetimewidget.set_text('')
        self.da_data_fine_datetimewidget.set_text('')
        self.a_data_fine_datetimewidget.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        numero = prepareFilterString(self.numero_filter_entry.get_text())
        da_data_inizio = stringToDateTime(emptyStringToNone(self.da_data_inizio_datetimewidget.get_text()))
        a_data_inizio = stringToDateTime(emptyStringToNone(self.a_data_inizio_datetimewidget.get_text()))
        da_data_fine = stringToDateTime(emptyStringToNone(self.da_data_fine_datetimewidget.get_text()))
        a_data_fine = stringToDateTime(emptyStringToNone(self.a_data_fine_datetimewidget.get_text()))

        def filterCountClosure():
            return TestataPrimaNota().count(numero=numero,
                                daDataInizio = da_data_inizio,
                                aDataInizio = a_data_inizio,
                                daDataFine = da_data_fine,
                                aDataFine = a_data_fine)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TestataPrimaNota().select(numero=numero,
                                     daDataInizio = da_data_inizio,
                                    aDataInizio = a_data_inizio,
                                    daDataFine = da_data_fine,
                                    aDataFine = a_data_fine,
                                        orderBy=self.orderBy,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self._treeViewModel.clear()
        valore = 0
        for i in valis:
            col = None
            if not i.data_fine:
                col = "green"
            valore += mN(i.totali["totale"]) or 0
            self._treeViewModel.append((i,col,
                                        (i.numero or ''),
                                        (dateToString(i.data_inizio) or ''),
                                        (dateToString(i.data_fine) or ''),
                                        (str(mN(i.totali["totale"])) or "0"),
                                        str(valore)))


class AnagraficaPrimaNotaHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'prima_nota',
                                'Dettaglio Prima Nota Cassa')


class AnagraficaPrimaNotaReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle Prime Note Cassa',
                                  defaultFileName='prima_nota',
                                  htmlTemplate='prima_nota',
                                  sxwTemplate='prima_nota')



class AnagraficaPrimaNotaEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle prima nota cassa """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_prima_nota_detail_vbox',
                                'Dati Prima nota cassa.',
                                gladeFile='_anagrafica_primanota_elements.glade')
        self._widgetFirstFocus = self.data_inserimento_datewidget
        self.anagrafica = anagrafica
        self.editRiga = False
        self.rotazione = setconf("rotazione_primanota","Primanota")
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
                                 on_id_banca_customcombobox_clicked)

#        self.id_banca_customcombobox.set_sensitive(False)

    def draw(self, cplx=False):
        treeview = self.riga_primanota_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Numero', renderer, text=1, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cassa Entrata', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cassa Uscita', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Banca Entrata', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Banca Uscita', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Rif.Banca', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Rif.Docu', renderer, text=9, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._rigaModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str,str, str, str, str, str, str, str,str)
        self.riga_primanota_treeview.set_model(self._rigaModel)
#        self.banca_viewport.set_property("visible",False)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            inizializzazione = TestataPrimaNota().select(daDataInizio=stringToDate("01/01/"+Environment.workingYear))
            # nn c'è una testata dall'inizio dell'anno ne creo una
            if not inizializzazione:
                print "CREO LA PRIMA PRIMA NOTA"
                a = TestataPrimaNota()
                a.numero = 1
                a.data_inizio = stringToDate("01/01/"+Environment.workingYear)
                a.note = " PRIMA NOTA AUTOMATICA"
                a.persist()
                self.dao = TestataPrimaNota().getRecord(id=a.id)
            else:
                #ce n'è una devo verificare se è chiusa
                ancoraaperta =TestataPrimaNota().select(datafinecheck=True)
                if len(ancoraaperta) >1:
                    print "ATTENZIONE CI SONO PIÙ PRIMA NOTA APERTE"
                    messageInfo(msg ="Attenzione ci sono più prime note aperte")
                elif len(ancoraaperta) ==1:
                    msg = """Attenzione! E' stata trovata una prima nota ancora aperta
Scegliendo NO verrà proposta quella precedente,
Scegliendo SI verrà chiusa la precedente ed aperta una nuova
"""
                    dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                    response = dialog.run()
                    dialog.destroy()
                    if response == gtk.RESPONSE_YES:
                        ancoraaperta[0].data_fine = datetime.datetime.now()
                        Environment.session.add(ancoraaperta[0])
                        Environment.session.commit()
                        self.dao = TestataPrimaNota()
                        self.dao.numero = ancoraaperta[0].numero+1
                        self.dao.data_inizio =ancoraaperta[0].data_fine
                        self.dao.note = "NUOVA"
                    else:
                        self.dao = ancoraaperta[0]
                elif len(ancoraaperta) <1:
                    ultimadatachiusa = TestataPrimaNota().ultimaNota()
                    ultimachiusa = TestataPrimaNota().select(datafine = ultimadatachiusa)
                    if ultimadatachiusa:
                        self.dao = TestataPrimaNota()
                        self.dao.numero = ultimachiusa[0].numero+1
                        self.dao.data_inizio = ultimadatachiusa
                        self.dao.note = "NUOVA PRIMA NOTA"
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataPrimaNota().getRecord(id=dao.id)
            print "ROTAZION", self.rotazione
#            ultimadatachiusa = TestataPrimaNota().ultimaNota()

        self._refresh()


    def on_entrata_cassa_radio_toggled(self, toggled):
        if self.entrata_cassa_radio.get_active():
            self.entrata_cassa_entry.set_sensitive(True)
            self.uscita_cassa_entry.set_sensitive(False)
            self.uscita_banca_entry.set_sensitive(False)
            self.entrata_banca_entry.set_sensitive(False)
            self.id_banca_customcombobox.hide()
        elif self.uscita_cassa_radio.get_active():
            self.uscita_cassa_entry.set_sensitive(True)
            self.uscita_banca_entry.set_sensitive(False)
            self.entrata_banca_entry.set_sensitive(False)
            self.entrata_cassa_entry.set_sensitive(False)
            self.id_banca_customcombobox.hide()
        elif self.uscita_banca_radio.get_active():
            self.uscita_banca_entry.set_sensitive(True)
            self.uscita_cassa_entry.set_sensitive(False)
            self.entrata_cassa_entry.set_sensitive(False)
            self.uscita_cassa_entry.set_sensitive(False)
            self.id_banca_customcombobox.show()
        elif self.entrata_banca_radio.get_active():
            self.entrata_banca_entry.set_sensitive(True)
            self.uscita_banca_entry.set_sensitive(False)
            self.uscita_cassa_entry.set_sensitive(False)
            self.entrata_cassa_entry.set_sensitive(False)
            self.id_banca_customcombobox.show()
        self.entrata_banca_entry.set_text("")
        self.uscita_banca_entry.set_text("")
        self.uscita_cassa_entry.set_text("")
        self.entrata_cassa_entry.set_text("")

    def on_riattiva_button_clicked(self, button):
        messageInfo(msg= "ATTENZIONE, SI sta modificando una nota già chiusa")
        self.riga_primanota_frame.set_sensitive(True)

    def on_forza_chiusura_button_clicked(self, button):
        self.saveDao(chiusura=True)


    def _refresh(self):
        self.id_banca_customcombobox.hide()
        self.numero_label.set_text(str(self.dao.numero) or "")
        self.note_entry.set_text(self.dao.note or "")
        self.data_inizio_label.set_text(dateToString(self.dao.data_inizio) or "")
        self.data_fine_label.set_text(dateToString(self.dao.data_fine) or "")
        if self.dao.data_fine:
            self.riga_primanota_frame.set_sensitive(False)
            self.riattiva_button.set_sensitive(True)
        else:
            self.riattiva_button.set_sensitive(False)

        model = self.riga_primanota_treeview.get_model()
        model.clear()
        cassa_entrata = ""
        cassa_uscita = ""
        banca_entrata = ""
        banca_uscita = ""
        riferimento = ""
        for r in self.dao.righeprimanota:
            if r.segno =="uscita" and r.tipo =="banca":
                banca_uscita = str(r.valore)
            elif r.segno =="uscita" and r.tipo =="cassa":
                cassa_uscita = str(r.valore)
            elif r.segno == "entrata" and r.tipo == "banca":
                banca_entrata = str(r.valore)
            elif r.segno =="entrata" and r.tipo =="cassa":
                cassa_entrata = str(r.valore)
            banca = ""
            if r.id_banca:
                banca = Banca().getRecord(id=r.id_banca).denominazione
            model.append((r, str(r.numero),
                        dateToString(r.data_registrazione),
                        r.denominazione,
                        str(mN(cassa_entrata)),
                        str(mN(cassa_uscita)) ,
                        str(mN(banca_entrata)),
                        str(mN(banca_uscita)) ,
                        str(banca) or "",
                        riferimento or ""))
            cassa_entrata = ""
            cassa_uscita = ""
            banca_entrata = ""
            banca_uscita = ""
        if self.dao.numero >1:
#            saldoPrecedente = TestataPrimaNota().select(numero=self.dao.numero-1)[0].totali["totale"]
            self.saldo_precedente_label.set_text(str(self.saldo()))
        self.calcolaTotali(model)

    def saldo(self):
        tutte = TestataPrimaNota().select(batchSize=None)
        saldo_precedente = 0
        for t in tutte:
            if t.numero < self.dao.numero:
                saldo_precedente += t.totali["totale"]
        return mN(saldo_precedente)

    def clear(self):
        self.entrata_cassa_entry.set_text("")
        self.uscita_cassa_entry.set_text("")
        self.entrata_banca_entry.set_text("")
        self.uscita_banca_entry.set_text("")
        self.data_inserimento_datewidget.set_text("")
        self.denominazione_entry.set_text("")
        self.id_banca_customcombobox.combobox.set_active(-1)

    def on_aggiungi_button_clicked(self, button):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)
        if self.data_inserimento_datewidget.get_text() == "":
            obligatoryField(self.dialogTopLevel, self.data_inserimento_datewidget)
        model = self.riga_primanota_treeview.get_model()
        if self.editRiga:
            riga = self.editRiga
            riga.numero = self.editRiga.numero
        else:
            riga = RigaPrimaNota()
            riga.numero = len(model)+1
        data_registrazione = stringToDate(self.data_inserimento_datewidget.get_text())
        riga.data_registrazione = data_registrazione
        denominazione = self.denominazione_entry.get_text()
        riga.denominazione = denominazione
        cassa_entrata = self.entrata_cassa_entry.get_text()
        cassa_uscita = self.uscita_cassa_entry.get_text()
        banca_entrata = self.entrata_banca_entry.get_text()
        banca_uscita = self.uscita_banca_entry.get_text()
        riferimento = None
        if cassa_entrata:
            riga.valore = cassa_entrata
            riga.tipo = "cassa"
            riga.segno = "entrata"
        elif cassa_uscita:
            riga.valore = cassa_uscita
            riga.segno = "uscita"
            riga.tipo = "cassa"
        elif banca_entrata:
            riga.valore = banca_entrata
            riga.tipo = "banca"
            riga.segno = "entrata"
            if (findIdFromCombobox(self.id_banca_customcombobox.combobox) is None):
                obligatoryField(self.dialogTopLevel,
                        self.id_banca_customcombobox,
                        'Inserire un riferimento ad una banca !')
            riga.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        elif banca_uscita:
            riga.valore = banca_uscita
            riga.segno = "uscita"
            riga.tipo = "banca"
            if (findIdFromCombobox(self.id_banca_customcombobox.combobox) is None):
                obligatoryField(self.dialogTopLevel,
                        self.id_banca_customcombobox,
                        'Inserire un riferimento ad una banca !')
            riga.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        banca = ""
        if riga.id_banca:
            banca = Banca().getRecord(id=riga.id_banca).denominazione
        dati = (riga,str(len(model)+1),dateToString(data_registrazione) or "",
                        denominazione,
                        str(mN(cassa_entrata)),
                        str(mN(cassa_uscita)) ,
                        str(mN(banca_entrata)),
                        str(mN(banca_uscita)) ,
                        str(banca),
                        riferimento or "")
        if self.editRiga:
            self.rigaIter[0] = riga
            self.rigaIter[1] = str(riga.numero)
            self.rigaIter[2] = dateToString(riga.data_registrazione)
            self.rigaIter[3] = riga.denominazione
            self.rigaIter[4] = cassa_entrata or ""
            self.rigaIter[5] = cassa_uscita or ""
            self.rigaIter[6] = banca_entrata or ""
            self.rigaIter[7] = banca_uscita or ""
            self.rigaIter[8] = banca or ""
            self.rigaIter[9] = riferimento
        else:
            model.append(dati)
        self.riga_primanota_treeview.set_model(model)
        self.editRiga = None
        cassa_entrata = ""
        cassa_uscita = ""
        banca_entrata = ""
        banca_uscita = ""
        self.clear()
        self.calcolaTotali(model)

    def calcolaTotali(self,model):
        rghe = len(model)
        self.totale_righe_label.set_markup(c(str(rghe),"blue"))
        tot_ent_cassa = 0
        tot_ent_banca = 0
        tot_usc_cassa = 0
        tot_usc_banca = 0
        tot_banca = 0
        tot_cassa = 0
        tot_saldo = 0
        for a in model:
            tot_ent_cassa += float(a[4] or 0)
            self.totale_entrate_cassa_label.set_markup(c(str(mN(tot_ent_cassa)),"green"))
            tot_ent_banca += float(a[6] or 0)
            self.totale_entrate_banca_label.set_markup(c(str(mN(tot_ent_banca)),"green"))
            tot_usc_cassa += float(a[5] or 0)
            self.totale_uscite_cassa_label.set_markup(c(str(mN(tot_usc_cassa)),"red"))
            tot_usc_banca += float(a[7] or 0)
            self.totale_uscite_banca_label.set_markup(c(str(mN(tot_usc_banca)),"red"))

        tot_banca = tot_ent_banca - tot_usc_banca
        if tot_banca >0:
            self.totale_banca_label.set_markup(c(str(mN(tot_banca)),"green"))
        else:
            self.totale_banca_label.set_markup(c(str(mN(tot_banca)),"red"))
        tot_cassa = tot_ent_cassa - tot_usc_cassa
        if tot_cassa >0:
            self.totale_cassa_label.set_markup(c(str(mN(tot_cassa)),"green"))
        else:
            self.totale_cassa_label.set_markup(c(str(mN(tot_cassa)),"red"))
        tot_saldo = (tot_ent_banca+tot_ent_cassa)-(tot_usc_banca+tot_usc_cassa)

        if tot_saldo >0:
            self.totale_saldo_label.set_markup(b(c(str(mN(tot_saldo)),"green")))
        else:
            self.totale_saldo_label.set_markup(b(c(str(mN(tot_saldo)),"red")))
        self.saldo_label.set_markup(b(c(str(mN(self.saldo())+mN(tot_saldo)), "blue")))

    def on_rimuovi_button_clicked(self, button):
        """ Elimina la riga di prima nota selezioata"""
        dao = RigaPrimaNota().getRecord(id=self.editRiga.id)
        dao.delete()
        self._editModel.remove(self._editIterator)
        self.clear()
        self.calcolaTotali(self._editModel)

    def on_riga_primanota_treeview_row_activated(self,treeview, path, column):
        sel = self.riga_primanota_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model
        self.data_inserimento_datewidget.set_text(self.rigaIter[2])
        if self.rigaIter[4] != "0":
            self.entrata_cassa_radio.set_active(True)
        if self.rigaIter[5] != "0":
            self.uscita_cassa_radio.set_active(True)
        if self.rigaIter[6] != "0":
            self.entrata_banca_radio.set_active(True)
            findComboboxRowFromId(self.id_banca_customcombobox.com, self.rigaIter[0].id_banca)
        if self.rigaIter[7] != "0":
            self.uscita_banca_radio.set_active(True)
            findComboboxRowFromId(self.id_banca_customcombobox.combobox, self.rigaIter[0].id_banca)
        self.entrata_cassa_entry.set_text(self.rigaIter[4])
        self.uscita_cassa_entry.set_text(self.rigaIter[5])
        self.entrata_banca_entry.set_text(self.rigaIter[6])
        self.uscita_banca_entry.set_text(self.rigaIter[7])
        self.denominazione_entry.set_text(self.rigaIter[3])



        self.editRiga = self.rigaIter[0]

    def saveDao(self, chiusura=False):
#        self.dao.righeprimanota = []
        if "Primanota" in Environment.modulesList or \
            "pan" in Environment.modulesList:

            model = self.riga_primanota_treeview.get_model()
            righe_ = []
            for m in model:
                righe_.append(m[0])
            self.dao.note = self.note_entry.get_text()
            self.dao.righeprimanota = righe_
            if chiusura:
                self.dao.data_fine = datetime.datetime.now()
            self.dao.persist()
        else:
            fenceDialog()
        self.clear()

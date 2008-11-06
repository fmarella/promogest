# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
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

import time, gtk, gobject, gtkhtml2
import math, os, shutil, sys, tempfile, threading, os.path
from GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
import Login
from utils import *
import genshi
from genshi.template import TemplateLoader



class Ricerca(GladeWidget):
    """ Classe base per le ricerche di Promogest """

    def __init__(self, windowTitle, filterElement, htmlHandler=None):
        GladeWidget.__init__(self, 'ricerca_window')

        self.ricerca_window.set_title(windowTitle)

        self.dao = None

        self._setFilterElement(filterElement)
        self._setHtmlHandler(htmlHandler)
        self.htmlHandler = htmlHandler
        self.placeWindow(self.ricerca_window)
        self.filter.draw()


    def _setFilterElement(self, gladeWidget):
        self.bodyWidget = FilterWidget(owner=gladeWidget, filtersElement=gladeWidget)
        self.ricerca_viewport.add(self.bodyWidget.getTopLevel())
        self.bodyWidget.filter_body_label.set_no_show_all(True)
        self.bodyWidget.filter_body_label.set_property('visible', False)

        self.filter = self.bodyWidget.filtersElement
        self.filterTopLevel = self.filter.getTopLevel()
        self.filterTopLevel.set_sensitive(True)

        self.ricerca_filter_treeview = self.bodyWidget.resultsElement
        self._treeViewModel = None

        gladeWidget.build()

        accelGroup = gtk.AccelGroup()
        self.getTopLevel().add_accel_group(accelGroup)
        self.bodyWidget.filter_clear_button.add_accelerator('clicked', accelGroup, gtk.keysyms.Escape, 0, gtk.ACCEL_VISIBLE)
        self.bodyWidget.filter_search_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)

    def _setHtmlHandler(self, htmlHandler):
        if htmlHandler is not None:
            self.htmlHandler = htmlHandler
        else:
            self.ricerca_html.destroy()
            return

        # Initial setup
        document = gtkhtml2.Document()
        document.open_stream('text/html')
        document.write_stream('<html></html>')
        document.close_stream()

        self.ricerca_html.set_document(document)
        (width, height) = self.getTopLevel().get_size()
        self.ricerca_html.set_size_request(-1, height // 2)

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura della ricerca """
        Login.windowGroup.append(self.ricerca_window)
        self.ricerca_window.show_all()


    def on_filter_treeview_row_activated(self, widget, path, column):
        """ Gestisce la conferma della riga """
        self.ricerca_window.hide()
        if self.ricerca_window in Login.windowGroup:
            Login.windowGroup.remove(self.ricerca_window)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        sel = self.ricerca_filter_treeview.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            #print 'Ricerca.on_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        self.dao = model.get_value(iterator, 0)
        if self.htmlHandler is not None:
            self.htmlHandler.setDao(self.dao)

    def on_filter_treeview_selection_changed(self, selection):
        pass

    def insert(self, toggleButton, returnWindow):
        """ Richiama l'anagrafica per l'inserimento """
        raise NotImplementedError


    def on_inserimento_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        anagReturn = self.getTopLevel()
        self.insert(toggleButton, anagReturn)


    def on_confirm_button_clicked(self, widget):
        """ Riga confermata """
        self.ricerca_window.hide()
        if self.ricerca_window in Login.windowGroup:
            Login.windowGroup.remove(self.ricerca_window)


    def on_ricerca_window_close(self, widget, event=None):
        """ Uscita """

        if self.ricerca_window in Login.windowGroup:
            Login.windowGroup.remove(self.ricerca_window)
        self.destroy()
        return None


    def getHtmlWidget(self):
        return self.ricerca_html

class RicercaFilter(GladeWidget):
    """ Filtro per la ricerca """

    def __init__(self, ricerca, rootWidget,fileName=None):
        GladeWidget.__init__(self, rootWidget, fileName)
        self._ricerca = ricerca


    def build(self):
        """ reindirizza alcuni campi e metodi dal filterWidget """
        self.bodyWidget = self._ricerca.bodyWidget

        # mapping fields and methods from bodyWidget to this class
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy = None
        self.batchSize = self.bodyWidget.batchSize = 30
        self.offset = self.bodyWidget.offset = 0
        self.numRecords = self.bodyWidget.numRecords = 0
        self._filterClosure = None


    def draw(self):
        """
        Disegna i contenuti del filtro ricerca.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def clear(self):
        """ Ripulisci il filtro di ricerca e aggiorna la ricerca stessa """
        raise NotImplementedError


    def refresh(self):
        """ Aggiorna il filtro di ricerca in base ai parametri impostati """
        raise NotImplementedError


    def on_campo_filter_entry_key_press_event(self, widget, event):
        return self._ricerca.bodyWidget.on_filter_element_key_press_event(widget, event)


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma della riga """
        self._ricerca.on_filter_treeview_row_activated(treeview, path, column)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        self._ricerca.on_filter_treeview_cursor_changed(treeview)


    def runFilter(self, offset='__default__', batchSize='__default__',
                  progressCB=None, progressBatchSize=0):
        """ Recupera i dati """
        self.bodyWidget.orderBy = self.orderBy
        return self.bodyWidget.runFilter(offset=offset, batchSize=batchSize,
                                         progressCB=progressCB, progressBatchSize=progressBatchSize,
                                         filterClosure=self._filterClosure)


    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()
class RicercaHtml(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica """

    def __init__(self, ricerca, template, description):
        self._ricerca = ricerca
        self._gtkHtml = None # Will be filled later
        #self._htmlTemplate = os.path.join('templates', template + '.kid')
        self._htmlTemplate = os.path.join('templates')
        self.description = description
        self.defaultFileName = template

        self.dao = None

        self._slaTemplateObj = None


    def setDao(self, dao):
        """ Visualizza il Dao specificato """
        self.dao = dao

        self._refresh()

        if dao is not None and Environment.debugDao ==True:
            # FIXME: add some logging level check here
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            print ("\n\n=== DAO object dump ===\n\n"
                   + pp.pformat(dao.dictionary(complete=True))
                   + "\n\n")

    def refresh(self):
        """ Aggiorna la vista HTML """
        self._refresh()

    def _refresh(self):
        """ show the html page in the custom widget"""
        if self._gtkHtml is None:
            self._gtkHtml = self._ricerca.getHtmlWidget()
            # A bit of double buffering here
            self._gtkHtmlDocuments = (gtkhtml2.Document(),
                                      gtkhtml2.Document())
            for doc in self._gtkHtmlDocuments:
                doc.connect('request_url', self.on_html_request_url)
                doc.connect('link_clicked', self.on_html_link_clicked)

            self._currGtkHtmlDocument = 0
        if self.dao is None:
            html = '<html></html>'
        else:
            currDocument = (self._currGtkHtmlDocument + 1) % 2
            document = self._gtkHtmlDocuments[currDocument]

            #document =gtkhtml2.Document()
            document.open_stream('text/html')
            templates_dir = self._htmlTemplate
            #print "TEMPPP", templates_dir
            loader = TemplateLoader([templates_dir])
            tmpl = loader.load(self.defaultFileName+".html")
            stream = tmpl.generate(dao=self.dao)
            html = stream.render('xhtml')
            document.write_stream(html)
            document.close_stream()
            self._gtkHtml.set_document(document)
            #self._refresh(html)

    def on_html_request_url(self, document, url, stream):
        print url


    def on_html_link_clicked(self, document, link):
        print link


    def setObjects(self, objects):
        # FIXME: dummy function for API compatibility, refactoring(TM) needed!
        pass



    def pdf(self, operationName):
        operationNameUnderscored = operationName.replace(' ' , '_').lower()
        if os.path.exists(Environment.templatesDir + operationNameUnderscored + '.sla'):
            self._slaTemplate = Environment.templatesDir + operationNameUnderscored + '.sla'
        else:
            self._slaTemplate = Environment.templatesDir + self.defaultFileName + '.sla'
        """ Restituisce una stringa contenente il report in formato PDF """
        if self._slaTemplateObj is None:
            self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                           pdfFolder=self._anagrafica._folder,
                                           report=self._anagrafica._reportType)

        self.dao.resolveProperties()
        param = [self.dao.dictionary(complete=True)]
        multilinedirtywork(param)
        return self._slaTemplateObj.serialize(param)


    def cancelOperation(self):
        """ Cancel current operation """
        self._slaTemplateObj.cancelOperation()


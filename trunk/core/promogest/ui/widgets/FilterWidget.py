# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author  Andrea Argiolas   <andrea@promotux.it>

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
import math
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.lib.HtmlHandler import createHtmlObj, renderHTML
from promogest.ui.utils import setconf

class FilterWidget(GladeWidget):
    """ Base Class for filter part of windows/dialogs """

    def __init__(self, owner, filtersElement=None, resultsElement='grid'):
        GladeWidget.__init__(self, 'filter_vbox', fileName='_filter_elements.glade')
        self._owner = owner
        self.filtersElement = None
        self.resultsElement = None
        self.join = None
        self.orderBy = False
        self.flag = False
        self.batchSize = int(setconf("Numbers", "batch_size"))
        self.offset = 0
        self.numRecords = 0
        self._treeViewModel = None
        self._htmlTemplate = None
        self._firstFocusWidget = None

        self.filter_current_page_entry.set_alignment(xalign=1)
        self.filter_current_page_entry.connect('key_press_event', self.on_filter_current_page_entry_key_press_event)

        if filtersElement is None:
            self.filter_frame.set_no_show_all(True)
            self.filter_frame.set_property('visible', False)
        else:
            self.filter_frame.set_property('visible', True)
            self._setFiltersElement(filtersElement)

        if resultsElement is None:
            self.filter_scrolledwindow.set_no_show_all(True)
            self.filter_scrolledwindow.set_property('visible', False)
        else:
            self.filter_scrolledwindow.set_property('visible', True)
            self._setResultsElement(resultsElement)

        self.setFocus()


    def _setFiltersElement(self, filtersElement):
        """
        Put filter elements into frame
        """
        self.filtersElement = filtersElement
        self.filtersElementTopLevel = self.filtersElement.getTopLevel()
        self.filter_frame_vbox.pack_start(self.filtersElementTopLevel)
        self.filtersElementTopLevel.set_sensitive(True)


    def _setResultsElement(self, widgetType):
        """
        Put results element into scrolled view
        """
        #FIXME passing a string is not the best: look for another way
        if widgetType == 'grid':
            self.resultsElement = self.getTreeViewFilterResultsWidget()
            self.filter_scrolledwindow.add(self.resultsElement)
            self.resultsElement.set_sensitive(True)
        elif widgetType == 'html':
            self.resultsElement = self.getHtmlFilterResultsWidget()
            self.filter_scrolledwindow.add(self.resultsElement)
            self.resultsElement.set_sensitive(True)
        else:
            raise Exception('Results widget undefined !!')


    def draw(self):
        """
        Designs results layout
        """
        self._owner.draw()


    def on_filter_search_button_clicked(self, widget):
        """
        Search button response
        """
        self.gotoFirstPage()


    def on_filter_clear_button_clicked(self, widget):
        """
        Clear button response
        """
        self.clear()
        self.gotoFirstPage()


    def on_filter_element_key_press_event(self, widget, event):
        """
        Confirm or erase filter's parameters from keyboard
        """
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == 'Escape':
            self.on_filter_clear_button_clicked(widget)
            return True
        elif keyname == 'Return' or keyname == 'KP_Enter' or keyname == 'F3':
            self.on_filter_search_button_clicked(widget)
            return True
        else:
            return False


    def on_filter_first_button_clicked(self, widget):
        """
        First page button response
        """
        self.gotoFirstPage()


    def on_filter_prev_button_clicked(self, widget):
        """
        Previous page button response
        """
        self.gotoPrevPage()


    def on_filter_next_button_clicked(self, widget):
        """
        Next page button response
        """
        self.gotoNextPage()


    def on_filter_last_button_clicked(self, widget):
        """
        Last page button response
        """
        self.gotoLastPage()


    def on_filter_current_page_entry_key_press_event(self, widget, event):
        """
        Confirms page indication
        """
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            page = int(self.filter_current_page_entry.get_text())
            self.gotoPage(int(page))


    def gotoFirstPage(self):
        """
        First page
        """
        self.offset = 0
        self._refreshCurrentPage()


    def gotoPrevPage(self):
        """
        Previous page
        """
        if self.offset > 0:
            self.offset -= self.batchSize
        self._refreshCurrentPage()


    def gotoPage(self, pagina):
        """
        Page number calculation
        """
        if pagina <= math.ceil(float(self.numRecords) / float(self.batchSize)):
            self.offset = (pagina - 1) * self.batchSize
            self._refreshCurrentPage()


    def gotoNextPage(self):
        """
        Next page
        """
        if self.offset < (self.numRecords-self.batchSize):
            self.offset += self.batchSize
        self._refreshCurrentPage()


    def gotoLastPage(self):
        """
        Last page
        """
        self.offset = (self._getPageCount() - 1) * self.batchSize
        self._refreshCurrentPage()


    def _getCurrentPage(self):
        """
        Calculate current page
        """
        return self.offset / self.batchSize + 1

    def _getPageCount(self):
        """
        Calculate how much pages we have
        """
        #print self.numRecords
        return int(math.ceil(float(self.numRecords or 0)
                             / float(self.batchSize)) or '1')

    def _refreshCurrentPage(self):
        """
        Show current page number
        """
        currPage = self._getCurrentPage()
        self.filter_current_page_entry.set_text(str(currPage))
        self.refresh()

    def _refreshPageCount(self):
        """ Show total pages number
        """
        self.filter_total_pages_label.set_text(str(self._getPageCount()))

    def isLastPage(self):
        """ Returns if the current page is the last
        """
        return (self._getCurrentPage() == self._getPageCount())

    def _disablePageNumbers(self):
        self.filter_current_page_entry.set_text('')
        self.filter_current_page_entry.set_sensitive(False)
        self.filter_filter_total_count.set_text('')

    def _changeOrderBy(self, widget, fieldsString):
        """ Changes results order
        RITOCCO fatto per SA 0.6.3 ...ancora da approfondire
        """
        if sqlalchemy.__version__ > 0.6:
            if (self.orderBy is not None ) == (fieldsString[1] is not None):
                if self.flag == False:
                    self.orderBy = asc(fieldsString[1])
                    self.flag = True
                else:
                    self.orderBy = desc(fieldsString[1])
                    self.flag = False
            else:
                self.orderBy = fieldsString[1]
            if fieldsString[0] is not None:
                self.join = fieldsString[0]
        else:
            if self.orderBy == fieldsString[1]:
                if self.flag == False:
                    self.orderBy = asc(fieldsString[1])
                    self.flag = True
                else:
                    self.orderBy = desc(fieldsString[1])
                    self.flag = False
            else:
                self.orderBy = fieldsString[1]
            if fieldsString[0]:
                self.join = fieldsString[0]
        self.refresh()

    def setFocus(self, widget=None):
        """ Give focus to a widget
        """
        if widget is None:
            if hasattr(self, '_firstFocusWidget'):
                if self._firstFocusWidget is not None:
                    self._firstFocusWidget.grab_focus()
        else:
            widget.grab_focus()

    def clear(self):
        """ Clears filter's parameters
        """
        self._owner.clear()


    def refresh(self):
        """
        Refresh of results output
        """
        self._owner.orderBy = self.orderBy
        self._owner.batchSize = self.batchSize
        self._owner.offset = self.offset
        self._owner.join = self.join
        self._owner.refresh()


    def runFilter(self, offset='__default__', batchSize='__default__',
                  progressCB=None, progressBatchSize=0, filterClosure=None):
        """
        Run the filter with the current search parameters.  Return a
        list of Dao's limited by the given offset and batchSize.

        progressCB is a callback to be called every time
        progressBatchSize records have been fetched.

        This method should be used both internally (in the derived
        filter classes) and externally (i.e. by the report generator),
        in order to avoid code duplication.
        """
        if filterClosure is None:
            raise 'filterClosure not specificated !!!'
        if offset == '__default__':
            offset = self.offset
        if batchSize == '__default__':
            batchSize = self.batchSize

        objList =  filterClosure(offset, batchSize)

        #objList = Dao.select(cursor=cursor, daoClass=daoClass,
                             #progressCB=progressCB,
                             #progressBatchSize=progressBatchSize)

        return objList


    def countFilterResults(self, filterCountClosure=None):
        """
        Count the filter results with the current search parameters.

        This method should be used both internally (in the derived
        filter classes) and externally (i.e. by the report generator),
        in order to avoid code duplication.
        """
        if filterCountClosure is None:
            raise 'filterCountClosure not specificated !!!'
        return filterCountClosure()

    def genericButton(self):
        button = gtk.Button()
        return button

    def getTreeViewFilterResultsWidget(self):
        """ Return a treeview widget for filter results """

        treeview = gtk.TreeView()

        # some default settings
        treeview.set_headers_clickable(True)
        treeview.set_headers_visible(True)
        treeview.set_rules_hint(True)
        treeview.set_reorderable(False)
        treeview.set_enable_search(True)
        treeview.set_fixed_height_mode(False)
        treeview.set_hover_selection(False)
        treeview.set_hover_expand(False)
        treeview.connect('row_activated',
                         self.on_filter_treeview_row_activated)
        treeview.connect('cursor_changed',
                         self.on_filter_treeview_cursor_changed)
        selection = treeview.get_selection()
        selection.connect('changed', self.on_filter_treeview_selection_changed)
        return treeview


    def getHtmlFilterResultsWidget(self):
        """ Return a treeview widget for filter results """
        self.html = createHtmlObj(self)
        html = """<html><body></body></html>"""
        renderHTML(self.html,html)
        return self.html

    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Row activated event response
        """
        self._owner.on_filter_treeview_row_activated(treeview, path, column)

    def on_filter_treeview_cursor_changed(self, treeview):
        """ Row selection event response
        """
        self._owner.on_filter_treeview_cursor_changed(treeview)

    def on_filter_treeview_selection_changed(self, treeSelection):
        """
        Row selection event response
        """
#        print " PASSS"

        self._owner.on_filter_treeview_selection_changed(treeSelection)

    def on_filter_treeview_keypress_event(self, treeview, event):
        """
        Row key press event response
        """
        self._owner.on_filter_treeview_keypress_event(treeview, event)

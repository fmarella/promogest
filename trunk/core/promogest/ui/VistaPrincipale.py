# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

import gtk
import threading
import webbrowser
import urllib, urllib2
from GladeWidget import GladeWidget
from promogest import Environment
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.lib import feedparser
from utils import *
from promogest.ui.SendEmail import SendEmail
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML

class VistaPrincipale(GladeWidget):
    """
    Frame Principale di visualizzazione principale da costruire all'uscita di ogni anagrafica
    alla chiamata del metodo _refresh() con update dei promemoria in scadenza.
    """

    def __init__(self, mainWindow, azs=None):
#        GladeWidget.__init__(self, 'vista_principale_frame', fileName='_main_window_view_select.glade')
        self._loading=None
#        self.getfeedFromSite()

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura del frame """
        self.vista_principale_frame.show_all()

    def on_alarm_notify_treeview_cursor_changed(self,treeview):
        if self._loading:
            return
        self.cancel_alarm_button.set_sensitive(True)

    def on_promotux_button_clicked(self, button):
        url ="http://www.promotux.it"
        webbrowser.open_new_tab(url)

    def on_promogest_button_clicked(self, button):
        url ="http://www.promogest.me"
        webbrowser.open_new_tab(url)

    def on_numero_verde_button_clicked(self, button):
        sendemail = SendEmail()

    def on_rivenditore_button_clicked(self, button):
        url = Environment.rivenditoreUrl
        webbrowser.open_new_tab(url)

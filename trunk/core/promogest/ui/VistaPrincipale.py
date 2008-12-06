# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

import sys
import gtk
import gobject
#from kiwi.ui.objectlist import ObjectList, Column

from GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.lib import feedparser
from utils import *
import threading
import time
import genshi
from genshi.template import TemplateLoader
import webbrowser
from promogest.ui.SendEmail import SendEmail

templates_dir = "./templates/"
loader = TemplateLoader([templates_dir])
tmpl = loader.load('feed.html')


class VistaPrincipale(GladeWidget):
    """
    Frame Principale di visualizzazione principale da costruire all'uscita di ogni anagrafica
    alla chiamata del metodo _refresh() con update dei promemoria in scadenza.
    """

    def __init__(self, mainWindow, azs=None):
        GladeWidget.__init__(self, 'vista_principale_frame', fileName='_main_window_view_select.glade')
        #self.cancel_alarm_button.set_sensitive(False)
        #self.alarm_notify_treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self._loading=None

        self.draw()

    def draw(self):
        """
        disegna questo frame nella finestra principale
        """
        treeview = self.alarm_notify_treeview
        renderer = gtk.CellRendererText()
        rendererCtr = gtk.CellRendererText()
        rendererCtr.set_property('xalign', 0.5)

        column = gtk.TreeViewColumn('Data Scadenza', rendererCtr, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(120)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Oggetto', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Incaricato', rendererCtr, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Autore', rendererCtr, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Annotazioni', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        model = gtk.ListStore(object, str, str, str, str, str, str)
        treeview.set_model(model)

        if Environment.feed == "True":
            feedAll = Environment.feedAll
            feedToHtml = Environment.feedCache
            if feedAll == "":
                print "LEGGERO RITARDO NEL RECUPERO DEI FEED"
                """apro un thread per il recupero dei feed , su piattaforma a 32 bit
                tutto procede per il meglio tanne qualche warning, su 64 bit ci sono
                invece dei crash core dump dovuti ad una asyncronia tra il textbuffer e la texview che
                si ritrova il cursore cambiato senza capire perchè
                ho visto che con un join del thread che "ritarda" di un secondo e mezzo
                l'apertura della finestra di main tutto procede per il meglio"""
                thread = threading.Thread(target=self.getfeedFromSite)
                thread.start()
                thread.join(1.3)
                #print "AAAAAAAAAAA", sys.version_info
                #gobject.io_add_watch(self.getfeedFromSite)

                #time.sleep(20)
                #thread.stop()
                #gobject.idle_add(self.getfeedFromSite)
            elif feedAll and feedToHtml:
                self.renderPage(feedToHtml)
            else:
                self.getfeedFromSite()


        self.anno_lavoro_label.set_markup('<b>Anno di lavoro:   ' + Environment.workingYear + '</b>')
        self._refresh()

    def _refresh(self):
        """
        aggiorna la treeview con i promemoria che hanno uno stato "in_scadenza"
        """
        self._loading=True
        #clear the treeview
        model = self.alarm_notify_treeview.get_model()
        model.clear()
        #get the current alarms from db
        idAllarmi = promogest.dao.Promemoria.getScadenze()
        #fill again the model of the treeview (a gtk.ListStore)
        for idAllarme in idAllarmi:
            dao = Promemoria().getRecord(id=idAllarme)
            model.append((dao, dateToString(dao.data_scadenza),\
                                dao.oggetto, dao.descrizione,\
                                dao.incaricato, dao.autore, dao.annotazione))
        self._loading=False

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura del frame """
        self.vista_principale_frame.show_all()

    def on_cancel_alarm_button_clicked(self, button):
        """
        viene(vengono) eliminato(i) l'allarme(i) selezionato(i) nella treeview
        """
        count = self.alarm_notify_treeview.get_selection().count_selected_rows()
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Sono stati selezionati '+str(count)+' allarmi.\nConfermi l\'eliminazione?')

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            (model, indexes)= self.alarm_notify_treeview.get_selection().get_selected_rows()
            rows = []
            for index in indexes:
                iter = model.get_iter(index)
                dao = model.get(iter,0)[0]
                dao.delete()
                model.remove(iter)
        else:
            return

    def on_snooze_alarm_button_clicked(self, button):
            (model, indexes)= self.alarm_notify_treeview.get_selection().get_selected_rows()
            rows = []
            for index in indexes:
                iter = model.get_iter(index)
                dao = model.get(iter,0)[0]
                dao.giorni_preavviso += 1
                dao.in_scadenza = False
                dao.persist()
                model.remove(iter)

    def on_alarm_notify_treeview_cursor_changed(self,treeview):
        if self._loading:
            return
        self.cancel_alarm_button.set_sensitive(True)

    def renderPage(self, feedToHtml):
        """ show the html page in the custom widget"""
        stream = tmpl.generate(feed=feedToHtml)
        body = stream.render('xhtml')
        self.refresh(body)


    def refresh(self, body="<p></p>"):
        htmlview = self.html_main_window_custom_widget
        htmlview.connect("url-clicked", self.url_cb)
        htmlview.display_html(body)
        text_buffer = htmlview.get_buffer()
        mark = text_buffer.create_mark("start", text_buffer.get_start_iter(), False)
        htmlview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)


    def url_cb(self,view, url, type_):

        webbrowser.open_new_tab(url)
        #webbrowser.open(url)


    def getfeedFromSite(self):
        string = ""
        if Environment.feedAll == "":
            d = feedparser.parse("http://blog.promotux.it/category/promogest/feed")
        else:
            d = Environment.feedAll
        feedList = d['entries']
        feedToHtml = []
        for feed in feedList[:-3]:
            try:
                body = feed['content'][0]['value']
            except:
                body = feed["summary_detail"]['value']
            body = body.replace("<strong>","<span style='font-weight: bold'>")
            body = body.replace("</strong>","</span>")
            body = body.replace ( "<em>","<span style='font-style: italic'>")
            body = body.replace ( "</em>","</span>")
            feed = {
                "title" :feed['title'],
                "links": feed['links'][0]['href'],
                "body" : body,
                "updated" : feed['updated'][4:-14],
                "autore" : feed['author']
                }
            feedToHtml.append(feed)
        Environment.feedCache = feedToHtml
        self.renderPage(feedToHtml)

    def on_promotux_button_clicked(self, button):
        url ="http://www.promotux.it"
        webbrowser.open_new_tab(url)

    def on_promogest_button_clicked(self, button):
        url ="http://promogest.promotux.it"
        webbrowser.open_new_tab(url)

    def on_numero_verde_button_clicked(self, button):
        sendemail = SendEmail()

    def on_rivenditore_button_clicked(self, button):
        url = Environment.rivenditoreUrl
        webbrowser.open_new_tab(url)
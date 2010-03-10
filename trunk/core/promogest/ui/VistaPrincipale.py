# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

import gtk
import threading
import webbrowser

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
        GladeWidget.__init__(self, 'vista_principale_frame', fileName='_main_window_view_select.glade')
        #self.cancel_alarm_button.set_sensitive(False)
        #self.alarm_notify_treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self._loading=None
        self.html = createHtmlObj(self)
        self.feed_scrolled.add(self.html)
        html = """<html><body></body></html>"""
        renderHTML(self.html,html)
        self.draw()
#        self.getfeedFromSite()

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
                Environment.pg2log.debug("LEGGERO RITARDO NEL RECUPERO DEI FEED")

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
        #gobject.idle_add(self.checkUpdate)
        #thread = threading.Thread(target=self.checkUpdate)
        #thread.start()
        #thread.join(1.3)
        #time.sleep(2)
        #thread.stop()
        self.anno_lavoro_label.set_markup('<b>Anno di lavoro:   ' + Environment.workingYear + '</b>')
        self._refresh()

    def checkUpdate(self):
        self.rigasvn1 =0
        self.rigasvn2 =0

        command = 'svn info ~/pg2'
        stdin, stdouterr = os.popen4(command)
        print "INFO REPO LOCALE", stdouterr.read()
        for r in stdouterr.readlines():
            if "Revision" in str(r):
                self.rigasvn1=r
        commandremote = 'svn info http://svn.promotux.it/svn/promogest2/trunk/'
        stdin, stdouterr = os.popen4(commandremote)
        print "INFO REPO REMOTO",stdouterr.read()
        for line in stdouterr.readlines():
            if "Revision" in str(line):
                self.rigasvn2=r
        if self.rigasvn1 == self.rigasvn2:
            print "aggiornamento da fare"
            msg ="""ATTENZIONE!!
Andate nella sezione "opzioni" ed aggiornare l'applicazione.
E' presente una nuova versione disponibile"""
            dialog = gtk.MessageDialog(None,
                                    gtk.DIALOG_MODAL
                                    | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                    "pippo")
            response = dialog.run()
            #dialog.destroy()
            dialog.hide()
            #return False
        else:
            print "NON CI SONO NUOVE VERSIONI DEL PROMOGEST2 DISPONIBILI"
        #return False
        gobject.source_remove(self.__a)

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
            model.append((dao, dateToString(dao.data_scadenza),
                                dao.oggetto,
                                dao.descrizione,
                                dao.incaricato,
                                dao.autore,
                                dao.annotazione))
        self._loading=False
        #self.checkUpdate()
        #self.__a = gobject.idle_add(self.checkUpdate)


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
        pageData = {}
        pageData = {
                "file" :"feed.html",
                "feed" :feedToHtml,
                }
        html = renderTemplate(pageData)
        renderHTML(self.html,html)

    def getfeedFromSite(self):
        string = ""
        if Environment.feedAll == "":
            d = feedparser.parse("http://blog.promotux.it/category/promogest/feed")
        else:
            d = Environment.feedAll
        feedList = d['entries']
        feedToHtml = []
        for feed in feedList[:-1]:
            try:
                body = feed['content'][0]['value']
            except:
                body = feed["summary_detail"]['value']
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
#        from promogest.dao.TestataMovimento import TestataMovimento
#        daos = TestataMovimento().select(batchSize=1000)
#        if daos:
#            for d in daos:
#                print d
#    #            d.delete()
#                Environment.session.delete(d)
#            Environment.session.commit()
#            print "FINITA QUESTA TRANCE da 1000"
#        else:
#            print "FINITTIIIIIIWW"


#        print daos
        return
#        from promogest.dao.Inventario import Inventario
#        daos = Inventario().select(idMagazzino=3, batchSize=None)
#        for d in daos:
#            print d.id
#            d.delete()
#            Environment.session.delete(d)
#        Environment.session.commit()
#        url ="http://onebip.com/otms/?item=9855"
#        webbrowser.open_new_tab(url)

    def on_numero_verde_button_clicked(self, button):
        sendemail = SendEmail()

    def on_rivenditore_button_clicked(self, button):
        url = Environment.rivenditoreUrl
        webbrowser.open_new_tab(url)

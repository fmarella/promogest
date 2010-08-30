# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# License GNU Gplv2

import locale
import gtk
import hashlib
import os
import glob
try:
    import ho.pisa as pisa
except:
    print "ERRORE NELL'IMPORT DI PISA"
    import pisaLib.ho.pisa as pisa
import calendar
from promogest.lib.relativedelta import relativedelta
from datetime import datetime, timedelta
import time
import webbrowser
from  subprocess import *
from promogest import Environment
from GladeWidget import GladeWidget
from ElencoMagazzini import ElencoMagazzini
from ElencoListini import ElencoListini
from VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from promogest.lib import feedparser
from promogest.ui.PrintDialog import PrintDialogHandler
from utils import hasAction,fenceDialog, aggiorna, updateScadenzePromemoria,\
                     setconf, dateTimeToString, dateToString,last_day_of_month, date_range
from utilsCombobox import *
from ParametriFrame import ParametriFrame
from SetConf import SetConfUI
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.lib.HtmlViewer import HtmlViewer
from AnagraficaPrincipaleFrame import AnagrafichePrincipaliFrame
import Login
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
from promogest.dao.TestataDocumento import TestataDocumento
from ConfiguraWindow import ConfiguraWindow
#inizializzano il customwidget
from widgets.ArticoloSearchWidget import ArticoloSearchWidget
from widgets.ClienteSearchWidget import ClienteSearchWidget
from widgets.FornitoreSearchWidget import FornitoreSearchWidget
from widgets.PersonaGiuridicaSearchWidget import PersonaGiuridicaSearchWidget
if "GestioneNoleggio" in Environment.modulesList:
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
try:
    from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False



class Main(GladeWidget):

    def __init__(self,aziendaStr,anagrafiche_modules,parametri_modules,
                    anagrafiche_dirette_modules,frame_modules,permanent_frames):

        GladeWidget.__init__(self, 'main_window')
        self.main_window.set_title('*** PromoGest2 *** Azienda : '+aziendaStr+'  *** Utente : '+Environment.params['usernameLoggedList'][1]+' ***')
        self.aziendaStr = aziendaStr

        self.statusBarHandler()
        for filename in glob.glob(Environment.promogestDir+"/temp/"+'*.cache') :
            os.remove( filename )
        Login.windowGroup.append(self.getTopLevel())
        self.anagrafiche_modules = anagrafiche_modules
        self.parametri_modules = parametri_modules
        self.anagrafiche_dirette_modules=anagrafiche_dirette_modules
        self.frame_modules = frame_modules
        self.permanent_frames = permanent_frames
        self.currentFrame = None
        self.alarmFrame = None
        self.shop = Environment.shop
        self.creata = False
        if "SincroDB" not in Environment.modulesList:
            self.sincro_db.destroy()
        elif "SincroDB" in Environment.modulesList and Environment.conf.SincroDB.tipo =="client":
            self.master_sincro_db.destroy()
        elif "SincroDB" in Environment.modulesList and Environment.conf.SincroDB.tipo =="server":
            self.client_sincro_db.destroy()
        if Environment.tipodb =="postgresql":
            self.whatcant_button.destroy()
            self.test_promowear_button.destroy()
        self.create_allarmi_frame()
#        self.main_notebook.set_current_page(self.main_notebook.page_num(self.notifica_allarmi_frame))
#        self.main_notebook.set_current_page(0)
        if not WEBKIT:
            self.main_notebook.remove_page(2)
            self.main_notebook.remove_page(2)
        else:
            self.htmlPlanningWidget = createHtmlObj(self)
            self.planning_scrolled.add(self.htmlPlanningWidget)
            self.create_planning_frame()
            gobject.idle_add(self.create_news_frame)
        self.updates()

    def show(self):
        """ Visualizza la finestra """
        self.anno_lavoro_label.set_markup('<b>Anno di lavoro:   ' + Environment.workingYear + '</b>')
        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf)

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'anagrafica48x48.png')
        model.append([0, "Anagrafiche", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'magazzino48x48.png')
        model.append([1, "Magazzini", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'listino48x48.png')
        model.append([2, "Listini", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'documento48x48.png')
        model.append([3, "Documenti", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'parametri48x48.png')
        model.append([4, "Parametri", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'promemoria48x48.png')
        model.append([5, "Promemoria", pbuf])

        self.main_iconview.set_model(model)
        self.main_iconview.set_text_column(1)
        self.main_iconview.set_pixbuf_column(2)
        self.main_iconview.connect('selection-changed',
                                   self.on_main_iconview_select, model)

        self.main_iconview.set_columns(1)
        self.main_iconview.set_item_width(80)
        self.main_iconview.set_size_request(95, -1)

        # right vertical icon list  adding modules
        model_right = gtk.ListStore(int, str, gtk.gdk.Pixbuf, object)
        ind = 0
        for mod in self.anagrafiche_dirette_modules.keys():
            currModule = self.anagrafiche_dirette_modules[mod]
            if self.shop and currModule["module"].VIEW_TYPE[1] =="Vendita Dettaglio":
                anag = currModule["module"].getApplication()
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                #icon_view.unselect_all()
                return
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model_right.append(row)
            ind += 1
        for mod in self.frame_modules.keys():
            currModule = self.frame_modules[mod]
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row =(ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model_right.append(row)
            ind += 1

        self.main_iconview_right.set_model(model_right)
        self.main_iconview_right.set_text_column(1)
        self.main_iconview_right.set_pixbuf_column(2)
        self.main_iconview_right.connect('selection-changed',
                                   self.on_main_iconview_right_select, model_right)

        self.main_iconview_right.set_columns(1)
        self.main_iconview_right.set_item_width(80)
        self.main_iconview_right.set_size_request(95, -1)
        #load the alarm notification frame (AKA MainWindowFrame)
        if self.currentFrame is None:
#            self.main_hbox.remove(self.box_immagini_iniziali)
            self._refresh()
        self.placeWindow(self.main_window)
        self.main_window.show_all()
        self.on_button_refresh_clicked()

    def updates(self):
        """ Aggiornamenti e controlli da fare all'avvio del programma
        """
        #Aggiornamento scadenze promemoria
        if "Promemoria" in Environment.modulesList:
            updateScadenzePromemoria()

    def _refresh(self):
        """
        Update the window, setting the appropriate frame
        """
        self.main_iconview.unselect_all()
#        if self.currentFrame is None:
#        self.currentFrame = self.create_main_window_frame()
#        self.main_notebook = gtk.Notebook()
#        if len(self.permanent_frames) > 0:
#            self.main_notebook.append_page(self.currentFrame, 'Home')
#            for module in self.pemanent_frames.iteritems():
#                frame = module[1]['module'].getApplication().getTopLevel()
#                self.main_notebook.append_page(frame,module[1]['module'].VIEW_TYPE[1])
#            self.main_hbox.pack_start(self.main_notebook, fill=True, expand=True)
#        else:
#            self.main_notebook.set_current_page(1)
#        self.main_viewport.remove(self.main_label1)
#        self.main_viewport.add(self.currentFrame.notizie_frame)
#        self.nb_label1.set_text("NOTIZIE")
#        self.main_viewport2.remove(self.main_label2)
#        self.main_viewport2.add(self.currentFrame.notifica_allarmi_frame)
#        self.nb_label2.set_text("NOTIFICHE ALLARMI")
#            self.main_hbox.pack_start(self.currentFrame, fill=True, expand=True)
        self.main_hbox.show_all()

    def on_button_help_clicked(self, button):
        sendemail = SendEmail()

    def on_button_refresh_clicked(self, widget=None):
        if WEBKIT:
            self.create_planning_frame()
        if self.creata:
           self.main_notebook.remove_page(0)
           self.creata = False
        self._refresh()

    def on_main_iconview_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = model[i][0]

        if selection == 0:
            if not self.creata:
                self.main_notebook.prepend_page(self.create_anagrafiche_principali_frame())
                self.creata = True
            else:
                self.main_notebook.remove_page(0)
                self.main_notebook.prepend_page(self.create_anagrafiche_principali_frame())

#            self.currentFrame = self.create_anagrafiche_principali_frame()
        elif selection == 1:
            if not self.creata:
                self.main_notebook.prepend_page(self.create_magazzini_frame())
                self.creata = True
            else:
                self.main_notebook.remove_page(0)
                self.main_notebook.prepend_page(self.create_magazzini_frame())
#            self.currentFrame = self.create_magazzini_frame()
        elif selection == 2:
            if not self.creata:
                self.main_notebook.prepend_page(self.create_listini_frame())
                self.creata = True
            else:
                self.main_notebook.remove_page(0)
                self.main_notebook.prepend_page(self.create_listini_frame())
#            self.currentFrame = self.create_listini_frame()
        elif selection == 3:
            #self.currentFrame = self.create_registrazioni_frame()
            # Andrea
            # richiamo diretto dei documenti: evita di dover premere il
            # pulsante nel frame registrazioni
            if not hasAction(actionID=2):return
            from AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 4:
            if not self.creata:
                self.main_notebook.prepend_page(self.create_parametri_frame())
                self.creata = True
            else:
                self.main_notebook.remove_page(0)
                self.main_notebook.prepend_page(self.create_parametri_frame())
#            self.currentFrame = self.create_parametri_frame()
        elif selection == 5:
#            if "Promemoria" in Environment.modulesList:
            from AnagraficaPromemoria import AnagraficaPromemoria
            anag = AnagraficaPromemoria(self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
#                return
#            else:
#                fenceDialog()
        self.main_notebook.set_current_page(0)
        self._refresh()

    def on_main_iconview_right_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = model[i][0]
        module = model[i][3]

        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
            self.currentFrame.destroy()
            self.currentFrame = None
        if module.VIEW_TYPE[0] == 'anagrafica_diretta':
            anag = module.getApplication()
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif module.VIEW_TYPE[0] == 'frame':
            frame = module.getApplication()
            self.currentFrame = frame.getTopLevel()
##            icon_view.unselect_all()
        self._refresh()

    # INIZIO CREAZIONE FRAME

    def on_when_combo_changed(self, combo):
        if self.when_combo.get_active() == 0:
            Environment.view = "month"
        elif self.when_combo.get_active() == 1:
            Environment.view = "week"
        else:
            Environment.view = "day"
        self.create_planning_frame(currentData=Environment.currentData,view=Environment.view)

    def on_tutti_check_toggled(self, toggled):
        if self.tutti_check.get_active():
            self.ordini_check.set_active(True)
            self.preventivi_check.set_active(True)
            self.promemoria_ins_check.set_active(True)
            self.promemoria_scad_check.set_active(True)
        else:
            self.ordini_check.set_active(False)
            self.preventivi_check.set_active(False)
            self.promemoria_ins_check.set_active(False)
            self.promemoria_scad_check.set_active(False)
        self.create_planning_frame(currentData= Environment.currentData)

    def on_print_button_clicked(self, button):
        nomefile = "planner"+dateToString(Environment.currentData).replace("/","_")+"_"+Environment.view
        g = file(".temp.pdf", "wb")
        pdf = pisa.CreatePDF(str(self.hhttmmll),g)
        g.close()
        anag = PrintDialogHandler(self.main_window, nomefile)
        anagWindow = anag.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def onlyWeek(self, cale, workinDay, workinMonth, workinYearc, dayName):
        newlist=[]
        for ca in cale:
            for s in ca:
                if s.day == workinDay:
                    for c in ca:
                        q,z,x,v = c.toordinal(), c.day,c.weekday(),list(dayName)[c.weekday()]
                        newlist.append((q,z,x,v))
                    return newlist

    def on_check_toggled(self, button):
        self.create_planning_frame(currentData= Environment.currentData)

    def create_planning_frame(self,d=1,m=1,y=0, currentData=None,view=None):
        promeDict= {}
        prevesDict = {}
        prevesDictAT = {}
        ordesDict = {}
        ordesDictAT = {}
        if d==1 and m==1 and y ==0 and not currentData:
            currentData = datetime.date.today()
            m = currentData.month
            y = currentData.year
            d = currentData.day
        if currentData:
            m = currentData.month
            y = currentData.year
            d = currentData.day
        Environment.currentData = currentData
        if view:
            Environment.view = view
        else:
            try:
                view = Environment.view
            except:
                view = "month"
        weekDay = currentData.weekday()
        workinMonth = Environment.workinMonth= m
        workinYearc = Environment.workinYearc= y
        self.anno_calendar_spinbutton.set_value(int(workinYearc))
        workinDay = Environment.workinDay = d
        if os.name=="nt":
            dayName2 = calendar.day_name
            dayName = [ x.decode("iso8859-1") for x in dayName2]
        else:
            dayName = calendar.day_name
        monthName = calendar.month_name

        cale = calendar.Calendar().monthdatescalendar(workinYearc,workinMonth)
        first_day = relativedelta(days=-(workinDay-1))
        last_day = relativedelta(days=(last_day_of_month(workinYearc, workinMonth)-workinDay))
        currentLastDay = currentData+last_day
        currentFirstDay = currentData+first_day

        eventipromes_ins = []
        eventipromes_scad = []
        if self.promemoria_ins_check.get_active():
            promes = Promemoria().select(da_data_inserimento= currentFirstDay,
                                a_data_scadenza=currentLastDay, batchSize=None)
            for p in promes:
                eventipromes_ins.append((p.data_inserimento.toordinal(),{"id":p.id,
                                                    "short":p.oggetto,
                                                    "tipo":"data_inserimento",
                                                    "colore":"#F2859A"},p.data_inserimento.day))
        if self.promemoria_scad_check.get_active():
            promes = Promemoria().select(da_data_inserimento= currentFirstDay,
                                a_data_scadenza=currentLastDay, batchSize=None)
            for p in promes:
                eventipromes_scad.append((p.data_scadenza.toordinal(),{"id":p.id,
                                                    "short":p.oggetto,
                                                    "tipo":"data_scadenza",
                                                    "colore":"#148F14"},p.data_scadenza.day))
        eventipreves = []
        eventiprevesAT = []
        if self.preventivi_check.get_active():
            preves = TestataDocumento().select(daData= currentFirstDay,
                                aData=currentLastDay, batchSize=None,
                                idOperazione="Preventivo")
            for p in preves:
                eventipreves.append((p.data_documento.toordinal(),{"id":p.id,
                                                    "short":p.ragione_sociale_cliente,
                                                    "tipo":"data_documento",
                                                    "colore":"#6495ED"},p.data_documento.day))
                if "GestioneNoleggio" in Environment.modulesList:
                    arcTemp = TestataGestioneNoleggio().select(idTestataDocumento=p.id, batchSize=None)
                    for a in arcTemp:
                        startDate =a.data_inizio_noleggio
                        stopDate =a.data_fine_noleggio
                        dateList= date_range(startDate,stopDate)
                        for d in dateList:
                            eventiprevesAT.append((d.toordinal(),{"id":p.id,
                                            "short":p.ragione_sociale_cliente,
                                            "tipo":"data_documento",
                                            "colore":"#AFEEEE"},d.day))
        eventiordes = []
        eventiordesAT = []
        if self.ordini_check.get_active():
            ordes = TestataDocumento().select(daData= currentFirstDay,
                                aData=currentLastDay, batchSize=None,
                                idOperazione="Ordine da cliente")

            for p in ordes:
                eventiordes.append((p.data_documento.toordinal(),{
                                "id":p.id,
                                "short":p.ragione_sociale_cliente,
                                "tipo":"data_documento",
                                "colore":"#FFA500"},p.data_documento.day))
                if "GestioneNoleggio" in Environment.modulesList:
                    arcTemp = TestataGestioneNoleggio().select(idTestataDocumento=p.id, batchSize=None)
                    for a in arcTemp:
                        startDate =a.data_inizio_noleggio
                        stopDate =a.data_fine_noleggio
                        dateList= date_range(startDate,stopDate)
                        for d in dateList:
                            eventiordesAT.append((d.toordinal(),{"id":p.id,
                                            "short":p.ragione_sociale_cliente,
                                            "tipo":"data_documento",
                                            "colore":"red"},d.day))
        onlyWeek = self.onlyWeek(cale, workinDay, workinMonth, workinYearc,dayName)

        pageData = {"file": "planning.html",
                    "cale":cale,
                    "onlyWeek":onlyWeek,
                    "eventipromes_ins": eventipromes_ins,
                    "eventipromes_scad": eventipromes_scad,
                    "eventipreves":eventipreves,
                    "eventiprevesAT": eventiprevesAT,
                    "eventiordes":eventiordes,
                    "eventiordesAT": eventiordesAT,
                    "dayName" :dayName,
                    "monthName": monthName,
                    "workinDay":workinDay,
                    "weekDay":weekDay,
                    "workinMonth":workinMonth,
                    "workinYearc":workinYearc,
                    "view":view}
        self.hhttmmll = renderTemplate(pageData)
        renderHTML(self.htmlPlanningWidget,self.hhttmmll)


    def on_refresh_button_clicked(self, button):
        self.create_planning_frame(currentData= Environment.currentData)

    def on_corrente_calendar_button_clicked(self,button):
        self.create_planning_frame(d=1,m=1,y=0)

    def on_piugiorni_calendar_button_clicked(self, button):
        one_day = datetime.timedelta(days=1)
        tomorrow =  Environment.currentData+one_day
        self.create_planning_frame(currentData=tomorrow)

    def on_piumesi_calendar_button_clicked(self, button):
        if Environment.view =="week":
            one_week = relativedelta(weeks=1)
            nextmonth =  Environment.currentData+one_week
        else:
            one_month = relativedelta(months=1)
            nextmonth =  Environment.currentData+one_month
        self.create_planning_frame(currentData=nextmonth)

    def on_anno_calendar_spinbutton_change_value(self, spinbutton):
        if int(spinbutton.get_value()) != Environment.workinYearc:
            newYear = int(spinbutton.get_value()) - Environment.workinYearc
            one_year = relativedelta(years=newYear)
            nextyear =  Environment.currentData+one_year
            self.create_planning_frame(currentData=nextyear)

    def on_menogiorni_calendar_button_clicked(self, button):
        one_day = relativedelta(days=-1)
        tomorrow =  Environment.currentData+one_day
        self.create_planning_frame(currentData=tomorrow)

    def on_menomesi_calendar_button_clicked(self, button):
        if Environment.view =="week":
            one_week = relativedelta(weeks=-1)
            nextmonth =  Environment.currentData+one_week
        else:
            one_month = relativedelta(months=-1)
            nextmonth =  Environment.currentData+one_month
        self.create_planning_frame(currentData=nextmonth)

    def drawAllarmi(self):
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

    def on_alarm_notify_treeview_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        dao = model[path][0]
        a = AnagraficaPromemoria()
        a.on_record_edit_activate(a, dao=dao)

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
                dao.scaduto = True
                dao.completato = True
                dao.in_scadenza = False
                dao.persist()
                model.remove(iter)
        else:
            return

    def on_snooze_alarm_button_clicked(self, button):
            (model, indexes)= self.alarm_notify_treeview.get_selection().get_selected_rows()
            rows = []
            for index in indexes:
                iter = model.get_iter(index)
                dao = model.get(iter,0)[0]
                dao.giorni_preavviso += -1
                dao.in_scadenza = False
                dao.persist()
                model.remove(iter)

    def create_allarmi_frame(self):
        """ creiamo il tab degli allarmi"""
        self.drawAllarmi()
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

    def create_news_frame(self):
        """ CREIAMO IL TAB DELLE NEWS"""
        self.htmlwidget = createHtmlObj(self)
        self.feed_scrolled.add(self.htmlwidget)
        html = """<html><body></body></html>"""
        renderHTML(self.htmlwidget,html)
        if setconf("Feed", "feed"):
            feedAll = Environment.feedAll
            feedToHtml = Environment.feedCache
            if feedAll != "" and feedAll and feedToHtml:
                self.renderPage(feedToHtml)
            else:
                try:
                    gobject.idle_add(self.getfeedFromSite)
                except:
                    Environment.pg2log.debug("LEGGERO RITARDO NEL RECUPERO DEI FEED")

    def renderPage(self, feedToHtml):
        """ show the html page in the custom widget"""
        pageData = {
                "file" :"feed.html",
                "feed" :feedToHtml,
                }
        html = renderTemplate(pageData)
        renderHTML(self.htmlwidget,html)

    def getfeedFromSite(self):
        string = ""
        if Environment.feedAll == "":
            d = feedparser.parse("http://www.promotux.it/newsfeed")
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
                "updated" : feed['updated'][4:-13],
                "autore" : feed['author']
                }
            feedToHtml.append(feed)
        Environment.feedCache = feedToHtml
        self.renderPage(feedToHtml)



    def create_main_window_frame(self):
#        if self.currentFrame is not None:
#            self.main_hbox.remove(self.currentFrame)
        frame = VistaPrincipale(self, self.aziendaStr)
#        return frame.vista_principale_frame
        return frame

    def create_anagrafiche_principali_frame(self):
        if not hasAction(actionID=11):return
#        if self.currentFrame is not None:
#            self.main_hbox.remove(self.currentFrame)
        frame = AnagrafichePrincipaliFrame(self.main_window, self.aziendaStr, modules=self.anagrafiche_modules)
        return frame.getTopLevel()

    def create_magazzini_frame(self):
        if not hasAction(actionID=12):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = MagazziniFrame(self.main_window, self.aziendaStr)
        return frame.getTopLevel()

    def create_listini_frame(self):
        if not hasAction(actionID=9):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = ListiniFrame(self.main_window, self.aziendaStr)
        return frame.getTopLevel()

    def create_registrazioni_frame(self):
        if not hasAction(actionID=2):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = RegistrazioniFrame(self.main_window, self.aziendaStr)
        return frame.getTopLevel()

    def create_parametri_frame(self):
        if not hasAction(actionID=6):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = ParametriFrame(self.main_window, self.aziendaStr, modules=self.parametri_modules)
        return frame.getTopLevel()

    # FINE CREAZIONE FRAME

    def on_nuovo_articolo_button_clicked(self, widget):
        if not hasAction(actionID=8):return
        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_cliente_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_promemoria_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaPromemoria import AnagraficaPromemoria
        anag = AnagraficaPromemoria(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_contatto_button_clicked(self, widget):
        if not hasAction(actionID=11):return
        from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
        anag = AnagraficaContatti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_fattura_vendita_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura vendita")

    def on_nuovo_fattura_acquisto_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura acquisto")

    def on_nuovo_ddt_vendita_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT vendita")

    def on_nuovo_ddt_acquisto_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT acquisto")

    def on_nuovo_ddt_reso_da_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso da cliente")

    def on_nuovo_ddt_reso_a_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso a fornitore")

    def on_nota_di_credito_a_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito a cliente")

    def on_nota_di_credito_a_fornitore_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito da fornitore")

    def on_fattura_accompagnatoria_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura accompagnatoria")

    def on_nuovo_preventivo_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Preventivo")

    def on_nuovo_ordine_da_cliente_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Ordine da cliente")

    def on_nuovo_vendita_al_dettaglio_button_clicked(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Vendita dettaglio")

    def nuovoDocumento(self, kind):
        if not hasAction(actionID=2):return
        from AnagraficaDocumenti import AnagraficaDocumenti
        #from utils import findComboboxRowFromStr
        anag = AnagraficaDocumenti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()
        findComboboxRowFromStr(anag.editElement.id_operazione_combobox, kind, 1)
        anag.editElement.id_persona_giuridica_customcombobox.grab_focus()
        findComboboxRowFromStr(anag.editElement.id_persona_giuridica_customcombobox, "Altro", 1)

    def on_promotux_button_clicked(self, button):
        url ="http://www.promotux.it"
        webbrowser.open_new_tab(url)

    def on_promogest_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest"
        webbrowser.open_new_tab(url)

    def on_email_button_clicked(self, button):
        sendemail = SendEmail()

    def on_configurazione_menu_activate(self, widget):
        if not hasAction(actionID=14):return

        configuraWindow = ConfiguraWindow(self)
        configuraWindow = SetConfUI(self)
        showAnagrafica(self.getTopLevel(), configuraWindow)

    def on_dati_azienda_activate(self, widget):
        from AnagraficaAziende import AnagraficaAziende
        anag =AnagraficaAziende(self)
        showAnagrafica(self.getTopLevel(), anag)

    def on_importa_modulo_activate(self, widget):
        fileDialog = gtk.FileChooserDialog(title='Importazione modulo',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_OK,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        fltr = gtk.FileFilter()
        fltr.add_pattern('*.pg2')
        fltr.set_name('File Pg2 (*.pg2)')
        fileDialog.add_filter(fltr)
        fltr = gtk.FileFilter()
        fltr.add_pattern('*')
        fltr.set_name('Tutti i file')
        fileDialog.add_filter(fltr)

        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            f = open(filename)
            r = f.readline()
            al = f.readlines()
            for a in al:
                if "MODULES_NAME" in a:
                    n = a.split("=")[1].strip()[1:-1]
                    break
                else:
                    continue
            c = Environment.PRODOTTO.strip()
            v = Environment.VERSIONE.strip()
            p = hashlib.sha224(n+c+v).hexdigest()
            if p.strip()==r.strip():
                pa = os.path.join(Environment.conf.Moduli.cartella_moduli,n+"/"+"module.py")
                g = file(pa,"w")
                for a in al:
                    g.write(a)
                g.close()
                f.close()
                msg = "MODULO CORRETTAMENTE INSTALLATO, CHIUDERE L'APPLICAZIONE\nED AGGIUNGERE I PARAMETRI NECESSARI\n"
            else:
                msg ="ATTENZIONE, MODULO NON INSTALLATO, CORROTTO O NON CORRETTO, CONTATTARE L'ASSISTENZA"
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
                #self.path_file_entry.set_text(filename)
            fileDialog.destroy()

    def on_credits_menu_activate(self, widget):
        context_id =  self.pg2_statusbar.get_context_id("GENERICO")
        self.pg2_statusbar.push(context_id,"PROVIAMO")
        from promogest.dao.Setting import Setting
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        self.pg2_statusbar.push(context_id,"SECONDO")
        encoding = locale.getlocale()[1]
        utf8conv = lambda x : unicode(x, encoding).encode('utf8')
        licenseText = ''
        textBuffer = creditsDialog.svn_info_textview.get_buffer()
        textBuffer.set_text(licenseText)
        command = ' info ~/pg2'
        p = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        (stdin, stdouterr) = (p.stdin, p.stdout)
        for line in stdouterr.readlines():
            textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
        textBuffer.insert(textBuffer.get_end_iter(),"""I moduli installati sono :
            """)
#        self.pg2_statusbar.push(context_id,"TERZO")
        for line in Environment.modulesList:
            textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
        response = creditsDialog.credits_dialog.run()
        if response == gtk.RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_licenza_menu_activate(self, widget):
        licenzaDialog = GladeWidget('licenza_dialog', callbacks_proxy=self)
        licenzaDialog.getTopLevel().set_transient_for(self.getTopLevel())
        licenseText = ''
        try:
            lines = open('./LICENSE').readlines()
            for l in lines:
                licenseText += l
        except:
            licenseText = 'Lavori in corso ....'
            print 'License file not found (LICENSE).'
        textBuffer = licenzaDialog.licenza_textview.get_buffer()
        textBuffer.set_text(licenseText)
        licenzaDialog.licenza_textview.set_buffer(textBuffer)
        licenzaDialog.getTopLevel().show_all()
        response = licenzaDialog.licenza_dialog.run()
        if response == gtk.RESPONSE_OK:
            licenzaDialog.licenza_dialog.destroy()

    def on_manuale_online_activate(self, widget):
        url ="http://help.promotux.it"
        webbrowser.open_new_tab(url)

    def on_aggiorna_activate(self, widget):
        aggiorna(self)

    def on_Back_up_Database_activate(self, widget):
        """ Si prepara un file zip con il dump del DB """

        st= Environment.startdir()
        nameDump = "promoGest2_dump_"+self.aziendaStr+"_"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
        msgg = """Il "dump" del database verrà salvato in

%s
ed avrà il nome

%s.zip

ATTENZIONE!!!! la procedura potrebbe richiedere diversi minuti.""" %(st, nameDump)
        dialogg = gtk.MessageDialog(self.getTopLevel(),
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK,
                                msgg)
        dialogg.run()
        dialogg.destroy()
        #if response == gtk.RESPONSE_OK:
        st= Environment.startdir()

        stname = st+nameDump
        os.environ["PGPASSWORD"]=Environment.password

        retcode = call(["pg_dump",
                        "-h",Environment.host,
                        "-p",Environment.port,
                        "-U",Environment.user,
                        "-Z","7",
                        "-f",stname,
                        Environment.database])

        Environment.pg2log.info("STO EFFETTUANDO UN BACKUP DEL FILE %s" %stname)
        #print "YYYYYYYYYYYYYYYYYY", retcode
        if not retcode:
            #zfilename = nameDump +".zip"
            #zout = zipfile.ZipFile(str(stname) +".zip", "w")
            #zout.write(stname,zfilename,zipfile.ZIP_DEFLATED)
            #zout.close()
            Environment.pg2log.info("DUMP EFFETTUATO CON SUCCESSO")
            #os.remove(stname)
        else:
            Environment.pg2log.info("ATTENZIONE DUMP NON RIUSCITO")

    def on_seriale_menu_activate(self, widget):
        try:
            fileName = Environment.conf.guiDir + 'logo_promogest.png'
            f = open(fileName,'rb')
            content = f.read()
            f.close()
            msg = 'Codice installazione:\n\n' + str(hashlib.md5(content).hexdigest().upper())
        except:
            msg = 'Impossibile generare il codice !!!'
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
        dialog.run()
        dialog.destroy()

    def on_send_Email_activate(self, widget):
        sendemail = SendEmail()

    def on_master_sincro_db_activate(self, widget):
        msg ="SERVER NON ANCORA IMPLEMENTATO"
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK,
                                msg)
        dialog.run()
        dialog.destroy()

    def on_client_sincro_db_activate(self, widget):
        if "SincroDB" in Environment.modulesList and Environment.conf.SincroDB.tipo =="client":
            from promogest.modules.SincroDB.ui.SincroDB import SincroDB
            anag = SincroDB()
            showAnagrafica(self.getTopLevel(), anag)
        else:
            print "PASSIQUI"

    def on_test_promowear_button_clicked(self, button):
        msg = """ATTENZIONE!! ATTENZIONE!! ATTENZIONE!!

QUESTA FUNZIONALITÀ È STATA AGGIUNTA PER
PERMETTERE DI PROVARE IL PROMOGEST2 LITE CON
IL MODULO TAGLIA E COLORE PROMOWEAR
QUESTO MODULO SERVE A CHI DEVE GESTIRE
UNA ATTIVITÀ CHE MOVIMENTA E VENDE
ABBIGLIAMENTO O CALZATURE.
L'OPERAZIONE È IRREVERSIBILE,AGGIUNGE DIVERSE
TABELLE NEL DATABASE E NUOVE INTERAFFCE UTENTE
DEDICATE,NON CAUSA PERDITA DI DATI
MA NON È CONSIGLIATO FARLO SE NON
NE AVETE BISOGNO

UNA VOLTA PREMUTO TERMINATA LA PROCEDURA
CHIUDERE E RIAVVIARE IL PROGRAMMA

PROCEDERE ALL'INSTALLAZIONE DEL MODULO PROMOWEAR? """
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)

        response = dialog.run()
        dialog.destroy()
        if response !=  gtk.RESPONSE_YES:
            return
        if not hasattr(Environment.conf,"PromoWear"):
            Environment.conf.add_section("PromoWear")
            Environment.conf.save()
            Environment.conf.PromoWear.primoavvio = "yes"
            Environment.conf.PromoWear.mod_enable = "yes"
            Environment.conf.save()
            tables = [t.name for t in Environment.params["metadata"].sorted_tables]
            if "colore" not in tables and "taglia" not in tables:
                from promogest.modules.PromoWear.data.PromoWearDB import *
                msg = " TABELLE AGGIUNTE, RIAVVIARE IL PROGRAMMA "
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
                dialog.run()
                dialog.destroy()
        else:
#            tables = [t.name for t in Environment.params["metadata"].sorted_tables]
#            if "colore" in tables and "taglia" in tables:
            print "Pulsante di test già premuto"

    def on_ricmedio_activate(self, widget):
        """ entry Menu statistiche Ricarico medio """
        from promogest.modules.Statistiche.ui.StatisticaGenerale import StatisticaGenerale
        anag = StatisticaGenerale(idMagazzino=None, nome="RICARICO MEDIO e INFLUENZA SULLE VENDITE")
        anagWindow = anag.getTopLevel()

    def on_whatcant_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/whatCanT"
        webbrowser.open_new_tab(url)

    def on_export_magazzino_activate(self, button):
        from promogest.modules.Statistiche.ui.StatisticheMagazzino import StatisticheMagazzino
        anag = StatisticheMagazzino(idMagazzino=None)
        anagWindow = anag.getTopLevel()

    def on_main_window_key_press_event(self, widget, event):
        if event.type == gtk.gdk.KEY_PRESS:
            if event.state & gtk.gdk.CONTROL_MASK and (
                (event.state & gtk.gdk.MOD2_MASK) or (event.state & gtk.gdk.MOD1_MASK)):
                if gtk.gdk.keyval_name(event.keyval) == "m":
                    # easter egg

                    def menuitem_response(game):
                        games_menu.hide()
                        os.system(game)

                    tetris_games = (
                        'gnometris','ksirtet','xtris','kcalc','emacs','ksmiletris','ltris')
                    games_menu = gtk.Menu()
                    for game in tetris_games:
                        ret = os.system('which ' + game + ' > /dev/null')
                        if ret==0:
                            item = gtk.MenuItem(game)
                            games_menu.append(item)
                            item.connect_object("activate", menuitem_response, game)
                            item.show()
                    games_menu.popup(None, None, None, 3, event.time)
                    return True
                elif gtk.gdk.keyval_name(event.keyval) == "u":
                    # easter egg

                    def menuitem_response(utilities):
                        utilities_menu.hide()
                        os.system(utilities)

                    utils = (
                        'firefox','konqueror','thunderbird','kcalc','kate','gcalctool', "gedit")
                    utilities_menu = gtk.Menu()
                    for util in utils:
                        ret = os.system('which ' + util + ' > /dev/null')
                        if ret==0:
                            item = gtk.MenuItem(util)
                            utilities_menu.append(item)
                            item.connect_object("activate", menuitem_response, util)
                            item.show()
                    utilities_menu.popup(None, None, None, 3, event.time)
                    return True
            elif gtk.gdk.keyval_name(event.keyval) == "t":
                import random
                msg= """
Il Promogest2 "MentoR" ha generato per te due sestine
"vincenti" per il prossimo concorso del superenalotto
giocale e facci sapere .....
Mi raccomando se dovessi vincere ricordati di noi :)

Il Team:

I Numeri:   %s
                %s
""" %(str(random.sample(xrange(90), 6))[1:-1],str(random.sample(xrange(90), 6))[1:-1])
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
                dialog.run()
                dialog.destroy()

            return True
        else:
            return False

    def on_disconnect(self, widget=None):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la disconnessione?')
        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            self.destroy()
        else:
            return

    def on_quit(self, widget=None):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la chiusura?')

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            self.hide()
            gtk.main_quit()
        else:
            return

    def statusBarHandler(self):
        textStatusBar = "    PromoGest2 - 8956060615 - www.promotux.it - info@promotux.it     "
        context_id =  self.pg2_statusbar.get_context_id("main_window")
        self.pg2_statusbar.push(context_id,textStatusBar)

        if Environment.rev_locale < Environment.rev_remota:
            self.active_img.set_from_file("gui/active_off.png")
        else:
            self.active_img.set_from_file("gui/active_on.png")

class MainWindowFrame(VistaPrincipale):
    def __init__(self, mainWindow, azs):
        VistaPrincipale.__init__(self, self.mainWindow, azs)


class MagazziniFrame(ElencoMagazzini):
    """ Frame per la gestione dei magazzini
    """
    def __init__(self, mainWindow, azs):
        self.mainWindow = mainWindow
        ElencoMagazzini.__init__(self, self.mainWindow, azs)


class RegistrazioniFrame(GladeWidget):
    """ Frame per la gestione delle registrazioni """

    def __init__(self, mainWindow,azs):
        self.mainWindow = mainWindow
        self.aziendaStr = azs
        GladeWidget.__init__(self, 'registrazioni_select_frame', fileName='_registrazioni_select.glade')

    def on_documenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=2):return
        from AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)


class ListiniFrame(ElencoListini):
    """ Frame per la gestione dei listini
    """

    def __init__(self, mainWindow,azs):
        self.mainWindow = mainWindow
        ElencoListini.__init__(self, self.mainWindow,azs)

def on_anagrafica_destroyed(anagrafica_window, argList):
    mainWindow = argList[0]
    anagraficaButton= argList[1]
    mainClass = argList[2]
    if anagrafica_window in Login.windowGroup:
        Login.windowGroup.remove(anagrafica_window)
    if anagraficaButton is not None:
        anagraficaButton.set_active(False)
    if mainClass is not None:
        mainClass.on_button_refresh_clicked()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button,mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
    anagWindow.set_transient_for(window)
#    setattr(anagWindow, "mainClass",mainClass)
    anagWindow.show_all()

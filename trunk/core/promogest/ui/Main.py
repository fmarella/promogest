# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import locale
import gtk
import hashlib
import os
import glob
try:
    import ho.pisa as pisa
except:
    print """ERRORE NELL'IMPORT DI PISA prova a digitare
'sudo apt-get install python-pisa" nel terminale' """
#    import pisaLib.ho.pisa as pisa
import calendar
from promogest.lib.relativedelta import relativedelta
from datetime import datetime
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
from utils import hasAction, fencemsg, aggiorna, updateScadenzePromemoria,\
         setconf, dateTimeToString, dateToString, last_day_of_month, \
         date_range, orda, posso
from utilsCombobox import *
from ParametriFrame import ParametriFrame
from SetConf import SetConfUI
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from AnagraficaPrincipaleFrame import AnagrafichePrincipaliFrame
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.VariazioneListino import VariazioneListino
from ConfiguraWindow import ConfiguraWindow
from promogest.ui.PanUi import PanUi, checkPan
#inizializzano il customwidget
from widgets.ArticoloSearchWidget import ArticoloSearchWidget
from widgets.ClienteSearchWidget import ClienteSearchWidget
from widgets.FornitoreSearchWidget import FornitoreSearchWidget
from widgets.PersonaGiuridicaSearchWidget import PersonaGiuridicaSearchWidget
if posso("GN"):
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio \
                            import TestataGestioneNoleggio
try:
    from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False


class Main(GladeWidget):

    def __init__(self, aziendaStr, anagrafiche_modules, parametri_modules,
                anagrafiche_dirette_modules, frame_modules, permanent_frames):

        GladeWidget.__init__(self, 'main_window')
        self.main_window.set_title('*** PromoGest2 *** Azienda : '+aziendaStr+\
                                '  *** Utente : '+\
                                Environment.params['usernameLoggedList'][1]+\
                                ' ***')
        self.aziendaStr = aziendaStr

        self.statusBarHandler()
        for filename in glob.glob(Environment.promogestDir+\
                                                    "/temp/"+'*.cache'):
            os.remove(filename)
        Environment.windowGroup.append(self.getTopLevel())
        self.anagrafiche_modules = anagrafiche_modules
        self.parametri_modules = parametri_modules
        self.anagrafiche_dirette_modules=anagrafiche_dirette_modules
        self.frame_modules = frame_modules
        self.permanent_frames = permanent_frames
        self.currentFrame = None
        self.alarmFrame = None
        self.shop = Environment.shop
        self.creata = False
        if posso("SD"):
            self.sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo =="client":
            self.master_sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo =="server":
            self.client_sincro_db.destroy()
        if Environment.tipodb =="postgresql":
#            self.whatcant_button.destroy()
            self.test_promowear_button.destroy()
        self.create_allarmi_frame()
#        self.main_notebook.set_current_page(self.main_notebook.page_num(self.notifica_allarmi_frame))
#        self.main_notebook.set_current_page(0)
        if not WEBKIT:
            self.main_notebook.remove_page(3)
            self.main_notebook.remove_page(3)
        else:
            self.htmlPlanningWidget = createHtmlObj(self)
            self.planning_scrolled.add(self.htmlPlanningWidget)
            self.create_planning_frame()
            gobject.idle_add(self.create_news_frame)
#        self.pp = gobject.idle_add(checkPan, self)
        self.pp = checkPan(self)
        ll = gtk.Label()
        ll.set_markup("<b>MAGAZZINI</b>")
        self.main_notebook.append_page(self.create_magazzini_frame(),ll)
        mm = gtk.Label()
        mm.set_markup("<b>LISTINI</b>")
        self.main_notebook.append_page(self.create_listini_frame(),mm)
        self.updates()

    def show(self):
        """ Visualizza la finestra """
        self.anno_lavoro_label.set_markup('<b>Anno di lavoro:   ' + \
                                        Environment.workingYear + '</b>')
        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf,object)

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'documento48x48.png')
        model.append([3, "Documenti\n(Fatture,DDT\nPreventivi)", pbuf,None])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'primanota_48X48.png')
        model.append([4, "Prima Nota", pbuf,None])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'promemoria48x48.png')
        model.append([5, "Promemoria", pbuf,None])

        # right vertical icon list  adding modules
#        model_right = gtk.ListStore(int, str, gtk.gdk.Pixbuf, object)
        ind = 6
        for mod in self.anagrafiche_dirette_modules.keys():
            currModule = self.anagrafiche_dirette_modules[mod]
            if self.shop and currModule["module"].VIEW_TYPE[1] =="Vendita Dettaglio":
                anag = currModule["module"].getApplication()
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                #icon_view.unselect_all()
                return
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model.append(row)
            ind += 1
        for mod in self.frame_modules.keys():
            currModule = self.frame_modules[mod]
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row =(ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model.append(row)
            ind += 1

        self.main_iconview.set_model(model)
        self.main_iconview.set_text_column(1)
        self.main_iconview.set_pixbuf_column(2)
        self.main_iconview.connect('selection-changed',
                                   self.on_main_iconview_select, model)

        self.main_iconview.set_columns(1)
        self.main_iconview.set_item_width(95)
        self.main_iconview.set_size_request(115, -1)

        if self.currentFrame is None:
#            self.main_hbox.remove(self.box_immagini_iniziali)
            self._refresh()
        self.setModulesButtons()
        self.placeWindow(self.main_window)
        self.main_window.show_all()
        self.on_button_refresh_clicked()

    def updates(self):
        """ Aggiornamenti e controlli da fare all'avvio del programma
        """
        #Aggiornamento scadenze promemoria
        if posso("PR"):
            print "VERIFICA DEI PROMEMORIA IN SCADENZA"
            updateScadenzePromemoria()

    def _refresh(self):
        """
        Update the window, setting the appropriate frame
        """
        self.main_iconview.unselect_all()
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
        ll = gtk.Label()

        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = model[i][0]

        if selection == 3:
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
            if not hasAction(actionID=2):return
            from AnagraficaPrimaNota import AnagraficaPrimaNota
            anag = AnagraficaPrimaNota(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 5:
            if posso("PR"):
                from AnagraficaPromemoria import AnagraficaPromemoria
                anag = AnagraficaPromemoria(self.aziendaStr)
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                icon_view.unselect_all()
                return
            else:
                fencemsg()
        else:
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
        self.main_notebook.set_current_page(0)
        self._refresh()

#    def on_main_notebook_switch_page(self, notebook, page, page_num):
#        print "CCCCCCCCCCCCCCCCCCCCC", notebook, page, page_num

    def setModulesButtons(self):

        if self.anagrafiche_modules is not None:
            for module in self.anagrafiche_modules.iteritems():
                module_button = gtk.Button()
                module_butt_image = gtk.Image()
                module_butt_image.set_from_file(module[1]['guiDir']+'/'+module[1]['module'].VIEW_TYPE[2])
                module_button.set_image(module_butt_image)
                module_button.set_label(module[1]['module'].VIEW_TYPE[1])
                module_button.connect('clicked', self.on_module_button_clicked)
                self.anagrafiche_moduli_vbox.pack_start(module_button, False, False)
            return
        else:
            return

    def on_module_button_clicked(self, button):
        label = button.get_label()
        for mk in self.anagrafiche_modules.iteritems():
            module = mk[1]['module']
            if label == module.VIEW_TYPE[1]:
                #chiave di tutto il richiamo di passaggio alla classe in module.py che poi fa la vera istanza"
                anag = module.getApplication()
                showAnagrafica(self.getTopLevel(), anag, button=None, mainClass=self)

    def on_articoli_button_clicked(self, toggleButton):
        if not hasAction(actionID=2): return
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(aziendaStr=Environment.azienda)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_forniture_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_vettori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_agenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("AG"):
            from promogest.modules.Agenti.ui.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_active(False)

    def on_categorie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
        anag = AnagraficaCategorieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_famiglie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
        anag = AnagraficaFamiglieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieClienti import AnagraficaCategorieClienti
        anag = AnagraficaCategorieClienti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
        anag = AnagraficaCategorieFornitori()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_utenti_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import AnagraficaUtenti
            anag = AnagraficaUtenti()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active',False)

    def on_ruoli_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.AnagraficaRuoli import AnagraficaRuoli
            anag = AnagraficaRuoli()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active',False)

    def on_ruoli_azioni_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.ManageRoleAction import ManageRuoloAzioni
            anag = ManageRuoloAzioni()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active',False)

    def on_multipli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_pagamenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaPagamenti import AnagraficaPagamenti
        anag = AnagraficaPagamenti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)


    def on_banche_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaBanche import AnagraficaBanche
        anag = AnagraficaBanche()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)


    def on_categorie_contatti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieContatti import AnagraficaCategorieContatti
        anag = AnagraficaCategorieContatti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)


    def on_aliquote_iva_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaAliquoteIva import AnagraficaAliquoteIva
        anag = AnagraficaAliquoteIva()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_imballaggi_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaImballaggi import AnagraficaImballaggi
        anag = AnagraficaImballaggi()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

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
        g = file(Environment.tempDir+".temp.pdf", "wb")
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
            dayName = [x.decode("iso8859-1") for x in dayName2]
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
                if posso("GN"):
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
                if posso("GN"):
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
                    Environment.pg2log.info("LEGGERO RITARDO NEL RECUPERO DEI FEED")

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
        for feed in feedList[0:3]:
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
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == gtk.RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_inserimento_codice_activate(self,widget):
        from promogest.dao.Setconf import SetConf
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
        dialog.set_markup("""<b>CODICE ATTIVAZIONE PACCHETTO</b>""")
        hbox = gtk.HBox()
        entry___ = gtk.Entry()

        label = gtk.Label(False)
        label.set_markup("<b>   Inserisci codice</b>")
        hbox.pack_start(label)
        hbox.pack_start(entry___)
        dialog.vbox.pack_start(hbox)
        dialog.show_all()
        response = dialog.run()
        codice = entry___.get_text()
#        hascode = str(hashlib.sha224(codice+orda(codice)).hexdigest())
        sets = SetConf().select(key="install_code",section="Master")
        if sets:
            sets[0].delete()
        k = SetConf()
        k.key = "install_code"
        k.value =str(hashlib.sha224(codice+orda(codice)).hexdigest())
        k.section = "Master"
        k.description = "codice identificativo della propria installazione"
        k.tipo_section = "General"
        k.tipo = "Lite"
        k.active = True
        k.date = datetime.datetime.now()
        k.persist()
        dialog.destroy()


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

        if Environment.tipodb == "sqlite":
            msg = """NELLA VERSIONE LITE IL BACKUP SI
EFFETTUA COPIANDO IL FILE db CHE SI TROVA NELLA CARTELLA
promogest2 IN /HOME/NOMEUTENTE/ O IN C:/UTENTI/NOMEUTENTE"""
            messageInfo(msg= MSG)
        else:
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

    def on_pan_active_clicked(self, button):
#        if not hasAction(actionID=14):return
#        configuraWindow = ConfiguraWindow(self)
        configuraWindow = PanUi(self)
        showAnagrafica(self.getTopLevel(), configuraWindow)


    def on_seriale_menu_activate(self, widget):
        from promogest.dao.Setconf import SetConf
        try:
            data = SetConf().select(key="install_code",section="Master")
            codice = data[0].value
            msg = 'Codice installazione:\n\n' + str(codice)
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
        if posso("SD") and Environment.conf.SincroDB.tipo =="client":
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

    def on_controllo_fatturato_activate(self, widget):
        print "CONTROLLO FATTURATO NON GESTITO"

    def on_whatcant_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/whatCanT"
        webbrowser.open_new_tab(url)

    def on_export_magazzino_activate(self, button):
        from promogest.modules.Statistiche.ui.StatisticheMagazzino import StatisticheMagazzino
        anag = StatisticheMagazzino(idMagazzino=None)
        anagWindow = anag.getTopLevel()

    def on_main_window_key_press_event(self, widget, event):
        return
#        if event.type == gtk.gdk.KEY_PRESS:
#            if event.state & gtk.gdk.CONTROL_MASK and (
#                (event.state & gtk.gdk.MOD2_MASK) or (event.state & gtk.gdk.MOD1_MASK)):
#                if gtk.gdk.keyval_name(event.keyval) == "m":
#                    # easter egg

#                    def menuitem_response(game):
#                        games_menu.hide()
#                        os.system(game)

#                    tetris_games = (
#                        'gnometris','ksirtet','xtris','kcalc','emacs','ksmiletris','ltris')
#                    games_menu = gtk.Menu()
#                    for game in tetris_games:
#                        ret = os.system('which ' + game + ' > /dev/null')
#                        if ret==0:
#                            item = gtk.MenuItem(game)
#                            games_menu.append(item)
#                            item.connect_object("activate", menuitem_response, game)
#                            item.show()
#                    games_menu.popup(None, None, None, 3, event.time)
#                    return True
#                elif gtk.gdk.keyval_name(event.keyval) == "u":
#                    # easter egg

#                    def menuitem_response(utilities):
#                        utilities_menu.hide()
#                        os.system(utilities)

#                    utils = (
#                        'firefox','konqueror','thunderbird','kcalc','kate','gcalctool', "gedit")
#                    utilities_menu = gtk.Menu()
#                    for util in utils:
#                        ret = os.system('which ' + util + ' > /dev/null')
#                        if ret==0:
#                            item = gtk.MenuItem(util)
#                            utilities_menu.append(item)
#                            item.connect_object("activate", menuitem_response, util)
#                            item.show()
#                    utilities_menu.popup(None, None, None, 3, event.time)
#                    return True
#            elif gtk.gdk.keyval_name(event.keyval) == "t":
#                import random
#                msg= """
#Il Promogest2 "MentoR" ha generato per te due sestine
#"vincenti" per il prossimo concorso del superenalotto
#giocale e facci sapere .....
#Mi raccomando se dovessi vincere ricordati di noi :)

#Il Team:

#I Numeri:   %s
#                %s
#""" %(str(random.sample(xrange(90), 6))[1:-1],str(random.sample(xrange(90), 6))[1:-1])
#                dialog = gtk.MessageDialog(self.getTopLevel(),
#                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
#                                   gtk.MESSAGE_INFO,
#                                   gtk.BUTTONS_OK,
#                                   msg)
#                dialog.run()
#                dialog.destroy()

#            return True
#        else:
#            return False

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
        textStatusBar = "    PromoGest2 - 800 034561 - www.promotux.it - info@promotux.it     "
        context_id =  self.pg2_statusbar.get_context_id("main_window")
        self.pg2_statusbar.push(context_id,textStatusBar)

        if Environment.rev_locale < Environment.rev_remota:
            self.active_img.set_from_file("gui/active_off.png")
            self.aggiornamento_label.set_label("DA AGGIORNARE!!! ")
        else:
            self.active_img.set_from_file("gui/active_on.png")
            self.aggiornamento_label.set_label("AGGIORNATO ")

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
    if anagrafica_window in Environment.windowGroup:
        Environment.windowGroup.remove(anagrafica_window)
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

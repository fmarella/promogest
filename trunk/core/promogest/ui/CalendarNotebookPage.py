# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
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

import calendar
from promogest.lib.relativedelta import relativedelta
from promogest.lib.utils import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.ui.PrintDialog import PrintDialogHandler
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Promemoria import Promemoria
from  xhtml2pdf import pisa

try:
    if Environment.pg3:
        from gi.repository.WebKit import WebView
    else:
        from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False

class CalendarNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnnn, azienda):
        GladeWidget.__init__(self, root='calendario_frame',
                                    path='calendario_notebook.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.mainoo = mainnnn
        self.aziendaStr = azienda or ""
        self.htmlPlanningWidget = createHtmlObj(self)
        self.planning_scrolled.add(self.htmlPlanningWidget)
#                    self.create_planning_frame()
#        gobject.idle_add(self.create_planning_frame)
        self.create_planning_frame()

    def draw(self):
        return self

    def on_when_combo_changed(self, combo):
        if combo.get_active() == 0:
            Environment.view = "month"
        elif combo.get_active() == 1:
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
        anag = PrintDialogHandler(self.mainoo.main_window, nomefile)
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

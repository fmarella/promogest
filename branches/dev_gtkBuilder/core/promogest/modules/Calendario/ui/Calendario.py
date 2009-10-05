# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import os, popen2
import calendar
from calendar import Calendar
from datetime import datetime, timedelta, date
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.ui.utils import *
from promogest.ui import utils
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML

class Calendario(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self):
        GladeWidget.__init__(self, 'calendar_window',
                fileName="Calendario/gui/calendar.glade", isModule=True)
        self._window = self.calendar_window
        self.placeWindow(self._window)
        self.html_main = createHtmlObj(self)
        self.html_main_scrolledwindow.add(self.html_main)
        renderHTML(self.html_main,html="")
        self.html_detail = createHtmlObj(self)
        self.html_detail_scrolledwindow.add(self.html_detail)
        renderHTML(self.html_detail,html="")
        self.calendar1.set_detail_height_rows(232)
        self.on_corrente_button_clicked()
        #self.draw()


    def on_month_button_clicked(self, button):
        cal = calendar
        cal.setfirstweekday(6)
        a = Calendar()
        #a.setfirstweekday(6)
        data = date.today()
        print a, data
        annoCorrente = data.year
        giornoCorrente = data.day
        meseCorrente = data.month
        #b = a.Calendar()
        monthdate = a.itermonthdates(annoCorrente,meseCorrente)
        for dd in monthdate:
            print dd
            #print dd, type(dd), dir(dd), dd.day, dd.month, dd.year
        monthdatecalendar = a.monthdatescalendar(annoCorrente,meseCorrente)
        for ee in monthdatecalendar:
            print ee, meseCorrente, type(meseCorrente)
            for e in ee:
                print "OOEEO", e, e.day, e.weekday(), e.today(), e.ctime() #e.timetuple(),
        pageData = {'file' : 'calendar_montly.html',
            #"subdomain": addSlash(subdomain),
            "cal":cal,
            "monthdatecalendar": monthdatecalendar,
            "annoCorrente":annoCorrente,
            "meseCorrente":meseCorrente,
            "giornoCorrente":giornoCorrente,
            "data":data,
            }
        html = renderTemplate(pageData)
        renderHTML(self.html_main, html)

    def on_week_button_clicked(self, button):
        print "SETTIMANA"

    def on_day_button_clicked(self, button):
        cal = calendar
        cal.setfirstweekday(6)
        a = Calendar()
        #a.setfirstweekday(6)
        data = date.today()
        annoCorrente = data.year
        giornoCorrente = data.day
        meseCorrente = data.month
        monthdate = a.itermonthdates(annoCorrente,meseCorrente)
        monthdatecalendar = a.monthdatescalendar(annoCorrente,meseCorrente)
        pageData = {'file' : 'calendar_day.html',
                    #"subdomain": addSlash(subdomain),
                    "cal":cal,
                    "monthdatecalendar": monthdatecalendar,
                    "annoCorrente":annoCorrente,
                    "meseCorrente":meseCorrente,
                    "giornoCorrente":giornoCorrente,
                    "data":data,
        }
        html = renderTemplate(pageData)
        renderHTML(self.html_main, html)

    def on_corrente_button_clicked(self, button=None):
        """ riporto la data al valore odierno"""
        month = int(date.today().month)
        year= int(date.today().year)
        day = int(date.today().day)
        self.calendar1.select_month(month,year)
        self.calendar1.select_day(day)


    def on_quit_button_clicked(self, widget, event=None):
        self.destroy()
        return None

    def on_rhesus_button_clicked(self, widget):
        if self.dao is not None:
            self._righe.append(self.dao.id)
            self.on_scontrini_window_close(widget)

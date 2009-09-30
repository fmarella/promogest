# -*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
""" gestione delle pagine statiche non gestite da CMS"""
import calendar
from calendar import Calendar
from core.lib.utils import *
from core.lib.page import Page
from datetime import date

def calendar_montly(req,static=None, subdomain=None):

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
    pageData = {'file' : 'calendar_montly',
        "subdomain": addSlash(subdomain),
        "cal":cal,
        "monthdatecalendar": monthdatecalendar,
        "annoCorrente":annoCorrente,
        "meseCorrente":meseCorrente,
        "giornoCorrente":giornoCorrente,
        "data":data,
        }
    return Page(req).render(pageData)

def calendar_day(req,static=None, subdomain=None):
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
    pageData = {'file' : 'calendar_day',
                "subdomain": addSlash(subdomain),
                "cal":cal,
                "monthdatecalendar": monthdatecalendar,
                "annoCorrente":annoCorrente,
                "meseCorrente":meseCorrente,
                "giornoCorrente":giornoCorrente,
                "data":data,
    }
    return Page(req).render(pageData)


def oneMonth(self, static=None, subdomain=None):
    a = Calendar()
    yeardatescalendar = a.yearsdatescalendar(annoCorrente,meseCorrente)
    data = date.today()
    annoCorrente = data.year
    giornoCorrente = data.day
    meseCorrente = data.month
    pageData = {'file' : 'one_month',
                "subdomain": addSlash(subdomain),
                #"cal":cal,
                "yeardatescalendar": yeardatescalendar,
                "annoCorrente":annoCorrente,
                "meseCorrente":meseCorrente,
                "giornoCorrente":giornoCorrente,
                "data":data,
    }
    return Page(req).render(pageData)
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

import gtk
from promogest.ui.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.lib import feedparser

try:
    from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False

class NewsNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main, azienda):
        GladeWidget.__init__(self, 'notizie_frame',
                                    'news_notebook.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.main = main
        self.aziendaStr = azienda or ""
        gobject.idle_add(self.create_news_frame)

    def draw(self):
        return self

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
            d = feedparser.parse("http://www.promogest.me/newsfeed")
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

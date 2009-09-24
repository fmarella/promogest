# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>
import os
import sys
import gobject
try:
    from webkit import WebView
    WEBKIT = True
except:
    import gtkhtml2
    WEBKIT = False
from HtmlTextView import HtmlTextView
import urllib2
import webbrowser
from promogest import Environment
from  promogest.ui import utils
from jinja2 import Environment  as Env
from jinja2 import FileSystemLoader,FileSystemBytecodeCache

templates_dir =Environment.templates_dir

jinja_env = Env(loader=FileSystemLoader(templates_dir),
        bytecode_cache = FileSystemBytecodeCache(os.path.join(Environment.promogestDir, 'temp'), '%s.cache'))
jinja_env.globals['environment'] = Environment
jinja_env.globals['utils'] = utils

class Pg2Html(object):
    def __init__(self,mainWidget,widget=None):
        self.mainWidget = mainWidget
        self.widget = widget

    def htmlObj(self):
        try:
            self.mainWidget.html = WebView()
            return True
        except:
            self.mainWidget.html = gtkhtml2.View()
            return False

def renderTemplate(pageData):
    jinja_env.globals['ui'] = pageData["file"].split(".")[0]
    if "feed" not in pageData:
        pageData["feed"] = []
    if "dao" not in pageData:
        pageData["dao"] = []
    if "objects" not in pageData:
        pageData["objects"] = []
    html = jinja_env.get_template(pageData["file"]).render(dao=pageData["dao"],objects=pageData["objects"], feed=pageData["feed"])
    return html

def on_html_request_url(document, url, stream):

    def render():
        try:
            f = open(url, 'rb')
            stream.write(f.read())
            f.close()
            stream.close()
        except:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            html = response.read()
            stream.write(html)
            stream.close()
    gobject.idle_add(render)


def on_html_link_clicked(url, link):
    def linkOpen():
        webbrowser.open_new_tab(link)
        #print link
    gobject.idle_add(linkOpen)
    """ funzione di apertura dei link presenti nelle pagine html di anteprima"""
    #print "URLLLLLLLLLLLLLLLLLLLLLLLLLL", dir(url)
    #if link =="/tt":
        #dialog = gtk.MessageDialog(None,
                                #gtk.DIALOG_MODAL
                                #| gtk.DIALOG_DESTROY_WITH_PARENT,
                                #gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                #'Confermi la chiusura ?')
        #response = dialog.run()
        #dialog.destroy()
        #if response ==  gtk.RESPONSE_YES:
            #self.setVisible(False)
        #else:
    return True

def renderHTML(widget, html):
    if WEBKIT:
            widget.load_string(html,"text/html","utf-8", "file:///"+sys.path[0]+os.sep)
    else:
        document = gtkhtml2.Document()
        document.connect('request_url', on_html_request_url)
        document.connect('link_clicked', on_html_link_clicked)
        document.open_stream('text/html')
        document.write_stream(html)
        document.close_stream()
        widget.set_document(document)
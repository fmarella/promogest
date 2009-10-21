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

templates_dir = [os.path.join('templates'),os.path.join('report-templates')]
jinja_env = None

def env(templates_dir):
    jinja_env = Env(loader=FileSystemLoader(templates_dir),
            bytecode_cache = FileSystemBytecodeCache(os.path.join(Environment.promogestDir, 'temp'), '%s.cache'))
    def noNone(value):
        if value =="None":
            return ""
        elif not value:
            return ""
        else:
            return value
    jinja_env.filters['nonone'] = noNone

    return jinja_env

"""
    createHtmlObj = restituisce un oggetto del render html o gtkhtml2 o webkit
    renderHTMLTemplate o renderTemplate = Restituiscono una stringa html dopo la
                                            renderizzazione del template engine
    renderHTML = inserisce il codice html dentro l'oggetto
"""



def createHtmlObj(mainWidget,widget=None):
    try:
        return WebView()
    except:
        return gtkhtml2.View()

def renderTemplate(pageData):
    if "feed" not in pageData: pageData["feed"] = []
    if "dao" not in pageData:  pageData["dao"] = []
    if "objects" not in pageData: pageData["objects"] = []
    jinja_env.globals['environment'] = Environment
    jinja_env.globals['utils'] = utils
    pageData["titolo"] = pageData["file"].split(".")[0].capitalize()
    html = jinja_env.get_template("/"+ pageData["file"]).render(pageData= pageData,dao=pageData["dao"],
                    objects=pageData["objects"], feed=pageData["feed"])
    return html

def _on_html_request_url(document, url, stream):

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

def _on_html_link_clicked(url, link):
    def linkOpen():
        webbrowser.open_new_tab(link)
        #print link
    gobject.idle_add(linkOpen)
    return True

def renderHTMLTemplate(pageData):
    return renderTemplate(pageData)

def renderHTML(widget, html):
    if WEBKIT:
            widget.load_string(html,"text/html","utf-8", "file:///"+sys.path[0]+os.sep)
    else:
        document = gtkhtml2.Document()
        document.connect('request_url', _on_html_request_url)
        document.connect('link_clicked', _on_html_link_clicked)
        document.open_stream('text/html')
        document.write_stream(html)
        document.close_stream()
        widget.set_document(document)
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
#from HtmlTextView import HtmlTextView
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
def apriAnagraficaArticoliEdit(articoloId):
    from promogest.ui.AnagraficaArticoli import AnagraficaArticoli
    from promogest.ui.AnagraficaArticoliEdit import AnagraficaArticoliEdit
    from promogest.dao.Articolo import Articolo
    a = AnagraficaArticoli()
    art = Articolo().getRecord(id=articoloId)
    a.on_record_edit_activate(a, dao=art)

def apriTestataDocumentoEdit(testataDocumentoId):
    from promogest.ui.AnagraficaDocumenti import AnagraficaDocumenti
#    from promogest.ui.AnagraficaDocumentiEdit import AnagraficaDocumentiEdit
    from promogest.dao.TestataDocumento import TestataDocumento
    a = AnagraficaDocumenti()
    art = TestataDocumento().getRecord(id=testataDocumentoId)
    a.on_record_edit_activate(a, dao=art)

def apriAnagraficaPromemoriaNew(selectedData=None):
    from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
    a = AnagraficaPromemoria(selectedData=selectedData)
    a.on_record_new_activate(a)

def apriAnagraficaPromemoriaEdit(promemoriaId):
    from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
    from promogest.dao.Promemoria import Promemoria
    a = AnagraficaPromemoria()
    pro = Promemoria().getRecord(id=promemoriaId)
    a.on_record_edit_activate(a, dao=pro)

def _on_navigation_requested(view, frame, req, data=None):
    uri = req.get_uri()
    if uri.startswith("program:/"):
        agg = uri.split("/")[1]
        if "articoloId" in agg:
            exec(agg)
            apriAnagraficaArticoliEdit(articoloId)
        elif "newPromemoria" in agg:
            data = agg.split("=")[1].replace("-","/")
            dta = data.split("/")
            datadef = dta[2]+"/"+dta[1]+"/"+dta[0]
            selectedData = datadef+" 09:00"
            apriAnagraficaPromemoriaNew(selectedData=selectedData)
        elif "promemoriaId" in agg:
            exec(agg)
            apriAnagraficaPromemoriaEdit(promemoriaId)
        elif "testataDocumentoId" in agg:
            exec(agg)
            apriTestataDocumentoEdit(testataDocumentoId)
    else:
        return False
    return True

def createHtmlObj(mainWidget,widget=None):
    try:
#    def _on_hovering_over_link(widget, title,uri,userdata):
#        print "OOOOOIJJJJJJJJJJJJJJJJJJJJJ", widget, title, uri, userdata
        a= WebView()
#    a.connect('hovering-over-link', _on_hovering_over_link,a)
        a.connect('navigation-requested', _on_navigation_requested,a)
        return a
    except:
        return gtkhtml2.View()

def renderTemplate(pageData):
    if "feed" not in pageData:
        pageData["feed"] = []
    if "dao" not in pageData:
        pageData["dao"] = []
    if "objects" not in pageData:
        pageData["objects"] = []
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

def linkOpen(link):
    webbrowser.open_new_tab(link)

def _on_html_link_clicked(url, link):
    agg = link.split("/")[1]
    if "articoloId" in agg:
        exec(agg)
        apriAnagraficaArticoliEdit(articoloId)
    elif "newPromemoria" in agg:
            apriAnagraficaPromemoriaNew()
    else:
        gobject.idle_add(linkOpen, link)
    return True

if not WEBKIT:
    document = gtkhtml2.Document()
    document.connect('request_url', _on_html_request_url)
    document.connect('link_clicked', _on_html_link_clicked)

def renderHTMLTemplate(pageData):
    return renderTemplate(pageData)

def renderHTML(widget, html):

    if WEBKIT:
        widget.load_string(html,"text/html","utf-8", "file:///"+sys.path[0]+os.sep)
        widget.show()
    else:
        document.open_stream('text/html')
        document.write_stream(html)
        document.close_stream()
        widget.set_document(document)

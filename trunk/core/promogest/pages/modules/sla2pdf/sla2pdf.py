# -*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
""" gestione delle pagine statiche non gestite da CMS"""

from calendar import Calendar
from core.lib.utils import *
from core.lib.page import Page
from core.lib.sla2pdf.Sla2Pdf import Sla2Pdf

def sla2pdff(req,static=None, subdomain=None):
    return
    name = None

    if req.args.get("upload"):
        f = req.files['slafile']
        name =f.filename
        data = f.read()
        fileObj = open( "templates/"+name ,"wb")
        fileObj.write(data)
        fileObj.close()
        #_slaTemplate = open( name ,"r")
        _slaTemplateObj=Sla2Pdf(slafile="templates/"+name).createPDF()
    pageData = {'file' : 'sla2pdf',
            "subdomain": addSlash(subdomain),
            "pdffile":name,
            "pdfname":name
            #"feedTrac" :feedTrac,

}
    return Page(req).render(pageData)

# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Alceste Scalas <alceste@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it

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

import time
#from promogest.ui.gtk_compat import *
import os
import sys
import threading
import os.path
from promogest.Environment import conf
from GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.lib.XmlGenerator import XlsXmlGenerator
from promogest.lib.CsvGenerator import CsvFileGenerator
from utils import *
import Login
import subprocess ,shlex
from promogest import Environment
from calendar import Calendar
#if Environment.new_print_enjine:
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
#else:


from promogest.ui.SendEmail import SendEmail
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda

class AnagraficaHtml(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica """

    def __init__(self, anagrafica, template, description):
        self._anagrafica = anagrafica
        self._gtkHtml = None # Will be filled later
        self.description = description
        self.defaultFileName = template
        self.dao = None
        self._slaTemplateObj = None

    def setDao(self, dao):
        """ Visualizza il Dao specificato """
        self.dao = dao

        self._refresh()
        if dao and Environment.debugDao:
            #FIXME: add some logging level check here
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            print ("\n\n=== DAO object dump ===\n\n"
                    + pp.pformat(dao.dictionary(complete=True))
                    + "\n\n")

    def refresh(self):
        """ Aggiorna la vista HTML """
        self._refresh()

    def variations(self):
        return self.dao

    def _refresh(self):
        """ show the html page in the custom widget"""
        pageData = {}
        eventipreves = []
        eventiprevesAT = []
        calendarioDatetime = []
        html = "<html><body></body></html>"
        if not self._gtkHtml:
            self._gtkHtml = self._anagrafica.getHtmlWidget()
        if self.dao and self.dao.__class__.__name__ =="Articolo":
            if posso("GN"):
                from promogest.dao.TestataDocumento import TestataDocumento
                from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
                preves = TestataDocumento().select(daData= stringToDate("1/1/"+Environment.workingYear),
                                aData=stringToDate("31/12/"+Environment.workingYear), batchSize=None,
                                idArticolo=self.dao.id)
                for p in preves:
                    eventipreves.append((p.data_documento.toordinal(),{"id":p.id,
                                                        "operazione":p.operazione,
                                                        "short":p.ragione_sociale_cliente,
                                                        "tipo":"data_documento",
                                                        "colore":"#6495ED"},p.data_documento.day))
                    arcTemp = TestataGestioneNoleggio().select(idTestataDocumento=p.id, batchSize=None)
                    for a in arcTemp:
                        startDate =a.data_inizio_noleggio
                        stopDate =a.data_fine_noleggio
                        dateList= date_range(startDate,stopDate)
                        for d in dateList:
                            eventiprevesAT.append((d.toordinal(),{"id":p.id,
                                            "operazione":p.operazione,
                                            "short":p.ragione_sociale_cliente,
                                            "tipo":"data_documento",
                                            "colore":"#AFEEEE"},d.day))
                calendarioDatetime = Calendar().yeardatescalendar(int(Environment.workingYear))
        #self.dao = self.variations()
        pageData = {
                "file" :self.defaultFileName+".html",
                "dao":self.dao,
                "objects":self.dao,
                "eventipreves": eventipreves,
                "eventiprevesAT": eventiprevesAT,
                "calendarioDatetime": calendarioDatetime,
                }
        html = renderTemplate(pageData)
        self.hh = html
        renderHTML(self._gtkHtml,html)

    def setObjects(self, objects):
        # FIXME: dummy function for API compatibility, refactoring(TM) needed!
        pass

    def pdf(self, operationName, classic=None, template_file=None):
        """ Qui si stampa selezione """
        self._slaTemplate = None
        self._slaTemplateObj=None
        # aggiungo i dati azienda al dao in modo che si gestiscano a monte
        azienda = Azienda().getRecord(id=Environment.azienda)
        operationNameUnderscored = operationName.replace(' ' , '_').lower()
        a= Environment.templatesDir + operationNameUnderscored + '.sla'
        Environment.pg2log.info(a)
        if os.path.exists(Environment.templatesDir + operationNameUnderscored + '.sla'):
            self._slaTemplate = Environment.templatesDir + operationNameUnderscored + '.sla'
        elif "DDT" in operationName and os.path.exists(Environment.templatesDir + 'ddt.sla'):
            self._slaTemplate = Environment.templatesDir + 'ddt.sla'
        else:
            Environment.pg2log.info("UTILIZZO il documento.sla normale per la stampa")
            self._slaTemplate = Environment.templatesDir + self.defaultFileName + '.sla'
        """ Restituisce una stringa contenente il report in formato PDF """

        print "DAO", self.dao.__class__.__name__

        if self.dao.__class__.__name__ in Environment.fromHtmlLits:
            import ho.pisa as pisa

            f = self.hh
            g = file(Environment.tempDir+".temp.pdf", "wb")
            pdf = pisa.CreatePDF(str(f),g)
            g .close()
            g=file(Environment.tempDir+".temp.pdf", "r")
            f= g.read()
            g.close()
            return f
        param = [self.dao.dictionary(complete=True)]
        multilinedirtywork(param)
        try:
            if hasattr(Environment.conf.Documenti,"jnet"):
                from promogest.modules.NumerazioneComplessa.jnet import numerazioneJnet
                param[0]["numero"]= numerazioneJnet(self.dao)
        except:
            print ""
        if azienda:
            azidict = azienda.dictionary(complete=True)
            for a,b in azidict.items():
                k = "azi_"+a
                azidict[k] = b
                del azidict[a]
            param[0].update(azidict)
        if "operazione" in param[0]:
            if (param[0]["operazione"] =="DDT vendita" or\
                     param[0]["operazione"] =="DDT acquisto") and \
                                     param[0]["causale_trasporto"] != "":
                param[0]["operazione"] = "DDT"
        # controllo la versione dello sla che devo elaborare
        versione = scribusVersion(self._slaTemplate)
        Environment.pg2log.info("VERSIONE SLA: "+ str(versione))

        if Environment.new_print_enjine:
            stpl2sla = SlaTpl2Sla_ng(slafile=None,label=None, report=None,
                                    objects=param,
                                    daos=self.dao,
                                    slaFileName=self._slaTemplate,
                                    pdfFolder=self._anagrafica._folder,
                                    classic=True,
                                    template_file=None).fileElaborated()
            return Sla2Pdf_ng(slafile=stpl2sla).translate()
        else:
            if self._slaTemplateObj is None:
                self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                            pdfFolder=self._anagrafica._folder,
                                            report=self._anagrafica._reportType,
                                            classic = True,
                                            template_file=template_file)
            Environment.pg2log.info("DAO IN STAMPA CLASSIC: "+str(self.dao))
            return self._slaTemplateObj.serialize(param, classic = True,dao=self.dao)

    def cancelOperation(self):
        """ Cancel current operation """
        self._slaTemplateObj.cancelOperation()

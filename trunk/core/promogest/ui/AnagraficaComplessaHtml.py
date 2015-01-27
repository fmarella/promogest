# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni <francesco@promotux.it
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from calendar import Calendar
import os.path
from promogest import Environment
from promogest.lib.utils import *
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
from promogest.lib.HtmlHandler import renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda


class AnagraficaHtml(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica """

    def __init__(self, anagrafica, template, description):
        self._anagrafica = anagrafica
        self._gtkHtml = None
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
        if self.dao and self.dao.__class__.__name__ == "Articolo":
            if posso("GN"):
                from promogest.dao.TestataDocumento import TestataDocumento
                from promogest.modules.GestioneNoleggio.dao.\
                    TestataGestioneNoleggio import TestataGestioneNoleggio
                preves = TestataDocumento().select(daData=stringToDate("1/1/" \
                                        + Environment.workingYear),
                                aData=stringToDate("31/12/" \
                                        + Environment.workingYear),
                                                    batchSize=None,
                                idArticolo=self.dao.id)
                for p in preves:
                    eventipreves.append((p.data_documento.toordinal(),
                                            {"id": p.id,
                                            "operazione": p.operazione,
                                            "short": p.ragione_sociale_cliente,
                                            "tipo": "data_documento",
                                            "colore": "#6495ED"},
                                            p.data_documento.day))
                    arcTemp = TestataGestioneNoleggio().select(
                                        idTestataDocumento=p.id,
                                        batchSize=None)
                    for a in arcTemp:
                        startDate = a.data_inizio_noleggio
                        stopDate = a.data_fine_noleggio
                        dateList = date_range(startDate, stopDate)
                        for d in dateList:
                            eventiprevesAT.append((d.toordinal(), {"id": p.id,
                                            "operazione": p.operazione,
                                            "short": p.ragione_sociale_cliente,
                                            "tipo": "data_documento",
                                            "colore": "#AFEEEE"},
                                            d.day))
                calendarioDatetime = Calendar().yeardatescalendar(
                                                int(Environment.workingYear))
        self.dao = self.variations()
        pageData = {
                "file": self.defaultFileName + ".html",
                "dao": self.dao,
                "tipopg" :Environment.modulesList,
                "objects": self.dao,
                "eventipreves": eventipreves,
                "eventiprevesAT": eventiprevesAT,
                "calendarioDatetime": calendarioDatetime,
                }
        html = renderTemplate(pageData)
        self.hh = html
        renderHTML(self._gtkHtml, html)

    def setObjects(self, objects):
        # FIXME: dummy function for API compatibility, refactoring(TM) needed!
        pass

    def pdf(self, operationName, classic=None, template_file=None):
        """ Qui si stampa selezione """
        from sqlalchemy.orm import undefer_group
        self._slaTemplate = None
        self._slaTemplateObj = None
        # aggiungo i dati azienda al dao in modo che si gestiscano a monte
        azienda = Azienda().getRecord(id=Environment.azienda)
        operationNameUnderscored = operationName.replace(' ', '_').lower()
        a = Environment.templatesDir + operationNameUnderscored + '.sla'
        Environment.pg2log.info(a)
        if os.path.exists(Environment.templatesDir + operationNameUnderscored \
                                                                + '.sla'):
            self._slaTemplate = Environment.templatesDir \
                                    + operationNameUnderscored \
                                    + '.sla'
        elif "DDT" in operationName and \
                        os.path.exists(Environment.templatesDir + 'ddt.sla'):
            self._slaTemplate = Environment.templatesDir + 'ddt.sla'
        else:
            self._slaTemplate = Environment.templatesDir \
                                        + self.defaultFileName \
                                        + '.sla'
        """ Restituisce una stringa contenente il report in formato PDF """

        if self.dao.__class__.__name__ in Environment.fromHtmlLits:
            from  xhtml2pdf import pisa
            f = self.hh
            g = file(Environment.tempDir + ".temp.pdf", "wb")
            pisa.CreatePDF(f, g)
            g .close()
            g = file(Environment.tempDir + ".temp.pdf", "r")
            f = g.read()
            g.close()
            return f
        param = [self.dao.dictionary(complete=True)]
        multilinedirtywork(param)
        try:
            if hasattr(Environment.conf.Documenti, "jnet"):
                from promogest.modules.NumerazioneComplessa.jnet import\
                                                             numerazioneJnet
                param[0]["numero"] = numerazioneJnet(self.dao)
        except:
            pass
        if azienda:
            azidict = azienda.dictionary(complete=True)
            for a, b in azidict.items():
                k = "azi_" + a
                azidict[k] = b
                del azidict[a]
            param[0].update(azidict)

        if 'operazione' in param[0] and 'causale_trasporto' in param[0]:
            if (param[0]["operazione"] in ["DDT vendita", "DDT acquisto"]) \
                 and param[0]["causale_trasporto"] != "":
                param[0]["operazione"] = "DDT"

        # controllo la versione dello sla che devo elaborare
        versione = scribusVersion(self._slaTemplate)
        Environment.pg2log.info("VERSIONE SLA: " + str(versione))

        if Environment.new_print_enjine:
            stpl2sla = SlaTpl2Sla_ng(slafile=None, label=None, report=None,
                                    objects=param,
                                    daos=self.dao,
                                    slaFileName=self._slaTemplate,
                                    pdfFolder=self._anagrafica._folder,
                                    classic=True,
                                    template_file=None).fileElaborated()
            return Sla2Pdf_ng(slafile=stpl2sla).translate()
        else:
            if self._slaTemplateObj is None:
                self._slaTemplateObj = SlaTpl2Sla(
                                        slaFileName=self._slaTemplate,
                                        pdfFolder=self._anagrafica._folder,
                                        report=self._anagrafica._reportType,
                                        classic=True,
                                        template_file=template_file)
            Environment.pg2log.info("DAO IN STAMPA CLASSIC: " + str(self.dao))
            return self._slaTemplateObj.serialize(param, classic=True,
                                                        dao=self.dao)

    def cancelOperation(self):
        """ Cancel current operation """
        self._slaTemplateObj.cancelOperation()

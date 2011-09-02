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
from promogest.ui.AnagraficaComplessaPrintPreview import AnagraficaPrintPreview

from promogest.ui.SendEmail import SendEmail
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda



class AnagraficaReport(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica
    """
    def __init__(self, anagrafica, description, defaultFileName,
                 htmlTemplate, sxwTemplate,
                templatesDir =None,
                ):
        self._anagrafica = anagrafica
        self.description = description
        self.defaultFileName = defaultFileName
        self._htmlTemplate = [os.path.join('report-templates'),htmlTemplate + '.html']

        self.objects = None
        self._slaTemplateObj = None


    def setObjects(self, objects):
        """ Imposta gli oggetti che verranno inclusi nel report """
        self.objects = objects

    def pdf(self,operationName, classic=None, template_file=None):
        """ Restituisce una stringa contenente il report in formato PDF
        """
        azienda = Azienda().getRecord(id=Environment.azienda)
        versione = scribusVersion(self._slaTemplate)
        if not Environment.new_print_enjine:
            if self._slaTemplateObj is None:
                self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                            pdfFolder=self._anagrafica._folder,
                                            report=self._anagrafica._reportType,
                                            classic = classic,
                                            template_file=template_file)

        param = []
        for d in self.objects:
            d.resolveProperties()
            param.append(d.dictionary(complete=True))
        multilinedirtywork(param)
        if azienda and param:
            azidict = azienda.dictionary(complete=True)
            for a,b in azidict.items():
                k = "azi_"+a
                azidict[k] = b
                del azidict[a]
            param[0].update(azidict)
        if not Environment.new_print_enjine:
            return self._slaTemplateObj.serialize(param, self.objects)
        else:
            return Sla2Pdf(slaFileName=self._slaTemplate,
                        pdfFolder=self._anagrafica._folder,
                        report=self._anagrafica._reportType).createPDF(objects=param, daos=self.objects)


    def cancelOperation(self):
        """ Cancel current operation
        """
        if self._slaTemplateObj is not None:
            self._slaTemplateObj.cancelOperation()


    def buildPreviewWidget(self, veter=False):
        """Build and return GladeWidget-derived component for print
        preview.
        """
        if veter:
            if "veter_" not in self._htmlTemplate[1]:
                self._htmlTemplate[1] = "veter_"+self._htmlTemplate[1]

        return AnagraficaPrintPreview(anagrafica=self._anagrafica,
                                      windowTitle=self.description,
                                      previewTemplate=self._htmlTemplate,
                                      )

# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import os
import os.path
from utils import *
from promogest import Environment
#if Environment.new_print_enjine:
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
#else:


from promogest.dao.Azienda import Azienda


class AnagraficaLabel(object):

    def __init__(self, anagrafica, description, defaultFileName,
                                                    htmlTemplate, sxwTemplate):
        """ Create labels """
        self._anagrafica = anagrafica
        self.description = description
        self.defaultFileName = defaultFileName
        self._htmlTemplate = os.path.join('label-templates', htmlTemplate \
                                                                + '.html')
        self._slaTemplate = Environment.labelTemplatesDir \
                                    + sxwTemplate \
                                    + '.sla'
        self.objects = None
        self._slaTemplateObj = None

    def setObjects(self, objects):
        """ Imposta gli oggetti che verranno inclusi nel report """
        self.objects = objects

    def pdf(self, operationName, classic=None, template_file=None):
        """ Restituisce una stringa contenente il report in formato PDF
        """
        azienda = Azienda().getRecord(id=Environment.azienda)
        param = []
        for d in self.objects:
            d.resolveProperties()
            param.append(d.dictionary(complete=True))
#        multilinedirtywork(param)
        if azienda:
            azidict = azienda.dictionary(complete=True)
            for a, b in azidict.items():
                k = "azi_" + a
                azidict[k] = b
                del azidict[a]
            if param:
                param[0].update(azidict)
        if template_file:
            scribusVersion(Environment.labelTemplatesDir + template_file)
        else:
            scribusVersion(self._slaTemplate)
        if not Environment.new_print_enjine:
            print "OLD PRINT ENGINE"
            self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                        pdfFolder=self._anagrafica._folder,
                                        report=self._anagrafica._reportType,
                                        label=True).serialize(
                                                param,
                                                self.objects,
                                                classic=classic,
                                                template_file=template_file)
            return self._slaTemplateObj
        else:
            print "NEW PRINT ENGINE"
            if template_file:
                slafile = Environment.labelTemplatesDir + template_file
            else:
                slafile = self._slaTemplate
            SlaTpl2Sla_ng(slafile=None, label=True,
                                    report=self._anagrafica._reportType,
                                    objects=param, daos=self.objects,
                                    slaFileName=slafile,
                                    pdfFolder=self._anagrafica._folder,
                                    classic=classic,
                                    template_file=template_file)
            return Sla2Pdf_ng(slafile=self._anagrafica._folder \
                                    + "_temppp.sla").translate()




#            return Sla2Pdf(slaFileName=self._slaTemplate,
#                            pdfFolder=self._anagrafica._folder,
#                            report=self._anagrafica._reportType,
#                            label=True).createPDF(objects=param,
#                                                    daos=self.objects,
#                                                classic = classic,
#                                                template_file=template_file)

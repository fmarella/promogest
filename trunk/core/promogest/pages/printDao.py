# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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

import datetime
from promogest.lib.page import Page
from promogest.lib.webutils import Response
from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Cliente import Cliente
from promogest.dao.Fornitore import Fornitore
from promogest.dao.Vettore import Vettore
from promogest.modules.Agenti.dao.Agente import Agente, getNuovoCodiceAgente
from promogest.dao.Fornitura import Fornitura
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Multiplo import Multiplo
import simplejson as json
#from promogest.lib.sla2pdf import SlaTpl2Sla_ng
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng


def printDao(req, dao=None):
    """
    Funzione di gestione delle preview
    """
    idr = req.args.get("idr")
    if dao== "articolo":
        daos = Articolo().getRecord(id =idr)
        filename = "articolo.sla"
    elif dao== "cliente":
        daos = Cliente().getRecord(id =idr)
        filename = "cliente.sla"
    elif dao== "fornitore":
        daos = Fornitore().getRecord(id =idr)
        filename = "fornitore.sla"
    elif dao== "vettore":
        daos = Vettore().getRecord(id =idr)
        filename = "vettore.sla"
    elif dao== "agente":
        daos = Agente().getRecord(id =idr)
        filename = "agente.sla"
    elif dao== "fornitura":
        daos = Fornitura().getRecord(id =idr)
        filename = "fornitura.sla"
    elif dao== "aliquota_iva":
        daos = AliquotaIva().getRecord(id =idr)
        filename = "aliquota_iva.sla"
    elif dao== "multiplo":
        daos = Multiplo().getRecord(id =idr)
        filename = "multiplo.sla"

    files = pdf(daos,template_file= filename)
    g = file("templates/pdfs/"+dao+".pdf", "wb")
    g.write(files)
    g.close()
    pageData = {'file' : 'download_pdf',
                "hf": "/templates/pdfs/"+dao+".pdf",
                "now": datetime.datetime.now()}
    return Page(req).render(pageData)




def pdf(dao,operationName=None, template_file=None):
    """ Qui si stampa selezione """
    # aggiungo i dati azienda al dao in modo che si gestiscano a monte
#    azienda = Azienda().getRecord(id=Environment.azienda)
#    operationNameUnderscored = operationName.replace(' ' , '_').lower()
#    print "PER LA STAMPA", operationNameUnderscored, Environment.templatesDir + operationNameUnderscored + '.sla'
#    if os.path.exists(Environment.templatesDir + operationNameUnderscored + '.sla'):
#        self._slaTemplate = Environment.templatesDir + operationNameUnderscored + '.sla'
#    else:
#        Environment.pg2log.info("UTILIZZO il documento.sla normale per la stampa")
#    _slaTemplate = Environment.templatesDir + self.defaultFileName + '.sla'
    """ Restituisce una stringa contenente il report in formato PDF """

    param = [dao.dictionary(complete=True)]
#    multilinedirtywork(param)

#    if azienda:
#        azidict = azienda.dictionary(complete=True)
#        for a,b in azidict.items():
#            k = "azi_"+a
#            azidict[k] = b
#            del azidict[a]
#        param[0].update(azidict)
    # controllo la versione dello sla che devo elaborare
#    versione = scribusVersion(self._slaTemplate)

#    if Environment.new_print_enjine:
    stpl2sla = SlaTpl2Sla_ng(slafile=None,label=None, report=None,
                            objects=param,
                            daos=dao,
                            slaFileName="templates_print/"+template_file,
                            pdfFolder="cache/",
                            classic=True,
                            template_file=template_file).fileElaborated()
    return Sla2Pdf_ng(slafile=stpl2sla).translate()

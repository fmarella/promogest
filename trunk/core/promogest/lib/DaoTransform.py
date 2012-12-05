# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import PyPDF2
from calendar import Calendar
import os
import glob
import tempfile
from promogest import Environment
from promogest.lib.utils import *
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
from promogest.lib.HtmlHandler import renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda


def _to_pdf(dao, classic=None, template_file=None):

    operationName = dao.operazione

    operationNameUnderscored = operationName.replace(' ', '_').lower()

    _slaTemplate = None
    _slaTemplateObj = None

    # aggiungo i dati azienda al dao in modo che si gestiscano a monte
    azienda = Azienda().getRecord(id=Environment.azienda)

    if os.path.exists(Environment.templatesDir + operationNameUnderscored + '.sla'):
        _slaTemplate = Environment.templatesDir + operationNameUnderscored + '.sla'
    elif "DDT" in operationName and \
                    os.path.exists(Environment.templatesDir + 'ddt.sla'):
        _slaTemplate = Environment.templatesDir + 'ddt.sla'
    else:
        _slaTemplate = Environment.templatesDir + 'documento.sla'
    """ Restituisce una stringa contenente il report in formato PDF """

    if dao.__class__.__name__ in Environment.fromHtmlLits:
        from  xhtml2pdf import pisa
        #f = self.hh
        g = file(Environment.tempDir + ".temp.pdf", "wb")
        pisa.CreatePDF(str(f), g)
        g.close()
        g = file(Environment.tempDir + ".temp.pdf", "r")
        f = g.read()
        g.close()
        return f

    param = [dao.dictionary(complete=True)]

    multilinedirtywork(param)

    try:
        if hasattr(Environment.conf.Documenti, "jnet"):
            from promogest.modules.NumerazioneComplessa.jnet import\
                                                         numerazioneJnet
            param[0]["numero"] = numerazioneJnet(dao)
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

    _anagrafica_folder = tempfile.gettempdir() + os.sep

    stpl2sla = SlaTpl2Sla_ng(slafile=None, label=None, report=None,
                            objects=param,
                            daos=dao,
                            slaFileName=_slaTemplate,
                            pdfFolder=_anagrafica_folder,
                            classic=True,
                            template_file=None).fileElaborated()
    return Sla2Pdf_ng(slafile=stpl2sla).translate()

def to_pdf(daos, output, anag=None):
    PDF_WORKING_DIR = tempfile.mkdtemp()
    i = 1
    if anag:
        anag.pbar_anag_complessa.show()
    #from operator import attrgetter
    #daos = sorted(daos, key=attrgetter('operazione', 'numero'), reverse=True)
    #daos.sort(key=lambda x: x.intestatario.strip().upper())
    for dao in daos:
        print "D", dao.intestatario
        if anag:
            pbar(anag.pbar_anag_complessa,parziale=daos.index(dao), totale=len(daos), text="GEN STAMPE MULTIPLE", noeta=False)
        if dao.__class__.__name__ == 'TestataDocumento':
            dao.totali

        with file(os.path.join(PDF_WORKING_DIR, '%s.pdf'% str(int(i)+10000)), 'wb') as f:
            f.write(_to_pdf(dao))
        i += 1

    merger = PyPDF2.PdfFileMerger()
    filesPdf = glob.glob(os.path.join(PDF_WORKING_DIR, '*.pdf'))
    filesPdf.sort()
    for infile in filesPdf:
        if anag:
            pbar(anag.pbar_anag_complessa,parziale=filesPdf.index(infile), totale=len(filesPdf), text="UNIONE PDF", noeta=False)
        merger.append(fileobj=file(infile, 'rb'))

    merger.write(output)
    merger.close()
    if anag:
        pbar(anag.pbar_anag_complessa,stop=True)
        anag.pbar_anag_complessa.set_property("visible",False)

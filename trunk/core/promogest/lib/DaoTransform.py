# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
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

from  promogest.lib.PyPDF2 import *
import os
import glob
import tempfile
from promogest import Environment
from  promogest.lib import utils
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.dao.Azienda import Azienda

from jinja2 import Environment as Env
from jinja2 import FileSystemLoader,FileSystemBytecodeCache,environmentfilter, Markup, escape


def dateformat(value, format='%Y/%m/%d'):
    if not value:
        return ""
    else:
        return value.strftime(format)

def noNone(value):
    if value =="None":
        return ""
    elif not value:
        return ""
    else:
        return value

def renderFatturaPA(pageData):
    env = Env(loader=FileSystemLoader([os.path.join('fattura_pa_template')]),
              trim_blocks=True,
              lstrip_blocks=True)
    env.filters['dateformat'] = dateformat
    env.filters['nonone'] = noNone
    env.globals['utils'] = utils
    print pageData
    return env.get_template('/' + 'fatturapa_template.xml').render(pageData = pageData,
        dao = pageData['dao'],
        progressivo = pageData['progressivo'],
        trasmittente = pageData['trasmittente'],
        trasmissione = pageData['trasmissione'],
        prestatore = pageData['prestatore'],
        organizzazione = pageData['organizzazione'],
        committente = pageData['committente'],
        soggetto_emittente = pageData['soggetto_emittente'])

def to_fatturapa(daos, output, anag=None):
    if anag:
        anag.pbar_anag_complessa.show()
    progressivo = 1
    for dao in daos:
        if anag:
            utils.pbar(anag.pbar_anag_complessa,parziale=daos.index(dao), totale=len(daos), text="GEN FatturePA MULTIPLE", noeta=False)
        if dao.__class__.__name__ == 'TestataDocumento':
            dao.totali
            azienda = Azienda().getRecord(id=Environment.azienda)
            # Riempiamo la fattura elettronica
            pageData = {}
            pageData['dao'] = dao
            pageData['codice_trasmittente'] = azienda.codice_fiscale
            # campi di trasmissione
            pageData['trasmissione'] = {
                'progressivo': progressivo,
                'formato_trasmissione': '11',
                'codice_destinatario': 'codice ufficio'
            }
            pageData['cedente'] = {
                'partita_iva': '',
                'denominazione': 'denominazione ditta',
                'nome': '',
                'cognome': '',
                'regime_fiscale': '',
                'sede_indirizzo': '',
                'sede_numero_civico': '',
                'sede_cap': '',
                'sede_comune': '',
                'sede_provincia': '',
                'sede_nazione': '',
                'stabile_indirizzo': '',
                'stabile_numero_civico': '',
                'stabile_cap': '',
                'stabile_comune': '',
                'stabile_provincia': '',
                'stabile_nazione': '',
                'iscrizioneREA_numeroREA': '',
                'iscrizioneREA_ufficio': '',
                'capitale_sociale': '',
                'socio_unico': '',
                'liquidazione': ''
            }

            pageData['committente'] = {
                'partita_iva': '',
                'codice_fiscale': '',
                'denominazione': 'denominazione ditta',
                'nome': '',
                'cognome': '',
                'sede_indirizzo': '',
                'sede_numero_civico': '',
                'sede_cap': '',
                'sede_comune': '',
                'sede_provincia': '',
                'sede_nazione': '',
            }

            pageData['soggetto_emittente'] = ''

            xml = renderFatturaPA(pageData)
            with open(os.path.join(os.path.dirname(output), 'output_fattura_pa.xml'), 'w') as out:
                out.write(xml)
            progressivo += 1
    if anag:
        utils.pbar(anag.pbar_anag_complessa,stop=True)
        anag.pbar_anag_complessa.set_property("visible",False)


def _to_pdf(dao, classic=None, template_file=None):

    operationName = dao.operazione

    operationNameUnderscored = operationName.replace(' ', '_').lower()

    _slaTemplate = None

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

    utils.multilinedirtywork(param)

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
    for dao in daos:
        if anag:
            utils.pbar(anag.pbar_anag_complessa,parziale=daos.index(dao), totale=len(daos), text="GEN STAMPE MULTIPLE", noeta=False)
        if dao.__class__.__name__ == 'TestataDocumento':
            dao.totali

        with file(os.path.join(PDF_WORKING_DIR, '%s.pdf'% str(int(i)+10000)), 'wb') as f:
            f.write(_to_pdf(dao))
        i += 1

    merger = PdfFileMerger()
    filesPdf = glob.glob(os.path.join(PDF_WORKING_DIR, '*.pdf'))
    filesPdf.sort()
    for infile in filesPdf:
        if anag:
            utils.pbar(anag.pbar_anag_complessa,parziale=filesPdf.index(infile), totale=len(filesPdf), text="UNIONE PDF", noeta=False)
        merger.append(fileobj=file(infile, 'rb'))

    merger.write(output)
    merger.close()
    if anag:
        utils.pbar(anag.pbar_anag_complessa,stop=True)
        anag.pbar_anag_complessa.set_property("visible",False)

import time
try:
    import keyring
except:
    keyring = None
import smtplib
from os.path import basename
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from promogest.Environment import session, azienda
from promogest.lib.utils import resolve_save_file_path
from promogest.dao.AccountEmail import AccountEmail

class NoAccountEmailFound(Exception): pass
class NetworkError(Exception): pass

def do_send_mail(daos, anag=None):
    if anag:
        anag.pbar_anag_complessa.show()
    # recupera informazioni account posta elettronica
    try:
        account_email = session.query(AccountEmail).filter_by(id_azienda=azienda, preferito=True).one()
    except: # NoResultFound
        raise NoAccountEmailFound("Nessun account email configurato")

    password = ''
    if keyring:
        password = keyring.get_password('promogest2', account_email.username)
    else:
        from promogest.lib.utils import inputPasswordDialog
        password = inputPasswordDialog()

    s = None
    if account_email.cripto_SSL:
        try:
            s = smtplib.SMTP_SSL(account_email.server_smtp, port=account_email.porta_smtp)
            time.sleep(1)
            s.login(account_email.username, password or '')
        except:
            raise NetworkError('Errore di connessione al server di posta in uscita.')
    else:
        try:
            s = smtplib.SMTP(account_email.server_smtp)
            time.sleep(1)
            s.starttls()
            time.sleep(1)
            s.login(account_email.username, password or '')
        except:
            raise NetworkError('Errore di connessione al server di posta in uscita.')
    del password

    for dao in daos:
        if not dao.id_cliente:
            continue

        # recupera email destinatario
        destinatario = dao.CLI.email_pec or dao.CLI.email_principale
        if not destinatario:
            continue

        if anag:
            utils.pbar(anag.pbar_anag_complessa,
                 parziale=daos.index(dao), totale=len(daos),
                 text="INVIO EMAIL MULTIPLO", noeta=False)

        # genera il documento in formato pdf
        path = resolve_save_file_path()
        fp = open(path, 'wb')
        fp.write(_to_pdf(dao))
        fp.close()
        # prepara il messaggio email con allegato
        outer = MIMEMultipart()
        outer.set_charset('UTF-8')
        outer['Subject'] = account_email.oggetto
        outer['To'] = formataddr((destinatario, destinatario))
        outer['From'] = formataddr((account_email.indirizzo, account_email.indirizzo))
        ctype, encoding = mimetypes.guess_type(path)
        maintype, subtype = ctype.split('/', 1)
        fp = open(path, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=basename(path))
        outer.attach(msg)
        text_msg = MIMEText(account_email.body + '\n' + account_email.firma)
        outer.attach(text_msg)
        try:
            s.sendmail(account_email.indirizzo, [destinatario], outer.as_string())
        except:
            raise NetworkError('Invio fattura a "{0}" non riuscito.'.format(destinatario))
        time.sleep(5)
    if s:
        s.quit()
    if anag:
        utils.pbar(anag.pbar_anag_complessa, stop=True)
        anag.pbar_anag_complessa.set_property("visible", False)

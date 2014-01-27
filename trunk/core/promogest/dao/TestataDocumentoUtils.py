# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


from decimal import Decimal
from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Fornitore import Fornitore
from promogest.dao.Cliente import Cliente
from promogest.modules.Provvigione.dao.ProvvPgAzArt import ProvvPgAzArt
from promogest.lib.utils import *
import datetime


def do_genera_fatture_provvigioni(data_da, data_a, data_doc, progress=None):
    '''
    '''
    documenti = TestataDocumento().select(complexFilter=(and_(TestataDocumento.operazione=='DDT vendita diretto',
            TestataDocumento.data_documento.between(data_da, data_a))),
        batchSize=None,
        orderBy=TestataDocumento.id_fornitore)

    if not documenti:
        messageInfo(msg="Non sono stati trovati documenti utili a completare l'operazione.")
    else:
        forn_totaledoc_dict = {}
        totaleProvv = Decimal(0)
        for doc in documenti:

            if progress:
                pbar(progress, parziale=documenti.index(doc), totale=len(documenti), text="Elaborazione documenti...", noeta=False)

            totaleProvvDoc = Decimal(0)
            for riga in doc.righe:
                p = ProvvPgAzArt().select(id_persona_giuridica_to=doc.id_fornitore,
                                          id_persona_giuridica_from=doc.id_cliente,
                                          id_articolo=riga.id_articolo)
                if p:
                    if p[0].provv.tipo_provv == "%":
                        totaleProvvRiga = riga.totaleRiga * p[0].provv.valore_provv / 100
                    else:
                        totaleProvvRiga = riga.quantita * p[0].provv.valore_provv
                else:
                    p = ProvvPgAzArt().select(id_persona_giuridica_to=doc.id_fornitore,
                                              id_persona_giuridica_from=doc.id_cliente,
                                              id_articolo=None)
                    if p[0].provv.tipo_provv == "%":
                        totaleProvvRiga = riga.totaleRiga * p[0].provv.valore_provv / 100
                    else:
                        totaleProvvRiga = riga.quantita * p[0].provv.valore_provv

                totaleProvvDoc += totaleProvvRiga
            if doc.id_fornitore not in forn_totaledoc_dict:
                forn_totaledoc_dict[doc.id_fornitore] = totaleProvvDoc
            else:
                forn_totaledoc_dict[doc.id_fornitore] += totaleProvvDoc

            totaleProvv += totaleProvvDoc

        operazione = "Fattura vendita"

        DESCR_RIGA = """Come convenuto Vi addebitiamo per nostre provvigioni su Vostre
forniture effettuate nel mese di %s l'importo di



FUORI CAMPO IVA ARTICOLO 7 ter D.P.R. 633/72""" % data_da.strftime('%B %Y')

        i = 0
        flag = False
        for k,v in forn_totaledoc_dict.iteritems():

            if pbar:
                pbar(progress, parziale=i, totale=len(forn_totaledoc_dict), text="Creazione fatture...", noeta=False)

            forn = Fornitore().getRecord(id=k)
            if forn.ragione_sociale:
                cli = Cliente().select(ragioneSociale=forn.ragione_sociale)

            if not cli and forn.cognome and forn.nome:
                cli = Cliente().select(cognomeNome=forn.cognome + ' ' + forn.nome)

            if not cli:
                flag = True
                continue

            td = TestataDocumento()
            td.data_documento = data_doc
            td.operazione = operazione
            td.id_cliente = cli[0].id
            daoRiga = RigaDocumento()
            daoRiga.posizione = 0
            daoRiga.descrizione = DESCR_RIGA
            daoRiga.quantita = 1.0
            daoRiga.percentuale_iva = 0
            daoRiga.valore_unitario_lordo = v
            daoRiga.moltiplicatore = 1
            daoRiga.valore_unitario_netto = v
            daoRiga.scontiRigaDocumento = []
            td.righeDocumento = [daoRiga]
            td.persist()

            i += 1

        if progress:
            pbar(progress, stop=True)
        if flag:
            messageWarning(msg="Non è stato possibile creare alcune fatture!")
        messageInfo(msg="Operazione completata, sono state create %d nuove fatture." % i)

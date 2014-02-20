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

import os
from promogest.Environment import tempDir
from promogest.lib.utils import leggiFornitore, leggiCliente
import re

TIPO_DATA_DOC = 0
TIPO_DATA_SPED = 1

def do_genera_fatture_provvigioni(tipo_data, data_da, data_a, data_doc, progress=None):
    '''
    '''

    # definisco gli articoli da escludere
    articoli_esclusi = r"(.*)(sacchi|trasporto|contributo energetico|riempimento|commissioni|cappucci|europalette|big bag)(.*)"

    documenti = []

    if tipo_data == TIPO_DATA_DOC:
        documenti = TestataDocumento().select(complexFilter=(and_(TestataDocumento.operazione=='DDT vendita diretto',
                TestataDocumento.data_documento.between(data_da, data_a))),
            batchSize=None,
            orderBy=TestataDocumento.id_fornitore)
    if tipo_data == TIPO_DATA_SPED:
        documenti = TestataDocumento().select(complexFilter=(and_(TestataDocumento.operazione=='DDT vendita diretto',
                TestataDocumento.fine_trasporto.between(data_da, data_a))),
            batchSize=None,
            orderBy=TestataDocumento.id_fornitore)

    if not documenti:
        messageInfo(msg="Non sono stati trovati documenti utili a completare l'operazione.")
    else:
        forn_totaledoc_dict = {}
        forn_provv_file = file(os.path.join(tempDir, 'riepilogo_provv.csv'), 'w')
        forn_provv_file.write('docNum;fornitore;cliente;articolo;totaleRiga;qta;tipo_provv;valore_provv;provv_articolo\n')
        for doc in documenti:
            if progress:
                pbar(progress, parziale=documenti.index(doc), totale=len(documenti), text="Elaborazione documenti...", noeta=False)
            totaleProvvDoc = Decimal(0)
            for riga in doc.righe:
                if riga.id_articolo is None or leggiArticolo(riga.id_articolo)['denominazione'] == '':
                    continue
                if re.match(articoli_esclusi, leggiArticolo(riga.id_articolo)['denominazione'], flags=re.IGNORECASE):
                    continue
                if Decimal(riga.totaleRiga) == Decimal(0) or Decimal(riga.quantita) == Decimal(0):
                    continue
                p = ProvvPgAzArt().select(id_persona_giuridica_to=doc.id_fornitore,
                                          id_persona_giuridica_from=doc.id_cliente,
                                          id_articolo=riga.id_articolo, batchSize=None)
                if p:
                    if p[0].provv.tipo_provv == "%":
                        provv_row = riga.totaleRiga * p[0].provv.valore_provv / 100
                    else:
                        provv_row = riga.quantita * p[0].provv.valore_provv
                    forn_provv_file.write("%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (doc.numero,
                        leggiFornitore(doc.id_fornitore)['ragioneSociale'],
                        leggiCliente(doc.id_cliente)['ragioneSociale'],
                        leggiArticolo(riga.id_articolo)['denominazione'],
                        mN(riga.totaleRiga, 2),
                        riga.quantita,
                        p[0].provv.tipo_provv,
                        mN(p[0].provv.valore_provv, 2),
                        mN(provv_row, 2)))
                    if doc.id_fornitore not in forn_totaledoc_dict:
                        forn_totaledoc_dict[doc.id_fornitore] = provv_row
                    else:
                        forn_totaledoc_dict[doc.id_fornitore] += provv_row
                else:
                    q = ProvvPgAzArt().select(id_persona_giuridica_to=doc.id_fornitore,
                                              id_persona_giuridica_from=doc.id_cliente,
                                              id_articolo=None, batchSize=None)
                    if q:
                        if q[0].provv.tipo_provv == "%":
                            provv_row = riga.totaleRiga * q[0].provv.valore_provv / 100
                        else:
                            provv_row = riga.quantita * q[0].provv.valore_provv
                        forn_provv_file.write("%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (doc.numero,
                            leggiFornitore(doc.id_fornitore)['ragioneSociale'],
                            leggiCliente(doc.id_cliente)['ragioneSociale'],
                            leggiArticolo(riga.id_articolo)['denominazione'],
                            mN(riga.totaleRiga, 2),
                            riga.quantita,
                            q[0].provv.tipo_provv,
                            mN(q[0].provv.valore_provv, 2),
                            mN(provv_row, 2)))
                        if doc.id_fornitore not in forn_totaledoc_dict:
                            forn_totaledoc_dict[doc.id_fornitore] = provv_row
                        else:
                            forn_totaledoc_dict[doc.id_fornitore] += provv_row

        forn_provv_file.close()

        operazione = "Fattura vendita"

        DESCR_RIGA = """Come convenuto Vi addebitiamo per nostre provvigioni su Vostre
forniture effettuate nel mese di %s l'importo di



FUORI CAMPO IVA ARTICOLO 7 ter D.P.R. 633/72""" % data_da.strftime('%B %Y')

        i = 0
        flag = False
        for k in forn_totaledoc_dict:

            if pbar:
                pbar(progress, parziale=i, totale=len(forn_totaledoc_dict), text="Creazione fatture...", noeta=False)

            forn = Fornitore().getRecord(id=k)
            if forn.ragione_sociale:
                cli = Cliente().select(ragioneSociale=forn.ragione_sociale, batchSize=None)

            if not cli and forn.cognome and forn.nome:
                cli = Cliente().select(cognomeNome=forn.cognome + ' ' + forn.nome, batchSize=None)

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
            daoRiga.valore_unitario_lordo = forn_totaledoc_dict[k]
            daoRiga.moltiplicatore = 1
            daoRiga.valore_unitario_netto = forn_totaledoc_dict[k]
            daoRiga.scontiRigaDocumento = []
            td.righeDocumento = [daoRiga]
            td.persist()

            i += 1

        if progress:
            pbar(progress, stop=True)
        if flag:
            messageWarning(msg="Non è stato possibile creare alcune fatture!")
        messageInfo(msg="Operazione completata, sono state create %d nuove fatture." % i)

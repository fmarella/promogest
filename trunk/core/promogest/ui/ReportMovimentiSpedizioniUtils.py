# -*- coding: utf-8 -*-

# Copyright (C) 2005-2014 by Promotux
# di Francesco Meloni snc - http://www.promotux.it/

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

from decimal import Decimal as D
import datetime
from promogest.dao.StoricoDocumento import get_padre, get_figli
from promogest.lib.utils import pbar
from promogest.dao.Operazione import Operazione
from promogest.Environment import session, workingYear
from promogest.dao.TestataDocumento import TestataDocumento


def controlla_quantita(ordine):

    # costruisco un dizionario con gli id articolo e le quantità richieste per ciascun articolo
    qta_ordine = {}

    tipo = Operazione().getRecord(id=ordine.operazione)
    if tipo.segno != '' and tipo.segno is not None:
        tipoDOC = "MOV"
    else:
        tipoDOC = "DOC"

    for r in ordine.righe:
        if (tipoDOC == "MOV" and r.id_articolo == None) or tipoDOC == "DOC":
            continue
        else:
            # riga movimento
            qta_ordine[r.id_articolo] = r.quantita

    # raccolgo le quantità già inserite nei precedenti DDT
    qta_richieste = {}
    objs_figli = get_figli(ordine.id)
    for figlio in objs_figli:
        if figlio.operazione not in ['DDT vendita', 'DDT vendita diretta']:
            continue
        for r in figlio.righe:
            if r.id_articolo not in qta_richieste.keys():
                qta_richieste[r.id_articolo] = r.quantita
            else:
                qta_richieste[r.id_articolo] += r.quantita

    posso_chiudere = True
    for k in qta_ordine:
        tmpp = D(qta_ordine[k] - qta_richieste[k])
        if tmpp > D(3) or tmpp < D(-3):
            posso_chiudere = False

    return posso_chiudere

def chiusura_ordini(progress=None):
    da_data = datetime.date(int(workingYear), 1, 1)
    ordini = session.query(TestataDocumento).filter(TestataDocumento.data_documento >= da_data,
                                                    TestataDocumento.operazione == 'Ordine da cliente',
                                                    TestataDocumento.documento_saldato == False).all()

    for doc in ordini:
        if controlla_quantita(doc):
            # controllo delle quantità tra ordine e DDT
            # quelle del DDT >= or < qta +3 quelle dell'ordine
            doc.totale_pagato = doc.totale_sospeso
            doc.totale_sospeso = 0
            doc.documento_saldato = True
            session.commit()
            self.filter.refresh()
        if progress:
            pbar(progress, parziale=ordini.index(doc), totale=len(ordini), text="Attendere...", noeta=True)

    if progress:
        pbar(progress, stop=True)
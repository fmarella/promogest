# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@gmail.com>

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
from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.TestataMovimento import TestataMovimento

(
    MOVIMENTI_VENDITA,
    MOVIMENTI_ACQUISTO,
    MOVIMENTI_ACQUISTO_VENDITA
) = range(3)

def ricerca_forniture_lotti(fornitore, daData, aData, tipoMovimento=None, progress=None):
    res = {}

    if not fornitore:
        return None

    idFornitore = fornitore.id
    
    forniture = Fornitura().select(idFornitore=idFornitore,
        daDataFornitura=daData,
        aDataFornitura=aData,
        batchSize=None)

    tot_a = 0
    tot_v = 0
    for fornitura in forniture:

        righe_mf = RigaMovimentoFornitura().select(idFornitura=fornitura.id)

        mov_ven = [riga_mf.rigamovven for riga_mf in righe_mf if riga_mf.rigamovven]
        mov_acq = [riga_mf.rigamovacq for riga_mf in righe_mf if riga_mf.rigamovacq]

        for riga_mov in mov_acq:
            if not riga_mov:
                continue
            tot_a += riga_mov.totaleRiga

        for riga_mov in mov_ven:
            if not riga_mov:
                continue
            tot_v += riga_mov.totaleRiga

        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=forniture.index(fornitura), totale=len(forniture),
                text="Attendere...", noeta=True)

    return {'diz_acquisto': None,
            'diz_vendita': None,
            'totale_acquisto': tot_a,
            'totale_vendita': tot_v}


def ricerca_forniture(fornitore, dataInizio, dataFine, tipoMovimento=None, progress=None):
    # %tipo movimento => {%id articolo => (%quantità, %totale)}
    res_acquisto = {}
    res_vendita = {}
    tot_a = 0
    tot_v = 0

    if not fornitore:
        return None

    tmovs = TestataMovimento().select(idFornitore=fornitore.id,
                                     daData=dataInizio,
                                     aData=dataFine,
                                     idOperazione="DDT acquisto",
                                     batchSize=None)

    for tm in tmovs:
        for rm in tm.rigamov:
            if str(rm.rig.id_articolo) not in res_acquisto:
                res_acquisto.update({str(rm.rig.id_articolo): (rm.rig.quantita * rm.rig.moltiplicatore, rm.totaleRiga)})
            else:
                r = res_acquisto[str(rm.rig.id_articolo)]
                res_acquisto[str(rm.rig.id_articolo)] = (r[0] + rm.rig.quantita * rm.rig.moltiplicatore,
                                                         r[1] + rm.totaleRiga)
            tot_a += rm.totaleRiga

        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=tmovs.index(tm), totale=len(tmovs),
                text="Controllo documenti acquisto...", noeta=True)

    tmovs = TestataMovimento().select(idArticolo=res_acquisto.keys(),
                                      daData=dataInizio,
                                      aData=dataFine,
                                      idOperazione="DDT vendita",
                                      batchSize=None)

    for tm in tmovs:
        for rm in tm.rigamov:
            if str(rm.rig.id_articolo) not in res_vendita:
                res_vendita.update({str(rm.rig.id_articolo): (rm.rig.quantita * rm.rig.moltiplicatore, rm.totaleRiga)})
            else:
                r = res_vendita[str(rm.rig.id_articolo)]
                res_vendita[str(rm.rig.id_articolo)] = (r[0] + rm.rig.quantita * rm.rig.moltiplicatore,
                                                         r[1] + rm.totaleRiga)
            tot_v += rm.totaleRiga

        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=tmovs.index(tm), totale=len(tmovs),
                text="Controllo documenti vendita...", noeta=True)

    return {'diz_acquisto': res_acquisto,
            'diz_vendita': res_vendita,
            'totale_acquisto': tot_a,
            'totale_vendita': tot_v}

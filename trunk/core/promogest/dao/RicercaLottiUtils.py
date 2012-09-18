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
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento


def ricerca_lotto(numero_lotto, anno, progress=None):
    lista_fornitori = []
    
    forniture = Fornitura().select(numeroLotto=numero_lotto,
        daDataFornitura=datetime.datetime(anno, 1, 1),
        aDataFornitura=datetime.datetime.now(),
        batchSize=None)

    docs = []

    for fornitura in forniture:

        righe_mf = RigaMovimentoFornitura().select(idFornitura=fornitura.id)

        righe_mov_acq = [riga_mf.rigamovacq for riga_mf in righe_mf if riga_mf.rigamovacq]
        righe_mov_ven = [riga_mf.rigamovven for riga_mf in righe_mf if riga_mf.rigamovven]

        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=forniture.index(fornitura), totale=len(forniture),
                text="Attendere...", noeta=True)

        for riga_mov in righe_mov_acq:
            if not riga_mov:
                continue
            tm = TestataMovimento().getRecord(id=riga_mov.id_testata_movimento)
            if tm:
                if tm.TD and tm.TD not in docs:
                    docs.append(tm.TD)

        for riga_mov in righe_mov_ven:
            if not riga_mov:
                continue
            tm = TestataMovimento().getRecord(id=riga_mov.id_testata_movimento)
            if tm:
                if tm.TD and tm.TD not in docs:
                    docs.append(tm.TD)

    docs.extend(ricerca_in_lottotemp(numero_lotto))

    lista_fornitori.append({'data_fornitura': fornitura.data_fornitura,
                'fornitore': fornitura.forni, 'docs': docs})
    return lista_fornitori

def ricerca_in_lottotemp(numero_lotto):
    nltemps = NumeroLottoTemp().select(lottoTemp=numero_lotto)

    docs = []
    for nltemp in nltemps:
        tm = TestataMovimento().getRecord(id=nltemp.rigamovventemp.id_testata_movimento)
        if tm:
            if tm.TD and tm.TD not in docs:
                docs.append(tm.TD)
    return docs
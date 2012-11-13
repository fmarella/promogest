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

(
    MOVIMENTI_VENDITA,
    MOVIMENTI_ACQUISTO,
    MOVIMENTI_ACQUISTO_VENDITA
) = range(3)

def ricerca_forniture(fornitore, daData, aData, tipoMovimento=None, progress=None):
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

    return tot_a, tot_v
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

from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento


def ricerca_lotto(numero_lotto):
    lista_fornitori = []
    forniture = Fornitura().select(numeroLotto=numero_lotto, batchSize=None)
    for fornitura in forniture:

        righe_mf = RigaMovimentoFornitura().select(idFornitura=fornitura.id)
        righe_mov = [riga_mf.rigamovven or riga_mf.rigamovacq for riga_mf in righe_mf]

        docs = []
        for riga_mov in righe_mov:
            if not riga_mov:
                continue
            tm = TestataMovimento().getRecord(id=riga_mov.id_testata_movimento)
            if tm:
                td = TestataDocumento().getRecord(id=tm.id_testata_documento)
                if td:
                    docs.append(td)

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
            td = TestataDocumento().getRecord(id=tm.id_testata_documento)
            if td:
                docs.append(td)
    return docs
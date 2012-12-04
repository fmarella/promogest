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
from promogest.Environment import session
from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga


def ricerca_forniture_lotti(fornitore, daData, aData, progress=None):
    data = {}

    if not fornitore:
        return None

    forniture = Fornitura().select(idFornitore=fornitore.id,
        daDataFornitura=daData,
        aDataFornitura=aData,
        batchSize=None)

    tot_a = 0
    tot_v = 0
    totale_qta_acq = 0
    totale_qta_ven = 0
    for fornitura in forniture:

        righe_mf = RigaMovimentoFornitura().select(idFornitura=fornitura.id)

        mov_acq = [riga_mf.rigamovacq for riga_mf in righe_mf if riga_mf.rigamovacq]

        for riga_mov in mov_acq:
            if not riga_mov:
                continue
            id_articolo = riga_mov.rig.id_articolo
            if str(id_articolo) not in data:
                data[str(id_articolo)] = {'QTAACQ': riga_mov.rig.quantita * riga_mov.rig.moltiplicatore,
                                         'TOTACQ': riga_mov.totaleRiga,
                                         'DAO_ART': riga_mov.rig.arti,
                                         'DAO_RIGAMOV': riga_mov,
                                         'QTAVEN': 0, 'TOTVEN': 0}
            else:
                data[str(id_articolo)]['QTAACQ'] += riga_mov.rig.quantita * riga_mov.rig.moltiplicatore
                data[str(id_articolo)]['TOTACQ'] += riga_mov.totaleRiga
            tot_a += riga_mov.totaleRiga
            totale_qta_acq += riga_mov.rig.quantita * riga_mov.rig.moltiplicatore

        mov_ven = [riga_mf.rigamovven for riga_mf in righe_mf if riga_mf.rigamovven]

        for riga_mov in mov_ven:
            if not riga_mov:
                continue
            id_articolo = riga_mov.rig.id_articolo
            if str(id_articolo) not in data:
                data[str(id_articolo)] = {'QTAVEN': riga_mov.rig.quantita * riga_mov.rig.moltiplicatore,
                                         'TOTVEN': riga_mov.totaleRiga,
                                         'DAO_ART': riga_mov.rig.arti,
                                         'DAO_RIGAMOV': riga_mov,
                                         'QTAACQ': 0, 'TOTACQ': 0}
            else:
                data[str(id_articolo)]['QTAVEN'] += riga_mov.rig.quantita * riga_mov.rig.moltiplicatore
                data[str(id_articolo)]['TOTVEN'] += riga_mov.totaleRiga
            tot_v += riga_mov.totaleRiga
            totale_qta_ven += riga_mov.rig.quantita * riga_mov.rig.moltiplicatore

        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=forniture.index(fornitura), totale=len(forniture),
                text="Attendere...", noeta=True)

    return data, {'totale_qta_acq': totale_qta_acq,
            'totale_qta_ven': totale_qta_ven,
            'totale_ven': tot_v,
            'totale_acq': tot_a}

def ricerca_forniture(fornitore, dataInizio, dataFine, progress=None):
    if not (fornitore or dataInizio or dataFine):
        return None

    data = {}
    totale_acq = 0
    totale_ven = 0
    totale_qta_acq = 0
    totale_qta_ven = 0

    id_articoli_forniture = session.query(Fornitura.id_articolo) \
            .distinct(Fornitura.id_articolo) \
            .filter(Fornitura.id_fornitore==fornitore.id) \
            .all()

    for id_articol in id_articoli_forniture:
        id_articolo = id_articol[0]
        res = session.query(Riga, RigaMovimento, TestataMovimento) \
                .join(RigaMovimento, TestataMovimento) \
                .filter(Riga.id_articolo==id_articolo) \
                .filter(TestataMovimento.data_movimento.between(dataInizio, dataFine + datetime.timedelta(days=1))) \
                .all()

        for item in res:
            riga, rigamov, testmov = item
            if testmov.id_fornitore and testmov.id_cliente:
                continue
            elif testmov.id_fornitore:
                if str(id_articolo) not in data:
                    data[str(id_articolo)] = {'QTAACQ': riga.quantita * riga.moltiplicatore,
                                             'TOTACQ': rigamov.totaleRiga,
                                             'DAO_ART': riga.arti,
                                             'DAO_RIGAMOV': rigamov,
                                             'QTAVEN': 0, 'TOTVEN': 0}
                else:
                    data[str(id_articolo)]['QTAACQ'] += riga.quantita * riga.moltiplicatore
                    data[str(id_articolo)]['TOTACQ'] += rigamov.totaleRiga
                totale_acq += rigamov.totaleRiga
                totale_qta_acq += riga.quantita * riga.moltiplicatore

            elif testmov.id_cliente:
                if str(id_articolo) not in data:
                    data[str(id_articolo)] = {'QTAVEN': riga.quantita * riga.moltiplicatore,
                                             'TOTVEN': rigamov.totaleRiga,
                                             'DAO_ART': riga.arti,
                                             'DAO_RIGAMOV': rigamov,
                                             'QTAACQ': 0, 'TOTACQ': 0}
                else:
                    data[str(id_articolo)]['QTAVEN'] += riga.quantita * riga.moltiplicatore
                    data[str(id_articolo)]['TOTVEN'] += rigamov.totaleRiga
                totale_ven += rigamov.totaleRiga
                totale_qta_ven += riga.quantita * riga.moltiplicatore


        if progress:
            from promogest.lib.utils import pbar
            pbar(progress, parziale=id_articoli_forniture.index(id_articol),
                totale=len(id_articoli_forniture),
                text="Controllo documenti...", noeta=True)

    return data, {'totale_qta_acq': totale_qta_acq,
            'totale_qta_ven': totale_qta_ven,
            'totale_ven': totale_ven,
            'totale_acq': totale_acq}

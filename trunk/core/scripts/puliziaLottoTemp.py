#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

import sys
import os
path = ".."
if path not in sys.path:
    sys.path.append(path)

from promogest import preEnv
preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "urbani"
from promogest.Environment import params  , session , azienda
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.lib.utils import stringToDateTime, timeit
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.dao.Fornitura import Fornitura

@timeit
def pulizia_lottotemp():
    #ltemp = setconf("Documenti", "lotto_temp")
    #if not ltemp:
        #return
    print "Avvio pulizia lotti temp..."
    lt = NumeroLottoTemp().select(batchSize=None)
    n = len(lt)
    g = 0
    for l in lt:
        print "RESIDUI DA ELABORARE", n-lt.index(l)
        rmf =  RigaMovimentoFornitura().select(idRigaMovimentoVendita=l.id_riga_movimento_vendita_temp)
        if not rmf:
            #cerchiamo una fornitura precisa
            daoForn = Fornitura().select(idArticolo=l.rigamovventemp.id_articolo,
                                    numeroLotto = l.lotto_temp,
                                    batchSize = None)

            if daoForn:
                a = RigaMovimentoFornitura()
                a.id_articolo = l.rigamovventemp.id_articolo
                a.id_riga_movimento_vendita = l.id_riga_movimento_vendita_temp
                a.id_fornitura = daoForn[0].id
                params["session"].add(a)
                params["session"].delete(l)
                g += 1
                if g == 2000:
                    params["session"].commit()
                    g = 0
        else:
            params["session"].delete(l)
    params["session"].commit()

if __name__ == '__main__':
    pulizia_lottotemp()


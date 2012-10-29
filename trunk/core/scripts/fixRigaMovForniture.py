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

""" IL FIx consiste nello spostae le righe da rigamovimentoFornitura a
rmovfornirigamoovend per gestire meglio le quantità
"""
from promogest import preEnv
preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "veterfarma"
from promogest.Environment import params  , session , azienda
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
#from promogest.dao.RigaMovFornituraRigaMovVendita import RMovFornituraRMovVendita
from promogest.dao.Setconf import SetConf
from promogest.lib.utils import stringToDateTime, setconf , timeit , pbar


@timeit
def fixRigaMovimentoTable(pbar_wid=None):

    a = SetConf().select(key="fix_riga_movimento", section="General")
    if a and a[0].value =="False":
        rmfall = session.query(RigaMovimentoFornitura.id_articolo, RigaMovimentoFornitura.id_fornitura, RigaMovimentoFornitura.id_riga_movimento_acquisto).distinct().all()
        #print "RMFALL", rmfall
        num = len(rmfall)
        for riga in rmfall:
            #if pbar:
                #pbar(pbar_wid,parziale=rmfall.index(riga), totale=num, text="MIGRAZIONE TABELLA LOTTI ACQUISTO", noeta=False)
            #print "riga", riga
            print "RESIDUI DA GESTIRE ACQ", num - rmfall.index(riga)
            rmf = RigaMovimentoFornitura().select(idArticolo=riga[0], idRigaMovimentoAcquisto=riga[2], idFornitura=riga[1], batchSize=None)
            if rmf:
                for r in rmf:
                    if r.id_riga_movimento_vendita:
                        a = RigaMovimentoFornitura()
                        a.id_articolo = r.id_articolo
                        a.id_riga_movimento_vendita = r.id_riga_movimento_vendita
                        a.id_fornitura = r.id_fornitura
                        session.add(a)
                    if rmf.index(r) == 0:
                        a = RigaMovimentoFornitura()
                        a.id_articolo = r.id_articolo
                        a.id_riga_movimento_acquisto = r.id_riga_movimento_acquisto
                        a.id_fornitura = r.id_fornitura
                        session.add(a)
                    session.delete(r)
                        #session.add(r)
        session.commit()
        print " FINITO ACQ"
        rmfall2 = session.query(RigaMovimentoFornitura.id_riga_movimento_vendita).distinct().all()
        #print rmfall2
        #num2 = len(rmfall2)
        for riga2 in rmfall2:
            ##if pbar_wid:
                ##pbar(pbar_wid,parziale=rmfall2.index(riga2), totale=num2, text="MIGRAZIONE TABELLA LOTTI VENDITA", noeta=False)
            #print "RESIDUI DA GESTIRE VEN", num2 - rmfall2.index(riga2)
            if riga2[0] is not None:
                rmf2 = RigaMovimentoFornitura().select(idRigaMovimentoVendita=riga2[0], batchSize=None)
                #print "RMFFFFFFFFFFFFFFFFFFF", rmf2
                for ff in rmf2[1:]:
                    if ff.id_riga_movimento_acquisto is None:
                        session.delete(ff)
                session.commit()
        #if pbar_wid:
            #pbar(pbar_wid,stop=True)
        #c = SetConf().select(key="fix_riga_movimento", section="General")
        #c[0].value = str(True)
        #session.add(c[0])
        #session.commit()
        #if pbar_wid:
            #pbar_wid.set_property("visible",False)
        #print "FATTO IL FIX"
        #if Environment.azienda =="urbani"
    else:
        print "NIENTE DA FIXARE"
    #from fixForniture import *

if __name__ == '__main__':
    fixRigaMovimentoTable()


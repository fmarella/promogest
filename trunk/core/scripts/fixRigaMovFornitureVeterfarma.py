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
def fixRigaMovimentoTableVETER(pbar_wid=None):
    with open("rmf_veter", "r") as f:
        righe = f.readlines()
    for r in righe:
        if r[0] == '"':
            print "primo tipo", r
            rigl = r.split(";")
            print rigl
        else:
            r = r.replace("    ", " ")
            r = r.replace("   ", " ")
            r = r.replace("  ", " ")
            print "secondo tipo", r
            rigl = r.split(" ")
            print rigl
        idArt = rigl[1]
        idForn = rigl[4]
        idRmac = rigl[2]
        idRmve = rigl[3]

        a = RigaMovimentoFornitura()
        a.id_articolo = int(idArt)
        if idRmve != "" and idRmve != "\\N":
            a.id_riga_movimento_vendita = int(idRmve)
        if idRmac != "" and idRmac != "\\N":
            a.id_riga_movimento_acquisto = int(idRmac)
        a.id_fornitura = int(idForn.replace("\n", ""))
        #print a.__dict__
        session.add(a)
        try:
            session.commit()
        except:
            session.rollback()
            del(a)
            print "NON ANDATO A BUONFINE"
            continue


if __name__ == '__main__':
    fixRigaMovimentoTableVETER()


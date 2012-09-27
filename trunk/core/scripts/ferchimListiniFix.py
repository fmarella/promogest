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

preEnv.tipodbforce = True
preEnv.aziendaforce = "ferchim"
#preEnv.echo = True

from promogest import Environment
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.dao.Listino import Listino
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.dao.ListinoArticolo import ListinoArticolo

listini = Listino().select(batchSize=None)
listino5 = Listino().select(idListino=5)

print listino5[0].__dict__

arti = ListinoArticolo().select(idListino=5, batchSize=None)
#print arti
for a in arti:
    #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", a.id_articolo, a.prezzo_ingrosso
    la = ListinoArticolo().select(idArticolo=a.id_articolo, batchSize=None)
    for l in la:
        #print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", l.id_listino, l.id_articolo, l.ultimo_costo
        l.ultimo_costo = a.prezzo_ingrosso
        #print l, l.__dict__
        Environment.params["session"].add(l)
    Environment.params["session"].commit()
print "FATTO"
#for l in listini:
    #if l.id != 5:
        #print l.id, l.denominazione

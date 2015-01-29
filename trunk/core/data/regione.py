# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from promogest.Environment import *

t_regione  = Table('regione', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100)),
        Column('codice',Integer),
        schema = params['mainSchema'])

t_regione.create(checkfirst=True)


regis = [ (1,'Piemonte'),
        (2,"Valle D'Aosta"),
        (3,"Lombardia"),
        (4,"Trentino Alto Adige"),
        (5,"Veneto"),
        (6,"Friuli Venezia Giulia"),
        (7,"Liguria"),
        (8,"Emilia Romagna"),
        (9,"Toscana"),
        (10,"Umbria"),
        (11,"Marche"),
        (12,"Lazio"),
        (13,"Abruzzo"),
        (14,"Molise"),
        (15,"Campania"),
        (16,"Puglia"),
        (17,"Basilicata"),
        (18,"Calabria"),
        (19,"Sicilia"),
        (20,"Sardegna"),]
s= select([t_regione.c.codice]).execute().fetchall()
if (1,) not in s or s==[]:
    unit = t_regione.insert()
    for a in regis:
        unit.execute(denominazione_breve=a[0], denominazione=a[1])

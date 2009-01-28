#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params
from Dao import Dao
#from promogest.dao.Articolo import Articolo

class CodiceABarreArticolo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'codice':
            dic = {k:codice_barre_articolo.c.codice.ilike("%"+v+"%")}
        elif k == 'codiceEM':
            dic = {k:codice_barre_articolo.c.codice == v}
        elif k == 'idArticolo':
            dic = {k:codice_barre_articolo.c.id_articolo == v}
        elif k == 'idArticoloNone':
            dic = {k:codice_barre_articolo.c.id_articolo == None}
        elif k == 'primario':
            dic = {k:codice_barre_articolo.c.primario ==v}
        return  dic[k]

codice_barre_articolo=Table('codice_a_barre_articolo',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)

std_mapper = mapper(CodiceABarreArticolo, codice_barre_articolo, properties={
        #"articolo":relation(Articolo,backref="codice_a_barre_articolo")
}, order_by=codice_barre_articolo.c.codice)







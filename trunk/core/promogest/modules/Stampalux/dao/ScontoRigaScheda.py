# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco <francesco@promotux.it>

"""
CREATE TABLE sconto_righa_scheda (
     id                         bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_riga_scheda             bigint          NOT NULL REFERENCES righe_schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
from promogest.Environment import *
from Dao import Dao

class ScontoRigaScheda(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':scontorigascheda.c.id ==v,
            'idRigaScheda':scontorigascheda.c.id_riga_scheda==v,}
        return  dic[k]

scontorigascheda=Table('sconto_riga_scheda',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)

sconto=Table('sconto', params['metadata'], schema = params['schema'], autoload=True)

j = join(sconto, scontorigascheda)

std_mapper = mapper(ScontoRigaScheda,j, properties={
    'id':[sconto.c.id, scontorigascheda.c.id],
    }, order_by=scontorigascheda.c.id)

#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class ScontoRigaMovimento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k=='id':
            dic = {k:sconto_riga_movimento.c.id==v}
        elif k=='idRigaMovimento':
            dic= {k:sconto_riga_movimento.c.id_riga_movimento==v}
        return  dic[k]

sconto=Table('sconto',
            params['metadata'],
            schema = params['schema'],
            autoload=True)


sconto_riga_movimento=Table('sconto_riga_movimento',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

j = join(sconto, sconto_riga_movimento)

std_mapper = mapper(ScontoRigaMovimento,j, properties={
    'id':[sconto.c.id, sconto_riga_movimento.c.id],
    }, order_by=sconto_riga_movimento.c.id)




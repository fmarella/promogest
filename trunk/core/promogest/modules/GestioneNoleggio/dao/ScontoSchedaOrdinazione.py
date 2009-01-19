#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
from promogest.Environment import params
from promogest.dao.Dao import Dao

class ScontoSchedaOrdinazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :scontoschedaordinazione.c.id == v}
        elif k== 'idSchedaOrdinazione':
            dic ={k:scontoschedaordinazione.c.id_scheda_ordinazione==v}
        return  dic[k]

sconto=Table('sconto', params['metadata'], schema = params['schema'], autoload=True)

scontoschedaordinazione=Table('sconto_scheda_ordinazione',params['metadata'],schema = params['schema'],
                                        autoload=True)
j = join(sconto, scontoschedaordinazione)

std_mapper = mapper(ScontoSchedaOrdinazione,j, properties={
            'id':[sconto.c.id, scontoschedaordinazione.c.id],
            }, order_by=scontoschedaordinazione.c.id)

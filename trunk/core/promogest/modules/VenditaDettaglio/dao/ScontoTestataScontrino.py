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

class ScontoTestataScontrino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :sconto_testata_documento.c.id == v}
        elif k== 'idScontoTestataScontrino':
            dic ={k:sconto_testata_scontrino.c.id_testata_scontrino==v}
        return  dic[k]



sconto_scontrino=Table('sconto_scontrino', params['metadata'], schema = params['schema'], autoload=True)

sconto_testata_scontrino=Table('sconto_testata_scontrino',params['metadata'],
                                schema = params['schema'],autoload=True)

j = join(sconto_scontrino, sconto_testata_scontrino)

std_mapper = mapper(ScontoTestataScontrino,j, properties={
    'id':[sconto_scontrino.c.id, sconto_testata_scontrino.c.id],
    }, order_by=sconto_testata_scontrino.c.id)

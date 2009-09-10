#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
from promogest.Environment import params
from Dao import Dao

class ScontoTestataDocumento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :sconto_testata_documento.c.id == v}
        elif k== 'idScontoTestataDocumento':
            dic ={k:sconto_testata_documento.c.id_testata_documento==v}
        return  dic[k]



sconto=Table('sconto', params['metadata'], schema = params['schema'], autoload=True)

sconto_testata_documento=Table('sconto_testata_documento',params['metadata'],schema = params['schema'],
                                autoload=True)
j = join(sconto, sconto_testata_documento)

std_mapper = mapper(ScontoTestataDocumento,j, properties={
    'id':[sconto.c.id, sconto_testata_documento.c.id],
    }, order_by=sconto_testata_documento.c.id)

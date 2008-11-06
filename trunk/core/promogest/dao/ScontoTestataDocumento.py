#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class ScontoTestataDocumento(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= { 'id' :sconto_testata_documento.c.id == v,
                'idScontoTestataDocumento' :sconto_testata_documento.c.id_testata_documento==v
                }
        return  dic[k]



sconto=Table('sconto',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

sconto_testata_documento=Table('sconto_testata_documento',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

j = join(sconto, sconto_testata_documento)

std_mapper = mapper(ScontoTestataDocumento,j, properties={
    'id':[sconto.c.id, sconto_testata_documento.c.id],
    }, order_by=sconto_testata_documento.c.id)

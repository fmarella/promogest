# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class ScontoRigaDocumento(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'id':sconto_riga_documento.c.id ==v,
            'idRigaDocumento':sconto_riga_documento.c.id_riga_documento==v,}
        return  dic[k]

sconto_riga_documento=Table('sconto_riga_documento',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)

sconto=Table('sconto',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

j = join(sconto, sconto_riga_documento)

std_mapper = mapper(ScontoRigaDocumento,j, properties={
    'id':[sconto.c.id, sconto_riga_documento.c.id],
    }, order_by=sconto_riga_documento.c.id)

# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class TestataDocumentoScadenza(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {'idTestataDocumentoScadenza': tesdocsca.c.id_testata_documento ==v}
        return  dic[k]

tesdocsca=Table('testata_documento_scadenza',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(TestataDocumentoScadenza, tesdocsca, properties={},
                                order_by=tesdocsca.c.id)


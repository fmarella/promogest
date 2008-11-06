# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class TestataDocumentoScadenza(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'idTestataDocumentoScadenza': tesdocsca.c.id_testata_documento ==v}
        return  dic[k]

tesdocsca=Table('testata_documento_scadenza',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(TestataDocumentoScadenza, tesdocsca, properties={},
                                order_by=tesdocsca.c.id)


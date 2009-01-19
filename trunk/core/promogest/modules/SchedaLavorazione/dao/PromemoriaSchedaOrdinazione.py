# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
import promogest.dao.Dao
from promogest.dao.Dao import Dao
from promogest.Environment import *


class PromemoriaSchedaOrdinazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':promemoriaschedaordinazione.c.id ==v}
        return  dic[k]

promemoriaschedaordinazione=Table('promemoria_scheda_ordinazione',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

std_mapper = mapper(PromemoriaSchedaOrdinazione, promemoriaschedaordinazione, properties={},
                                order_by=promemoriaschedaordinazione.c.id)

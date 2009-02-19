# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
import promogest.dao.Dao
from promogest.dao.Dao import Dao
from promogest.Environment import *
from promogest.dao.Promemoria import Promemoria
#from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione

class PromemoriaSchedaOrdinazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="id" or k=="idPromemoria":
            dic= {k : promemoriaschedaordinazione.c.id ==v}
        elif k=="idScheda":
            dic={k:promemoriaschedaordinazione.c.id_scheda ==v}
        return  dic[k]

promemoriaschedaordinazione=Table('promemoria_scheda_ordinazione',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

promemoria=Table('promemoria', params['metadata'], schema = params['schema'], autoload=True)

j = join(promemoriaschedaordinazione, promemoria)

std_mapper = mapper(PromemoriaSchedaOrdinazione, j, properties={
            'id':[promemoria.c.id, promemoriaschedaordinazione.c.id],
                    },
                                order_by=promemoriaschedaordinazione.c.id)

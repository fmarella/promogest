# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione

class Datario(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':datario.c.id ==v}
        return  dic[k]

datario=Table('datario',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Datario, datario, properties={
                "schedaOrd":relation(SchedaOrdinazione,primaryjoin=
                    contattoscheda.c.id_scheda==SchedaOrdinazione.id, backref="datario")
                        }, order_by = datario.c.id)
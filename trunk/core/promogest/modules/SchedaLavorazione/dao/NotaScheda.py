# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione

class NotaScheda(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':notascheda.c.id ==v}
        return  dic[k]

notascheda=Table('nota_scheda', params['metadata'], schema = params['schema'],
                                                                    autoload=True)

std_mapper = mapper(NotaScheda, notascheda, properties={
                "schedaOrd":relation(SchedaOrdinazione,primaryjoin=
                    contattoscheda.c.id_scheda==SchedaOrdinazione.id, backref="nota_scheda")},
                                order_by=notascheda.c.id)

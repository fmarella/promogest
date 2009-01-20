# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione

class ContattoScheda(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':contattoscheda.c.id ==v}
        return  dic[k]

contattoscheda=Table('contatto_scheda',params['metadata'],schema = params['schema'],
                                                                    autoload=True)

std_mapper = mapper(ContattoScheda, contattoscheda, properties={
                "schedaOrd":relation(SchedaOrdinazione,primaryjoin=
                    contattoscheda.c.id_scheda==SchedaOrdinazione.id, backref="cont_sched") },
                                                },
                                                    order_by=contattoscheda.c.id)

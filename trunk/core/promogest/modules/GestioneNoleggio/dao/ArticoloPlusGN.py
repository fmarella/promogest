# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
#from promogest.modules.GestioneNoleggio.dao.DivisoreNoleggio import DivisoreNoleggio

class ArticoloPlusGN(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k =='idArticolo':
            dic= {k:articologestionenoleggio.c.id_articolo ==v}
        elif k == "idDivisoreNoleggio":
            dic = {k:articologestionenoleggio.c.id_divisore_noleggio ==v}

        return  dic[k]

articologestionenoleggio=Table('articolo_gestione_noleggio',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(ArticoloPlusGN, articologestionenoleggio,
                    #properties=dict(
                    #DN =relation(DivisoreNoleggio,primaryjoin=
                        #(DivisoreNoleggio.id==articologestionenoleggio.c.id_divisore_noleggio), backref="APGNDN"),
                       
                order_by=articologestionenoleggio.c.id_articolo)
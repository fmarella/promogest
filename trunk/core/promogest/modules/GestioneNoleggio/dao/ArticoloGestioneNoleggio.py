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


try:
    articologestionenoleggio=Table('articolo_gestione_noleggio',params['metadata'],schema = params['schema'],autoload=True)
except:
    articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)

    if tipodb == "sqlite":
        articoloFK = 'articolo.id'
    else:
        articoloFK = params['schema']+'.articolo.id'
    params["session"].close()
    conn = params["engine"].connect()
    articologestionenoleggio = Table('articolo_gestione_noleggio', params['metadata'],
                    Column('id_articolo',Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('divisore_noleggio_value',Numeric(4), nullable=False),
                    schema=params['schema'])
    articologestionenoleggio.create(checkfirst=True)
    conn.close()

class ArticoloGestioneNoleggio(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =='idArticolo':
            dic= {k:articologestionenoleggio.c.id_articolo ==v}
        elif k == "idDivisoreNoleggio":
            dic = {k:articologestionenoleggio.c.id_divisore_noleggio ==v}

        return  dic[k]

std_mapper = mapper(ArticoloGestioneNoleggio, articologestionenoleggio,
                    #properties=dict(
                    #DN =relation(DivisoreNoleggio,primaryjoin=
                        #(DivisoreNoleggio.id==articologestionenoleggio.c.id_divisore_noleggio), backref="APGNDN"),
                order_by=articologestionenoleggio.c.id_articolo)

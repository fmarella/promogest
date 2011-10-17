#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

moduleTable  = Table('modulo', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('codice',String(5), unique=True, nullable=False),
        Column('denomination',String(100), unique=True, nullable=False),
        Column('imagepath',String(500)),
        Column('versione',String(200)),
        Column("permalink", String(500), nullable=True),
        Column('insertdate',DateTime),
        Column('body',Text),
        Column('active', Boolean, default=0),
        Column('abstract', String(500), nullable=True),
        Column('clicks', Integer, default=1),
        Column('lite', Boolean, default=0, nullable=False),
        Column('normal', Boolean, default=0, nullable=False),
        Column('prezzo', Numeric(), nullable=True),
        Column('prezzo_rinnovo', Numeric(), nullable=True),
        Column('ordine', Integer, unique=True, nullable=True),
        #useexisting=True,
        schema = params['schema'])
moduleTable.create(checkfirst=True)

class Modulo(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    #@reconstructor
    #def init_on_load(self):
        #self.__dbcategorie = []
        #self.__categorie = []


    def filter_values(self, k,v):
        if k == "denomination":
            dic= { k : module.c.denomination.ilike("%"+v+"%")}
        elif k == "denominationEM":
            dic= { k : module.c.denomination == v}
        elif k == "permalink":
            dic= { k : module.c.permalink == v}
        elif k == "codice":
            dic= { k : module.c.codice == v}
        elif k == "ordine":
            dic= { k : module.c.ordine == v}
        elif k =="active":
            dic = { k :module.c.active ==v}
        return  dic[k]


module=Table('modulo', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Modulo, module, properties={
            #'user' : relation(User, backref="sw"),
            #'lang' : relation(Language),
            #'categ':relation(SoftwareCategorySoftware,primaryjoin = software.c.id==SoftwareCategorySoftware.id_software, backref='sw'),
                }, order_by=module.c.ordine)

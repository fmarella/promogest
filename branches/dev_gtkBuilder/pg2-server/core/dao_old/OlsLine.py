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
from User import User
userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])

if params["tipo_db"] == "sqlite":
    utenteFK ='utente.id'
else:
    utenteFK =params['mainSchema']+'.utente.id'


olslineTable  = Table('ols_line', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('codice',String(10), unique=True, nullable=False),
        Column('data_registrazione',Date),
        Column("data_expire", Date),
        Column('active', Boolean, default=0),
        Column('spot', String(2000), nullable=False),
        Column('clicks', Integer, default=1),
        Column('ordine', Integer, unique=True, nullable=True),
        Column('id_user', Integer,ForeignKey(utenteFK)),
        #useexisting=True,
        schema = params['schema'])
olslineTable.create(checkfirst=True)

class OlsLine(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    #@reconstructor
    #def init_on_load(self):
        #self.__dbcategorie = []
        #self.__categorie = []


    def filter_values(self, k,v):
        if k == "denomination":
            dic= { k : olsline.c.denomination.ilike("%"+v+"%")}
        elif k == "denominationEM":
            dic= { k : olsline.c.denomination == v}
        elif k == "codice":
            dic= { k : olsline.c.codice == v}
        elif k =="active":
            dic = { k :olsline.c.active ==v}
        return  dic[k]


olsline=Table('ols_line', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(OlsLine, olsline, properties={
            'user' : relation(User, backref="olsline"),
            #'lang' : relation(Language),
            #'categ':relation(SoftwareCategorySoftware,primaryjoin = software.c.id==SoftwareCategorySoftware.id_software, backref='sw'),
                }, order_by=olsline.c.ordine.asc())
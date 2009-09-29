#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao


regioniTable  = Table('regione', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100)),
        Column('codice',Integer),
        schema = params['schema'])

regioniTable.create(checkfirst=True)
s= select([regioniTable.c.denominazione]).execute().fetchall()
if (u'Piemonte',) not in s or s ==[]:
    tipo = regioniTable.insert()
    tipo.execute(codice = "01", denominazione='Piemonte')
    tipo.execute(codice = "02", denominazione="Valle D'Aosta")
    tipo.execute(codice = "03", denominazione="Lombardia")
    tipo.execute(codice = "04", denominazione="Trentino Alto Adige")
    tipo.execute(codice = "05", denominazione="Veneto")
    tipo.execute(codice = "06", denominazione="Friuli Venezia Giulia")
    tipo.execute(codice = "07", denominazione="Liguria")
    tipo.execute(codice = "08", denominazione="Emilia Romagna")
    tipo.execute(codice = "09", denominazione="Toscana")
    tipo.execute(codice = "10", denominazione="Umbria")
    tipo.execute(codice = "11", denominazione="Marche")
    tipo.execute(codice = "12", denominazione="Lazio")
    tipo.execute(codice = "13", denominazione="Abruzzo")
    tipo.execute(codice = "14", denominazione="Molise")
    tipo.execute(codice = "15", denominazione="Campania")
    tipo.execute(codice = "16", denominazione="Puglia")
    tipo.execute(codice = "17", denominazione="Basilicata")
    tipo.execute(codice = "18", denominazione="Calabria")
    tipo.execute(codice = "19", denominazione="Sicilia")
    tipo.execute(codice = "20", denominazione="Sardegna")


class Regioni(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':regioni.c.denominazione == v,
                }
        return  dic[k]

regioni=Table('regione', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Regioni, regioni,properties={
        #'compan': relation(CompanyCategoryCompany,primaryjoin = category.c.id==CompanyCategoryCompany.id_company_category, backref='catego')
}, order_by=regioni.c.denominazione
)
#filler()
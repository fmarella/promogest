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

software_categoryTable  = Table('software_category', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100),unique=True),
        schema = params['schema'])

software_categoryTable.create(checkfirst=True)
s= select([software_categoryTable.c.denominazione]).execute().fetchall()
if (u'Gestionale',) not in s or s ==[]:
    tipo = software_categoryTable.insert()
    tipo.execute(denominazione="Gestionale")
    tipo.execute(denominazione="Statistico")
    tipo.execute(denominazione="Contabile")
    tipo.execute(denominazione="Mobile")
    tipo.execute(denominazione="ERP")
    tipo.execute(denominazione="CRM")
    tipo.execute(denominazione="O.S")
    tipo.execute(denominazione="Internet")
    tipo.execute(denominazione="Networking")
    tipo.execute(denominazione="Ufficio")
    tipo.execute(denominazione="Audio Video")
    tipo.execute(denominazione="Grafica")
    tipo.execute(denominazione="Gioco")
    tipo.execute(denominazione="Educazione")
    tipo.execute(denominazione="Sicurezza")
    tipo.execute(denominazione="Scientifico")
    tipo.execute(denominazione="Education")
    tipo.execute(denominazione="Development")
    tipo.execute(denominazione="Database")
    tipo.execute(denominazione=u"Utilità")

class SoftwareCategory(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(k,v):
        dic= {
            'denominazione':sofwaretcategory.c.denominazione == v,
                }
        return  dic[k]

sofwaretcategory=Table('software_category', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(SoftwareCategory, sofwaretcategory)
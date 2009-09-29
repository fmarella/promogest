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


categoryTable  = Table('category', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100),unique=True),
        Column('parent_id',Integer),
        Column('description',String(500)),
        schema = params['schema'])
categoryTable.create(checkfirst=True)
s= select([categoryTable.c.denominazione]).execute().fetchall()
if (u'Formazione',) not in s or s ==[]:
    tipo = categoryTable.insert()
    tipo.execute(denominazione='Formazione',description="Sempre  piu` aziende puntano su Linux e tante sono quelle che si occupano di formazione a distanza  e/o in aula.  Di seguito troverai  tutte le aziende italiane che si occupano di formazione su Linux e su pacchetti Open Source. Corsi in aula, online, personalizzati, di gruppo.")
    tipo.execute(denominazione='Vendita',description="Rivenditori di personal computer con sistema operativo Linux, assistenza hardware e software.")
    tipo.execute(denominazione='Networking',description="Aziende che si occupano di installazione e configurazione di reti e sicurezza - Assistenza sistemistica.")
    tipo.execute(denominazione='Consulenza', description="Aziende che offrono servizi di consulenza informatica su Linux.")
    tipo.execute(denominazione='Gadget', description="Rivenditori di articoli e gadget su Linux e sul suo logo Tux.")
    tipo.execute(denominazione='Editoria ', description="Vuoi conoscere Linux e l'Open Source? Lo conosci gia` e vuoi saperne di piu`? Vuoi tenerti aggiornato? Linux e` anche manuali, riviste mensili, siti web.")
    tipo.execute(denominazione='Blog e Portali', description="Vuoi conoscere Linux e l'Open Source? Lo conosci gia` e vuoi saperne di piu`? Vuoi tenerti aggiornato? Linux e` anche manuali, riviste mensili, siti web.")
    tipo.execute(denominazione='Assistenza Legale', description="Studi legali, Avvocati specializzati su Linux e l'opensource, licenze, brevetti.")
    tipo.execute(denominazione='SW House', description="Societa` che si occupano della creazione e dello sviluppo di software, siti web, ERP, e sistemi operativi.")
    tipo.execute(denominazione='Web', description="Societa` specializzate nello sviluppo di portali e siti web con strumenti open source.")
    tipo.execute(denominazione='Assistenza',description="Assistenza hardware e software.")


class Category(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':category.c.denominazione == v,
                }
        return  dic[k]

category=Table('category', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Category, category,properties={
        #'compan': relation(CompanyCategoryCompany,primaryjoin = category.c.id==CompanyCategoryCompany.id_company_category, backref='catego')
}
)
#filler()
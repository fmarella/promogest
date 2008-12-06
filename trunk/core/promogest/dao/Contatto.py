#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
#from promogest.dao.Recapito import Recapito
from promogest.ui.utils import getCategorieContatto, getRecapitiContatto
from RecapitoContatto import RecapitoContatto
#import promogest.dao.ContattoCategoriaContatto
from ContattoCategoriaContatto import ContattoCategoriaContatto

class Contatto(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = getRecapitiContatto(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)

    def _getCategorieContatto(self):
        self.__dbCategorieContatto = getCategorieContatto(id=self.id)
        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        return ""
    appartenenza = property(_appartenenza)


    #FIXME: verificare TUTTI i filtri Contatto!!!
    def filter_values(self,k,v):
        dic= {  'tipo_contatto' : contatto.c.tipo_contatto == v,
                "idCategoria" : None,
                "appartenenza" : and_(self.appartenenza == v),
                        }
        return  dic[k]

    def delete(self, multiple=False, record = True):
        cleanRecapitoContatto = RecapitoContatto(isList=True).select(idContatto=self.id)
        for recapito in cleanRecapitoContatto:
            recapito.delete()
        cleanContattoCategoriaContatto = ContattoCategoriaContatto(isList=True)\
                                                        .select(idContatto=self.id,
                                                        batchSize=None)
        for contatto in cleanContattoCategoriaContatto:
            contatto.delete()
        params['session'].delete(self)
        params['session'].flush()
        #params["session"].refresh(self)
        params["session"].clear()


contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper=mapper(Contatto, contatto,properties={
    'recapito' : relation(RecapitoContatto, backref=backref('contatto')),
    "contatto_cat_cont": relation(ContattoCategoriaContatto,backref=backref("contatto")),
    }, order_by=contatto.c.id)

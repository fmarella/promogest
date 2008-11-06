# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Azienda import Azienda
from RecapitoContatto import RecapitoContatto
from ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoAzienda(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = RecapitoContatto(isList=True).select(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)

    def _getCategorieContatto(self):
        self.__dbCategorieContatto = ContattoCategoriaContatto(isList=True).select(id=self.id)
        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        a =  params["session"].query(Azienda).with_parent(self).filter(self.schema_azienda==Azienda.schemaa).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale or a[0].denominazione
    appartenenza = property(_appartenenza)


    def filter_values(self,k,v):
        dic= {  'idCategoria' : None,
                'schemaAzienda' : contattoazienda.c.schema_azienda == v,
                #'tipoRecapito':
                'cognomeNome' : or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%")),
                'ruolo': contatto.c.ruolo.ilike("%"+v+"%"),
                'descrizione': contatto.c.descrizione.ilike("%"+v+"%"),
                #'recapito':
            }
        return dic[k]


contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

contattoazienda=Table('contatto_azienda',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

j = join(contatto, contattoazienda)
std_mapper = mapper(ContattoAzienda, j,properties={
                'id':[contatto.c.id, contattoazienda.c.id],
                'tipo_contatto':[contatto.c.tipo_contatto, contattoazienda.c.tipo_contatto],
                "azienda":relation(Azienda, backref="contatto_azienda")},
                order_by=contatto.c.id)


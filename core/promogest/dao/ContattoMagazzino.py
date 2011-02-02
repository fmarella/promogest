# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table, or_
from sqlalchemy.orm import join, relation, mapper
from promogest.Environment import params
from Dao import Dao
from Magazzino import Magazzino
from RecapitoContatto import RecapitoContatto
from ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoMagazzino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = RecapitoContatto().select(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)


    def _getCategorieContatto(self):
        self.__dbCategorieContatto = ContattoCategoriaContatto().select(id=self.id)

        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        a =  params["session"].query(Magazzino).with_parent(self).filter(self.id_magazzino==Magazzino.id).all()
        if not a:
            return a
        else:
            return a[0].denominazione
    appartenenza = property(_appartenenza)

    def filter_values(self,k,v):
        if k == 'idCategoria':
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idMagazzino':
            dic = {k : contattomagazzino.c.id_magazzino == v}
        elif k == 'idMagazzinoList':
            dic = {k : contattomagazzino.c.id_magazzino.in_(v)}
        elif k == 'cognomeNome':
            dic = {k : or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k : contatto.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.tipo_recapito ==v)}
        elif k =='descrizione':
            dic = {k : contatto.c.descrizione.ilike("%"+v+"%")}
        #'recapito':
        #'tipoRecapito':
        return dic[k]

recapito=Table('recapito',params['metadata'],autoload=True,schema = params['schema'])
contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

contattomagazzino=Table('contatto_magazzino',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

j = join(contatto, contattomagazzino)

std_mapper = mapper(ContattoMagazzino, j,properties={
               'id':[contatto.c.id, contattomagazzino.c.id],
                'tipo_contatto':[contatto.c.tipo_contatto, contattomagazzino.c.tipo_contatto],
                "magazzino":relation(Magazzino, backref="contatto_magazzino")},
                order_by=contattomagazzino.c.id)

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
from Fornitore import Fornitore
#from promogest.dao.Contatto import Contatto
from RecapitoContatto import RecapitoContatto
from ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoFornitore(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id, orderBy='cognome, nome',)


    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = RecapitoContatto(isList=True).select(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)


    def _getCategorieContatto(self):
        self.__dbCategorieContatto = ContattoCategoriaContatto(isList=True).select(id=self.id,
                                                                            orderBy="id_contatto")
        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        a =  params["session"].query(Fornitore).with_parent(self).filter(self.id_fornitore==Fornitore.id).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale or a[0].cognome or a[0].nome
    appartenenza = property(_appartenenza)


    #FIXME: sistemare questo filtro
    def filter_values(self, k,v):
        if k == 'idCategoria':
            dic = {k:None}
        elif k == 'idFornitore':
            dic = {k:contattofornitore.c.id_fornitore == v}
        elif k == 'idFornitoreList':
            dic = {k:contattofornitore.c.id_fornitore.in_(v)}
        elif k == 'cognomeNome':
            dic = {k:or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k:contatto.c.ruolo.ilike("%"+v+"%")}
        elif k=='descrizione':
            dic = {k:contatto.c.descrizione.ilike("%"+v+"%")}
            #'recapito':
            #'tipoRecapito':
        return  dic[k]


contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

contattofornitore=Table('contatto_fornitore',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

j = join(contatto, contattofornitore)

std_mapper = mapper(ContattoFornitore, j,properties={
        'id':[contatto.c.id, contattofornitore.c.id],
        'tipo_contatto':[contatto.c.tipo_contatto, contattofornitore.c.tipo_contatto],
        "fornitore":relation(Fornitore, backref="contatto_fornitore")})





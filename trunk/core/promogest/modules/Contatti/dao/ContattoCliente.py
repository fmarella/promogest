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
from promogest.Environment import params
from promogest.dao.Dao import Dao
from promogest.dao.Cliente import Cliente
from promogest.dao.Contatto import Contatto
from promogest.dao.RecapitoContatto import RecapitoContatto
from promogest.dao.ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoCliente(Dao):

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
        self.__dbCategorieContatto = ContattoCategoriaContatto().select(id=self.id,
                                                        orderBy=ContattoCategoriaContatto.id_contatto)

        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        appa = ""
        a =  params["session"].query(Cliente).with_parent(self).filter(self.id_cliente==Cliente.id).all()
        if a:
            appa = "Rif."+a[0].ragione_sociale+" "+a[0].cognome + " " +a[0].nome
        return appa
    appartenenza = property(_appartenenza)


    def filter_values(self,k,v):
        if k == 'idCategoria':
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idCliente':
            dic = {k:contattocliente.c.id_cliente == v}
        elif k == "idClienteList":
            dic = {k:contattocliente.c.id_cliente.in_(v)}
        elif k == 'cognomeNome':
            dic = {k:or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k:contatto.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.tipo_recapito ==v)}
        elif k=='descrizione':
            dic = {k:contatto.c.descrizione.ilike("%"+v+"%")}

        #FIXME: #'recapito'
        #FIXME : #'tipoRecapito':
        return dic[k]

recapito=Table('recapito',params['metadata'],autoload=True,schema = params['schema'])
contatto=Table('contatto', params['metadata'],schema = params['schema'], autoload=True)
contattocliente=Table('contatto_cliente', params['metadata'],schema = params['schema'], autoload=True)

j = join(contatto, contattocliente)

std_mapper = mapper(ContattoCliente, j,properties={
                'id':[contatto.c.id, contattocliente.c.id],
                "cc" : relation(Contatto, backref="contatto_cliente"),
                'tipo_contatto':[contatto.c.tipo_contatto, contattocliente.c.tipo_contatto],
                "cliente":relation(Cliente, backref="contatto_cliente")
                }, order_by=contattocliente.c.id)

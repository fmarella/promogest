#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table, or_
from sqlalchemy.orm import mapper, join, relation
from promogest.Environment import params, conf
from Dao import Dao
from ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.ui.utils import  codeIncrement

class Cliente(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _getCategorieCliente(self):
        self.__dbCategorieCliente = ClienteCategoriaCliente()\
                                    .select(idCliente = self.id,
                                    offset=None,
                                    batchSize=None)
        self.__categorieCliente = self.__dbCategorieCliente[:]
        return self.__categorieCliente

    def _setCategorieCliente(self, value):
        self.__categorieCliente = value
    categorieCliente = property(_getCategorieCliente, _setCategorieCliente)

    def filter_values(self,k,v):
        if k == 'codice':
            dic = {k:persona_giuridica.c.codice.ilike("%"+v+"%")}
        elif k == 'codicesatto':
            dic = {k:persona_giuridica.c.codice == v}
        elif k == 'ragioneSociale':
            dic = {k:persona_giuridica.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k:persona_giuridica.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k:or_(persona_giuridica.c.cognome.ilike("%"+v+"%"),persona_giuridica.c.nome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k:or_(persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"),persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k:persona_giuridica.codice_fiscale.ilike("%"+v+"%")}
        return  dic[k]

def getNuovoCodiceCliente():
    """
        Restituisce il codice progressivo per un nuovo cliente
    """

    lunghezzaCodice = 10
    prefissoCodice = 'CL'
    codice = ''
    listacodici= []
    if hasattr(conf,'Clienti'):
        if hasattr(conf.Clienti,'lunghezza_codice'):
            lunghezzaCodice = conf.Clienti.lunghezza_codice
        if hasattr(conf.Clienti,'prefisso_codice'):
            prefissoCodice = conf.Clienti.prefisso_codice
            try:
                #codicesel  = select([func.max(Cliente.c.codice)]).execute().fetchall()
                codicesel = Cliente().select(batchSize=None)
                for cod in codicesel:
                    listacodici.append(cod.codice)
                codice = codeIncrement(str(max(listacodici)))
            except:
                pass
            try:
                if codice == "" and hasattr(conf.Clienti,'struttura_codice'):
                    codice = codeIncrement(conf.Clienti.struttura_codice)
            except:
                pass
    return codice

persona_giuridica=Table('persona_giuridica', params['metadata'],schema = params['schema'], autoload=True)

cliente=Table('cliente', params['metadata'],schema = params['schema'], autoload=True)

j = join(cliente, persona_giuridica)

std_mapper = mapper(Cliente,j, properties={
        'id':[cliente.c.id, persona_giuridica.c.id],
        'cliente_categoria_cliente':relation(ClienteCategoriaCliente, backref='cliente'),
        }, order_by=cliente.c.id)



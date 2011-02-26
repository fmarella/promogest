# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Table, or_,and_
from sqlalchemy.orm import mapper, join, relation
from promogest.Environment import params, conf,session
from Dao import Dao
from ClienteCategoriaCliente import ClienteCategoriaCliente
from PersonaGiuridica import PersonaGiuridica_
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

    def delete(self):
        categ = self._getCategorieCliente()
        if categ:
            for c in categ:
                c.delete()
        session.delete(self)
        session.commit()


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
        elif k == 'provincia':
            dic = {k:or_(persona_giuridica.c.sede_operativa_provincia.ilike("%"+v+"%"),persona_giuridica.c.sede_legale_provincia.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k:persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        elif k == 'idCategoria':
            dic = {k:and_(Cliente.id==ClienteCategoriaCliente.id_cliente,ClienteCategoriaCliente.id_categoria_cliente==v)}
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
            #codicesel  = select([func.max(Cliente.codice)]).execute().fetchall()
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
        "per_giu" :relation(PersonaGiuridica_, backref='cliente_'),
        'cliente_categoria_cliente':relation(ClienteCategoriaCliente, backref='cliente_'),
        }, order_by=cliente.c.id)

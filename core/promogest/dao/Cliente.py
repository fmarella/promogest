# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params, conf,session
from Dao import Dao
#from promogest.modules.Contatti.dao.ContattoCliente import ContattoCliente
#from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
#from promogest.modules.Contatti.dao.Contatto import Contatto
from ClienteCategoriaCliente import ClienteCategoriaCliente
from PersonaGiuridica import PersonaGiuridica_
from promogest.ui.utils import  codeIncrement, getRecapitiCliente


class Cliente(Dao):

    def __init__(self, req=None):
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

    def _cellularePrincipale(self):
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito =="Cellulare":
                    return reca.recapito
        return ""
    cellulare_principale = property(_cellularePrincipale)

    def _telefonoPrincipale(self):
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito =="Telefono":
                    return reca.recapito
        return ""
    telefono_principale = property(_telefonoPrincipale)

    def _emailPrincipale(self):
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito =="Email":
                    return reca.recapito
        return ""
    email_principale = property(_emailPrincipale)

    def _faxPrincipale(self):
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito =="Fax":
                    return reca.recapito
        return ""
    fax_principale = property(_faxPrincipale)

    def _sitoPrincipale(self):
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito =="Sito":
                    return reca.recapito
        return ""
    sito_principale = property(_sitoPrincipale)


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
    try:
        n = 1
        clienti = session.query(Cliente.codice).all()[-500:]
        clienti.reverse()

        for q in clienti:
            codice = codeIncrement(q[0])
            if not codice or Cliente().select(codicesatto=codice):
                continue
            else:
                if not Cliente().select(codicesatto=codice):
                    return codice

    #quanti = session.query(Cliente).count()
    #if quanti > 0:
        #while session.query(Cliente).offset(quanti-n).limit(1).all():
            #art = session.query(Cliente).offset(quanti-n).limit(1).all()
            #codice = codeIncrement(art[0].codice)
            #if not codice or Cliente().select(codicesatto=codice):
                #if n < 300:
                    #n +=1
                #else:
                    #break
            #else:
                #if not Cliente().select(codicesatto=codice):
                    #return codice
    except:
        pass
    try:
        if not codice:
            from promogest.ui.utils import setconf
            dd = setconf("Clienti", "cliente_struttura_codice")
            codice = codeIncrement(dd)
    except Exception as e:
        pass
    return codice

persona_giuridica = Table('persona_giuridica',
                          params['metadata'],
                          schema=params['schema'],
                          autoload=True)

cliente = Table('cliente',
              params['metadata'],
              schema=params['schema'],
              autoload=True)

if 'id_aliquota_iva' not in [c.name for c in cliente.columns]:
    col = Column('id_aliquota_iva', Integer, nullable=True)
    col.create(cliente, populate_default=True)

j = join(cliente, persona_giuridica)

std_mapper = mapper(Cliente,j, properties={
        'id': [cliente.c.id, persona_giuridica.c.id],
        "per_giu" : relation(PersonaGiuridica_, backref='cliente_'),
        'cliente_categoria_cliente': relation(ClienteCategoriaCliente, backref='cliente_'),
        }, order_by=cliente.c.id)
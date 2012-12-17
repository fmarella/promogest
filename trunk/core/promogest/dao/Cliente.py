# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.Environment import params, conf, session, delete_pickle
from promogest.dao.Dao import Dao
from ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.dao.PersonaGiuridica import t_persona_giuridica
from promogest.dao.User import User
from promogest.dao.DestinazioneMerce import DestinazioneMerce
from promogest.dao.DaoUtils import codeIncrement, getRecapitiCliente, get_columns
from promogest.dao.VariazioneListino import VariazioneListino
from promogest.dao.ClienteVariazioneListino import t_cliente_variazione_listino
from promogest.lib.utils import posso


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
        clienti = session.query(Cliente.codice).all()
        clienti.reverse()

        for q in clienti:
            codice = codeIncrement(q[0])
            if not codice or Cliente().select(codicesatto=codice):
                continue
            else:
                if not Cliente().select(codicesatto=codice):
                    return codice

    except:
        pass
    try:
        if not codice:
            from promogest.lib.utils import setconf
            dd = setconf("Clienti", "cliente_struttura_codice")
            codice = codeIncrement(dd)
    except Exception:
        pass
    return codice


class Cliente(Dao):
    """
    Dao Cliente
    """

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def __repr__(self):
        def _descrizione(obj):
            if obj.tipo=='PG':
                return ', ragione sociale="{0}"'.format(obj.ragione_sociale)
            elif obj.tipo == 'PF':
                return ', nome e cognome="{0} {1}"'.format(obj.nome, obj.cognome)
            else:
                return ''
        return '<Cliente ID={0}>'.format(self.codice) # , _descrizione(self)

    def _getCategorieCliente(self):
        self.__dbCategorieCliente = self.cliente_categoria_cliente
        self.__categorieCliente = self.__dbCategorieCliente[:]
        return self.__categorieCliente

    def _setCategorieCliente(self, value):
        self.__categorieCliente = value
    categorieCliente = property(_getCategorieCliente, _setCategorieCliente)

    def persist(self):
        if not self.codice:
            self.codice = getNuovoCodiceCliente()
        session.add(self)
        session.commit()

    def delete(self):
        """
        Rimuove il cliente
        """
        if len(self.TD) > 0:
            return """<big><b>Non è possibile cancellare il cliente.</b></big>

ESISTONO DOCUMENTI COLLEGATI"""

        if self.id_user:
            utente = User().getRecord(id=self.dao.id_user)
            if utente:
                utente.delete()

        if posso("IP"):
            from promogest.modules.InfoPeso.dao.TestataInfoPeso import\
                                                             TestataInfoPeso
            from promogest.modules.InfoPeso.dao.ClienteGeneralita import\
                                                             ClienteGeneralita
            cltip = TestataInfoPeso().select(idCliente=dao.id, batchSize=None)
            if cltip:
                for l in cltip:
                    l.delete()
            clcg = ClienteGeneralita().select(idCliente=dao.id, batchSize=None)
            if clcg:
                for l in clcg:
                    l.delete()

        #self.delete()
        session.delete(self)
        session.commit()
#        return "OK"

    @property
    def username_login(self):
        """
        """
        if self.id:
            user = User().getRecord(id=self.id_user)
            if user:
                return user.username
        return ""

    @property
    def email_confirmed(self):
        """
        """
        if self.id:
            user = User().getRecord(id=self.id_user)
            if user:
                return user.email_confirmed
        return False

    @property
    def password_login(self):
        """
        """
        if self.id:
            user = User().getRecord(id=self.id_user)
            if user and user.tipo_user == "PLAIN":
                return user.password
        return ""


    @property
    def cellulare_principale(self):
        """
        Ritorna il numero di cellulare principale del cliente
        """
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito == "Cellulare":
                    return reca.recapito
        return ""

    @property
    def telefono_principale(self):
        """
        Ritorna il numero di rete fissa principale del cliente
        """
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito == "Telefono":
                    return reca.recapito
        else:
            return ""

    @property
    def email_principale(self):
        """
        Ritorna l'indirizzo email principale del cliente
        """
        if self.id:
            u = User().getRecord(id=self.id_user)
            if u:
                return u.email
            else:
                for reca in getRecapitiCliente(self.id):
                    if reca.tipo_recapito == "Email":
                        return reca.recapito
        return ""

    @property
    def fax_principale(self):
        """
        Ritorna il fax principale del cliente
        """
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito == "Fax":
                    return reca.recapito
        else:
            return ""

    @property
    def sito_principale(self):
        """
        Ritorna il sito principale del cliente
        """
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito == "Sito":
                    return reca.recapito
        else:
            return ""

    def filter_values(self, k, v):
        if k == 'codice':
            dic = {k: t_persona_giuridica.c.codice.ilike("%"+v+"%")}
        elif k == 'codicesatto':
            dic = {k : t_persona_giuridica.c.codice == v}
        elif k == 'idList':
            dic = {k: t_persona_giuridica.c.id.in_(v)}
        elif k == 'ragioneSociale':
            dic = {k: t_persona_giuridica.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k: t_persona_giuridica.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k: or_(t_persona_giuridica.c.cognome.ilike("%"+v+"%"),t_persona_giuridica.c.nome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k: or_(t_persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"), t_persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'provincia':
            dic = {k: or_(t_persona_giuridica.c.sede_operativa_provincia.ilike("%"+v+"%"), t_persona_giuridica.c.sede_legale_provincia.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k: t_persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k: t_persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        elif k == 'idCategoria':
            dic = {k:and_(Cliente.id==ClienteCategoriaCliente.id_cliente,ClienteCategoriaCliente.id_categoria_cliente==v)}
        return dic[k]

t_cliente = Table('cliente',
              params['metadata'],
              schema=params['schema'],
              autoload=True)

colonne = get_columns(t_cliente)

if 'pagante' not in colonne:
    col = Column('pagante', Boolean, default=False)
    col.create(t_cliente, populate_default=True)
    delete_pickle()

if 'id_aliquota_iva' not in colonne:
    col = Column('id_aliquota_iva', Integer, nullable=True)
    col.create(t_cliente, populate_default=True)
    delete_pickle()


# Sistema di definizione della tipologia di cliente
#opzioni PF ( Persona fisica ) o PG
# PG ( Persona Giusridica )

if 'tipo' not in colonne:
    col = Column('tipo', String(2), default="PG")
    col.create(t_cliente, populate_default=True)

j = join(t_cliente, t_persona_giuridica)

std_mapper = mapper(Cliente,
                    j,
                    properties={

                        'id': [t_cliente.c.id, t_persona_giuridica.c.id],
                        'cliente_categoria_cliente': relation(ClienteCategoriaCliente,cascade="all, delete",
                                                             backref='cliente_'),
                        "dm": relation(DestinazioneMerce,cascade="all, delete",),
                        'vl': relation(VariazioneListino,
                            lazy='joined',
                            secondary=t_cliente_variazione_listino)
                    },
                    order_by=t_cliente.c.id)

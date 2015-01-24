# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.Environment import *

from promogest.dao.Dao import Dao, Base
from ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.dao.User import User
from promogest.dao.DestinazioneMerce import DestinazioneMerce
from promogest.dao.DaoUtils import codeIncrement, getRecapitiCliente, get_columns
from promogest.dao.VariazioneListino import VariazioneListino
from promogest.dao.ClienteVariazioneListino import ClienteVariazioneListino
from promogest.lib.utils import posso, timeit


from data.cliente import t_cliente
from data.personaGiuridica import t_persona_giuridica
cliente_persona_giuridica = join(t_cliente, t_persona_giuridica)

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
        clienti = session.query(Cliente.codice).order_by(desc(Cliente.id)).all()
        for q in clienti:
            codice = codeIncrement(q[0])
            if not codice or (codice,) in clienti:
                continue
            else:
                if (codice,) not in clienti:
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


class Cliente(Base, Dao):
    """
    Dao Cliente
    """
    __table__ = cliente_persona_giuridica
    id = column_property(t_cliente.c.id, t_persona_giuridica.c.id)

    cliente_categoria_cliente = relationship("ClienteCategoriaCliente",cascade="all, delete",
                                                             backref='cliente_')
    dm = relationship("DestinazioneMerce",cascade="all, delete")
    vl = relationship("VariazioneListino",secondary=ClienteVariazioneListino.__table__)

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
            self.cancellato = False
            self.codice = getNuovoCodiceCliente()
        session.add(self)
        session.commit()

    def delete(self):
        """
        Rimuove il cliente
        """
        if len(self.TD) > 0:
            self.cancellato = True
            session.add(self)
        else:
            if self.id_user:
                utente = User().getRecord(id=self.id_user)
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

            session.delete(self)
        session.commit()

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
    def email_pec(self):
        """
        Ritorna l'indirizzo email pec del cliente
        """
        if self.id:
            for reca in getRecapitiCliente(self.id):
                if reca.tipo_recapito == "Email PEC":
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
            dic = {k: PersonaGiuridica_.__table__.c.codice.ilike("%"+v+"%")}
        elif k == 'codicesatto':
            dic = {k : PersonaGiuridica_.__table__.c.codice == v}
        elif k == 'idUser':
            dic = {k : PersonaGiuridica_.__table__.c.id_user == v}
        elif k == 'idPagamento':
            dic = {k : t_cliente.c.id_pagamento == v}
        elif k == 'idBanca':
            dic = {k : t_cliente.c.id_banca == v}
        elif k == 'idList':
            dic = {k: PersonaGiuridica_.__table__.c.id.in_(v)}
        elif k == 'ragioneSociale':
            dic = {k: PersonaGiuridica_.__table__.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k: PersonaGiuridica_.__table__.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k: or_(PersonaGiuridica_.__table__.c.cognome.ilike("%"+v+"%"),PersonaGiuridica_.__table__.c.nome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k: or_(PersonaGiuridica_.__table__.c.sede_operativa_localita.ilike("%"+v+"%"), PersonaGiuridica_.__table__.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'indirizzo':
            dic = {k: or_(PersonaGiuridica_.__table__.c.sede_operativa_indirizzo.ilike("%"+v+"%"), PersonaGiuridica_.__table__.c.sede_legale_indirizzo.ilike("%"+v+"%"))}
        elif k == 'cap':
            dic = {k: or_(PersonaGiuridica_.__table__.c.sede_operativa_cap.ilike("%"+v+"%"), PersonaGiuridica_.__table__.c.sede_legale_cap.ilike("%"+v+"%"))}
        elif k == 'provincia':
            dic = {k: or_(PersonaGiuridica_.__table__.c.sede_operativa_provincia.ilike("%"+v+"%"), PersonaGiuridica_.__table__.c.sede_legale_provincia.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k: PersonaGiuridica_.__table__.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k: PersonaGiuridica_.__table__.c.codice_fiscale.ilike("%"+v+"%")}
        elif k == 'idCategoria':
            dic = {k:and_(Cliente.id==ClienteCategoriaCliente.id_cliente,ClienteCategoriaCliente.id_categoria_cliente==v)}
        elif k == 'cancellato':
            dic = {k: and_(PersonaGiuridica_.__table__.c.cancellato==v)}
        return dic[k]


#if tipodb=="sqlite":
    #from promogest.dao.Pagamento import Pagamento
    #a = session.query(Pagamento.id).all()
    #b = session.query(Cliente.id_pagamento).all()
    #fixit =  list(set(b)-set(a))
    #print "fixt-cliente-pagamento", fixit
    #for f in fixit:
        #if f[0] != "None" and f[0] != None:
            #aa = Cliente().select(idPagamento=f[0], batchSize=None)
            #for a in aa:
                #a.id_pagamento = None
            #session.add(a)
    #from promogest.dao.Banca import Banca
    #c = session.query(Banca.id).all()
    #d = session.query(Cliente.id_banca).all()
    #fixit2 =  list(set(d)-set(c))
    #print "fixt-cliente-banca", fixit2
    #for f in fixit2:
        #if f[0] != "None" and f[0] != None:
            #aa = Cliente().select(idBanca=f[0], batchSize=None)
            #for a in aa:
                #a.id_banca = None
                #session.add(a)
    #session.commit()

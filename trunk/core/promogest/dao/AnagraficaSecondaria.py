# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from promogest.dao.DaoUtils import codeIncrement, getRecapitiAnagraficaSecondaria

persona_giuridica = Table('persona_giuridica',
                        meta,
                        schema=params["schema"],
                        autoload=True)

try:
    anagraficasecondaria = Table('anagrafica_secondaria',
        meta,
        schema=params["schema"],
        autoload=True)

except Exception as e:
    #params["session"].close()
    ruoloTable = Table('role',
        meta,
        autoload=True,
        schema=params["mainSchema"])

    utenteTable = Table('utente',
        meta,
        schema=params["mainSchema"],
        autoload=True)

    pagamentoTable = Table('pagamento',
        meta,
        schema=params["schema"],
        autoload=True)

    bancaTable = Table('banca',
        meta,
        schema=params["schema"],
        autoload=True)

    magazzinoTable = Table('magazzino',
        meta,
        schema=params["schema"],
        autoload=True)

    listinoTable = Table('listino',
        meta,
        schema=params["schema"],
        autoload=True)

    if params["tipo_db"] == "sqlite":
        ruoloFK = 'role.id'
        personagiuridicaFK = 'persona_giuridica.id'
        utenteFK = "utente.id"
        pagamentoFK = "pagamento.id"
        bancaFK = "banca.id"
        magazzinoFK = "magazzino.id"
        listinoFK = "listino.id"
    else:
        ruoloFK = params["mainSchema"] + '.role.id'
        personagiuridicaFK = params["schema"] + '.persona_giuridica.id'
        utenteFK = params["mainSchema"] + ".utente.id"
        pagamentoFK = params["schema"] + '.pagamento.id'
        bancaFK = schema_azienda + '.banca.id'
        magazzinoFK = params["schema"] + '.magazzino.id'
        listinoFK = params["schema"] + '.listino.id'

    anagraficasecondaria = Table('anagrafica_secondaria', meta,
            Column('id', Integer, ForeignKey(personagiuridicaFK,
                onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
            Column('id_ruolo', Integer, ForeignKey(ruoloFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_utente', Integer, ForeignKey(utenteFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_pagamento', Integer, ForeignKey(pagamentoFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_banca', Integer, ForeignKey(bancaFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_magazzino', Integer, ForeignKey(magazzinoFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_listino', Integer, ForeignKey(listinoFK,
                onupdate="CASCADE", ondelete="CASCADE")),
            schema=params["schema"],
            useexisting=True,
            )
    anagraficasecondaria.create(checkfirst=True)
    #Session = sessionmaker(bind=engine)
    #session = Session()

class AnagraficaSecondaria_(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'codice':
            dic = {k: persona_giuridica.c.codice.ilike("%" + v + "%")}
        elif k == 'ragioneSociale':
            dic = {k: persona_giuridica.c.ragione_sociale.ilike("%" + v + "%")}
        elif k == 'idRole':
            dic = {k: anagraficasecondaria.c.id_ruolo == v}
        elif k == 'idMagazzino':
            dic = {k: anagraficasecondaria.c.id_magazzino == v}
        elif k == 'cognomeNome':
            dic = {k: or_(persona_giuridica.c.cognome.ilike("%" + v + "%"),
                persona_giuridica.c.nome.ilike("%" + v + "%"))}
        elif k == 'localita':
            dic = {k: or_(
            persona_giuridica.c.sede_operativa_localita.ilike("%" + v + "%"),
                persona_giuridica.c.sede_legale_localita.ilike("%" + v + "%"))}
        elif k == 'partitaIva':
            dic = {k: persona_giuridica.c.partita_iva.ilike("%" + v + "%")}
        elif k == 'codiceFiscale':
            dic = {k: persona_giuridica.c.codice_fiscale.ilike("%" + v + "%")}
        return  dic[k]

    def _cellularePrincipale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Cellulare":
                    return reca.recapito
        return ""
    cellulare_principale = property(_cellularePrincipale)

    def _telefonoPrincipale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Telefono":
                    return reca.recapito
        return ""
    telefono_principale = property(_telefonoPrincipale)

    def _emailPrincipale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Email":
                    return reca.recapito
        return ""
    email_principale = property(_emailPrincipale)

    def _faxPrincipale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Fax":
                    return reca.recapito
        return ""
    fax_principale = property(_faxPrincipale)

    def _sitoPrincipale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Sito":
                    return reca.recapito
        return ""
    sito_principale = property(_sitoPrincipale)


def getNuovoCodiceAnagraficaSecondaria():
    """
        Restituisce il codice progressivo per un nuovo vettore
    """
    codice = ''
    listacodici = []
    #try:
    codicesel = session.query(AnagraficaSecondaria_).all()[-3:]
    for cod in codicesel:
        listacodici.append(cod.codice)
        codice = codeIncrement(str(max(listacodici)))
    #except:
        #pass
    try:
        if codice == "":
            codice = "AS000"
    except:
        pass
    return codice

j = join(anagraficasecondaria, persona_giuridica)

std_mapper = mapper(AnagraficaSecondaria_, j, properties={
    'id': [anagraficasecondaria.c.id, persona_giuridica.c.id]},
    order_by=anagraficasecondaria.c.id)

# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


from sqlalchemy import *

class PersonaGiuridicaDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):

        userTable = Table('utente',self.metadata, autoload=True, schema=self.mainSchema)

        if self.mainSchema:
            utenteFK = self.mainSchema+'.utente.id'
        else:
            utenteFK = 'utente.id'

        personaGiuridicaTable = Table('persona_giuridica', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('codice', String(50), nullable=True,),
                Column('ragione_sociale',String(200), nullable=True),
                Column('insegna',String(100), nullable=True),
                Column('cognome',String(70), nullable=True),
                Column('nome',String(70), nullable=True),
                Column('sede_operativa_indirizzo',String(300), nullable=True),
                Column('sede_operativa_cap',String(10), nullable=True),
                Column('sede_operativa_provincia',String(50), nullable=True),
                Column('sede_operativa_localita',String(200), nullable=True),
                Column('sede_legale_indirizzo',String(300), nullable=True),
                Column('sede_legale_cap',String(10), nullable=True),
                Column('sede_legale_provincia',String(50), nullable=True),
                Column('sede_legale_localita',String(200), nullable=True),
                Column('nazione',String(100), nullable=True),
                Column('codice_fiscale',String(16), nullable=True),
                Column('partita_iva',String(30), nullable=True),
                Column('id_user',Integer, ForeignKey(utenteFK)),
                schema=self.schema
                )
        personaGiuridicaTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass

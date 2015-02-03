# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

from promogest.dao.Dao import Dao, Base
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.dao.DaoUtils import codeIncrement, getRecapitiAnagraficaSecondaria

from data.anagraficaSecondaria import t_anagrafica_secondaria
from data.personaGiuridica import t_persona_giuridica

anagrafica_secondaria_persona_giuridica = join(t_anagrafica_secondaria, t_persona_giuridica)


class AnagraficaSecondaria_(Base, Dao):

    __table__ = anagrafica_secondaria_persona_giuridica

    id = column_property(t_anagrafica_secondaria.c.id, t_persona_giuridica.c.id)

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'codice':
            dic = {k: t_persona_giuridica.c.codice.ilike("%" + v + "%")}
        elif k == 'ragioneSociale':
            dic = {k: t_persona_giuridica.c.ragione_sociale.ilike("%" + v + "%")}
        elif k == 'idRole':
            dic = {k: t_anagrafica_secondaria.c.id_ruolo == v}
        elif k == 'idMagazzino':
            dic = {k: t_anagrafica_secondaria.c.id_magazzino == v}
        elif k == 'cognomeNome':
            dic = {k: or_(t_persona_giuridica.c.cognome.ilike("%" + v + "%"),
                t_persona_giuridica.c.nome.ilike("%" + v + "%"))}
        elif k == 'localita':
            dic = {k: or_(
            t_persona_giuridica.c.sede_operativa_localita.ilike("%" + v + "%"),
                t_persona_giuridica.c.sede_legale_localita.ilike("%" + v + "%"))}
        elif k == 'partitaIva':
            dic = {k: t_persona_giuridica.c.partita_iva.ilike("%" + v + "%")}
        elif k == 'codiceFiscale':
            dic = {k: t_persona_giuridica.c.codice_fiscale.ilike("%" + v + "%")}
        return  dic[k]

    @property
    def cellulare_principale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Cellulare":
                    return reca.recapito
        return ""
    @property
    def telefono_principale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Telefono":
                    return reca.recapito
        return ""
    @property
    def email_principale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Email":
                    return reca.recapito
        return ""
    @property
    def fax_principale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Fax":
                    return reca.recapito
        return ""
    @property
    def sito_principale(self):
        if self.id:
            for reca in getRecapitiAnagraficaSecondaria(self.id):
                if reca.tipo_recapito == "Sito":
                    return reca.recapito
        return ""


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

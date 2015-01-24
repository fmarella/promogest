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
from promogest.dao.DaoUtils import codeIncrement
from promogest.dao.PersonaGiuridica import PersonaGiuridica_

from data.agente import t_agente
from data.personaGiuridica import t_persona_giuridica

agente_persona_giuridica = join(t_agente, t_persona_giuridica)


class Agente(Base, Dao):
    __table__ = agente_persona_giuridica
    id = column_property(t_agente.c.id, t_persona_giuridica.c.id)

    def __init__(self, req=None):
        """
        Tabella Agente
        """
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        """
        Creazione dei parametri del filtro
        """
        if k == 'codice':
            dic= {k : PersonaGiuridica_.__table__.c.codice.ilike("%"+v+"%")}
        elif k == 'ragioneSociale':
            dic = {k:PersonaGiuridica_.__table__.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k:PersonaGiuridica_.__table__.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k: or_(PersonaGiuridica_.__table__.c.cognome.ilike("%"+v+"%"),
                                PersonaGiuridica_.__table__.c.cognome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k:or_(PersonaGiuridica_.__table__.c.sede_operativa_localita.ilike("%"+v+"%"),
                        PersonaGiuridica_.__table__.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:PersonaGiuridica_.__table__.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = { k:PersonaGiuridica_.__table__.c.codice_fiscale.ilike("%"+v+"%")}
        return  dic[k]

def getNuovoCodiceAgente():
    """
    Restituisce il codice progressivo per un nuovo agente
    """
    codice = ''
    listacodici= []
    if hasattr(conf,'Agenti'):
        try:
            codicesel = Agente().select(batchSize=None)
            for cod in codicesel:
                listacodici.append(cod.codice)
            codice = codeIncrement(str(max(listacodici)))
        except:
            pass
        try:
            if codice == "" and hasattr(conf.Agenti,'struttura_codice'):
                codice = codeIncrement(conf.Agenti.struttura_codice)
        except:
            pass
    return codice

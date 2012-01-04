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

from sqlalchemy import Table, or_
from sqlalchemy.orm import mapper, join
from promogest.Environment import params, conf
from promogest.dao.Dao import Dao
from promogest.ui.utils import  codeIncrement

class Agente(Dao):

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
            dic= {k : persona_giuridica.c.codice.ilike("%"+v+"%")}
        elif k == 'ragioneSociale':
            dic = {k:persona_giuridica.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k:persona_giuridica.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k: or_(persona_giuridica.c.cognome.ilike("%"+v+"%"),
                                persona_giuridica.c.cognome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k:or_(persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"),
                        persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = { k:persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        return  dic[k]

def getNuovoCodiceAgente():
    """
    Restituisce il codice progressivo per un nuovo agente
    """
    codice = ''
    listacodici= []
    if hasattr(conf,'Agenti'):
        try:
            #codicesel  = select([func.max(Cliente.c.codice)]).execute().fetchall()
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


persona_giuridica=Table('persona_giuridica',params['metadata'],
                                                        schema=params['schema'],
                                                        autoload=True)

agent=Table('agente',params['metadata'],schema = params['schema'],autoload=True)

j = join(agent, persona_giuridica)

std_mapper = mapper(Agente,j, properties={
                    'id':[agent.c.id, persona_giuridica.c.id]},
                    order_by=agent.c.id)

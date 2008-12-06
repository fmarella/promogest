# -*- coding: utf-8 -*-

"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 license: GPL see LICENSE file
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from promogest.ui.utils import  codeIncrement

class Agente(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {  'codice' : persona_giuridica.c.codice.ilike("%"+v+"%"),
                'ragioneSociale' : persona_giuridica.c.ragione_sociale.ilike("%"+v+"%"),
                'insegna' : persona_giuridica.c.insegna.ilike("%"+v+"%"),
                'cognomeNome' : or_(persona_giuridica.c.cognome.ilike("%"+v+"%"),persona_giuridica.c.cognome.ilike("%"+v+"%")),
                'localita' : or_(persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"),persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%")),
                'partitaIva' : persona_giuridica.c.partita_iva.ilike("%"+v+"%"),
                'codiceFiscale' : persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
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
            codicesel = Agente(isList=True).select(batchSize=None)
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


persona_giuridica=Table('persona_giuridica',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

agent=Table('agente',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

j = join(agent, persona_giuridica)

std_mapper = mapper(Agente,j, properties={
       'id':[agent.c.id, persona_giuridica.c.id]},
                                    order_by=agent.c.id)
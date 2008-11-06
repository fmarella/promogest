# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import mapper
from promogest.lib.sqlalchemy import and_, or_
from promogest.Environment import *
from Dao import Dao
from promogest.ui.utils import  codeIncrement

class Vettore(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        if k == 'codice':
            dic = {k:persona_giuridica.c.codice.ilike("%"+v+"%")}
        elif k == 'ragioneSociale':
            dic = {k:persona_giuridica.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k:persona_giuridica.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k:or_(persona_giuridica.c.cognome.ilike("%"+v+"%"),persona_giuridica.c.nome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k:or_(persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"),persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k== 'codiceFiscale':
            dic ={k:persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        return  dic[k]

def getNuovoCodiceVettore():
    """
        Restituisce il codice progressivo per un nuovo vettore
    """
    codice = ''
    listacodici= []
    if hasattr(conf,'Vettori'):
        try:
            codicesel = Vettore(isList=True).select(batchSize=None)
            for cod in codicesel:
                listacodici.append(cod.codice)
            codice = codeIncrement(str(max(listacodici)))
        except:
            pass
        try:
            if codice == "" and hasattr(conf.Vettori,'struttura_codice'):
                codice = codeIncrement(conf.Vettori.struttura_codice)
        except:
            pass
    return codice


persona_giuridica=Table('persona_giuridica',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)

vettore=Table('vettore',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

j = join(vettore, persona_giuridica)

std_mapper = mapper(Vettore, j, properties={
    'id':[vettore.c.id, persona_giuridica.c.id]},
    order_by=vettore.c.id)




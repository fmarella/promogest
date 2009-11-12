# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table, or_
from sqlalchemy.orm import mapper, relation, join
from promogest.Environment import params, conf
from Dao import Dao
from CategoriaFornitore import CategoriaFornitore
from promogest.ui.utils import  codeIncrement

class Fornitore(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _categoria(self):
        a =  params["session"].query(CategoriaFornitore).with_parent(self).filter(self.id_categoria_fornitore==CategoriaFornitore.id).all()
        if not a:
            return a
        else:
            return a[0].denominazione
    categoria = property(_categoria)

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
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k:persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        elif k == 'idCategoria':
            dic = {k:fornitore.c.id_categoria_fornitore==v}
        return  dic[k]

def getNuovoCodiceFornitore():
    """ Restituisce il codice progressivo per un nuovo fornitore """

    lunghezzaCodice = 10
    prefissoCodice = 'FO'
    codice = ''
    listacodici = []
    if hasattr(conf,'Fornitori'):
        try:
            codicesel = Fornitore().select(batchSize=None, orderBy="ragione_sociale")
            for cod in codicesel:
                listacodici.append(cod.codice)
                codice = codeIncrement(str(max(listacodici)))
        except:
            pass
        try:
            if codice == "" and hasattr(conf.Fornitori,'struttura_codice'):
                codice = codeIncrement(conf.Fornitori.struttura_codice)
        except:
            pass
    return codice

fornitore=Table('fornitore',params['metadata'],schema = params['schema'],autoload=True)

persona_giuridica=Table('persona_giuridica',params['metadata'],schema = params['schema'],autoload=True)

j = join(fornitore, persona_giuridica)

std_mapper = mapper(Fornitore,j, properties={
        'id':[fornitore.c.id, persona_giuridica.c.id],
        "categoria_fornitore":relation(CategoriaFornitore,backref="fornitore")
        }, order_by=fornitore.c.id)
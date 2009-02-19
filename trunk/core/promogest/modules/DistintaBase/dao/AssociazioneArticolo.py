# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class AssociazioneArticolo(Dao):
    """
    Rappresenta un raggruppamento di articoli relazionati ad un unico articolo "padre"
    """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _codicePadre(self):
        if self.ARTIPADRE: return self.ARTIPADRE.codice
        else: return None
    codice = property(_codicePadre)

    def _denominazionePadre(self):
        if self.ARTIPADRE: return self.ARTIPADRE.denominazione
        else: return None
    denominazione = property(_denominazionePadre)

    def filter_values(self,k,v):
        if k =='idFiglio':
            dic= {k:associazionearticolo.c.id_figlio ==v}
        elif k == "idPadre":
            dic = {k:associazionearticolo.c.id_padre ==v}
        elif k=="codice":
            dic = {k:and_(articolo.c.id == associazionearticolo.c.id_padre,articolo.c.codice.ilike("%"+v+"%"))}
        return  dic[k]

articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
associazionearticolo=Table('associazione_articolo',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(AssociazioneArticolo, associazionearticolo, order_by=associazionearticolo.c.id)

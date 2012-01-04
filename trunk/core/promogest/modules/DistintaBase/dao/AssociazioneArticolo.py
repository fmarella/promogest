# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class AssociazioneArticolo(Dao):
    """
    Rappresenta un raggruppamento di articoli relazionati ad un unico articolo "padre"
    """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @reconstructor
    def init_on_load(self):
        self.__cancellato = None
        self.__codice = None
        self.__denominazione = None


    def _codicePadre(self):
        if self.ARTIPADRE: return self.ARTIPADRE.codice
        else: return None
    codicePadre = property(_codicePadre)


    def _getCodiceFiglio(self):
        if not self.__codice:
            if self.ARTIFIGLIO: return self.ARTIFIGLIO.codice
            else: return None
        else:
            return self.__codice
    def _setCodiceFiglio(self, value):
        self.__codice= value
    codice = property(_getCodiceFiglio, _setCodiceFiglio)

    def _denominazionePadre(self):
        if self.ARTIPADRE: return self.ARTIPADRE.denominazione
        else: return None
    denominazionePadre = property(_denominazionePadre)

    def _getDenominazioneFiglio(self):
        if not self.__denominazione:
            if self.ARTIFIGLIO: return self.ARTIFIGLIO.denominazione
            else:return None
        else:
            return self.__denominazione
    def _setDenominazioneFiglio(self, value):
        self.__denominazione= value
    denominazione = property(_getDenominazioneFiglio, _setDenominazioneFiglio)

    def _getCancellatoFiglio(self):
        if not self.__cancellato:
            if self.ARTIFIGLIO: return self.ARTIFIGLIO.cancellato
            else: return None
        else:
            return self.__cancellato

    def _setCancellatoFiglio(self, value):
        self.__cancellato= value
    cancellato = property(_getCancellatoFiglio, _setCancellatoFiglio)


    def _idArticoloPadre(self):
        if self.ARTIFIGLIO: return self.ARTIFIGLIO.id
        else: return None
    id_articolo = property(_idArticoloPadre)

    def _idListinoPadre(self):
        if self.ARTIFIGLIO: return self.ARTIFIGLIO.id_listino
        else: return None
    id_listino = property(_idListinoPadre)

    def filter_values(self,k,v):
        if k =='idFiglio':
            dic= {k:associazionearticolo.c.id_figlio ==v}
        elif k == "idPadre":
            dic = {k:associazionearticolo.c.id_padre ==v}
        elif k=="codice":
            dic = {k:and_(articolo.c.id == associazionearticolo.c.id_padre,articolo.c.codice.ilike("%"+v+"%"))}
        elif k =="node":
            dic={k:and_(associazionearticolo.c.id_padre == associazionearticolo.c.id_figlio)}
        return  dic[k]


    #def delete(self):
        #print "che succede"

articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
associazionearticolo=Table('associazione_articolo',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(AssociazioneArticolo, associazionearticolo, order_by=associazionearticolo.c.id)

# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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

class NoleggioRiga(Base, Dao):
    """ TABELLA:  riga_dati_noleggio,
        questo dao gestisce la tabella di integrazioen dati su riga:
        per il noleggio è necessario infatti salvare diverse informazioni :
        coeficente di noleggio: ( salvato in articolo può essere modificato in sede
                                di creazione documento)
        numero giorni : ( risultato dalla differenza tra le due date di noleggio
                        é il caso di salvarlo per poter incrociare i dati e perchè
                        sento che a breve sarà necessario gestire archi temporali per riga)
    """
    try:
        __table__ = Table('riga_dati_noleggio', params['metadata'],
                             schema=params['schema'], autoload=True)
    except:
        from data.noleggioRiga import  t_riga_dati_noleggio
        __table__ = t_riga_dati_noleggio


    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:self.__table__.c.id ==v}
        return dic[k]


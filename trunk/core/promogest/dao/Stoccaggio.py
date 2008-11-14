# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Articolo import Articolo
from Magazzino import Magazzino
from DaoUtils import giacenzaSel

class Stoccaggio(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _getTotaliOperazioniMovimento(self):
        self.__dbTotaliOperazioniMovimento = giacenzaSel(year=workingYear, idMagazzino= self.id_magazzino, idArticolo=self.id_articolo)
        self.__totaliOperazioniMovimento = self.__dbTotaliOperazioniMovimento[:]

        return self.__totaliOperazioniMovimento

    def _setTotaliOperazioniMovimento(self, value):
        self.__totaliOperazioniMovimento = value

    totaliOperazioniMovimento = property(_getTotaliOperazioniMovimento,
                                         _setTotaliOperazioniMovimento)

    def _getGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totGiacenza = 0

        for t in totaliOperazioniMovimento:
            totGiacenza += (t['giacenza'] or 0)
            #totGiacenza += (t[4] or 0)
        return totGiacenza

    giacenza = property(_getGiacenza, )

    def _getValoreGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totValoreGiacenza = 0

        for t in totaliOperazioniMovimento:
            totValoreGiacenza += (t['valore'] or 0)
            #totValoreGiacenza += (t[5] or 0)
        return totValoreGiacenza

    valoreGiacenza = property(_getValoreGiacenza, )

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo= property(_denoArticolo)


    def _magazzino(self):
        if self.arti: return self.maga.denominazione
        else: return ""
    magazzino= property(_magazzino)

    def filter_values(self,k,v):
        if k== 'idArticolo':
            dic= {k:stoc.c.id_articolo == v}
        elif k == 'idMagazzino':
            dic = {k:stoc.c.id_magazzino == v}
        return  dic[k]

stoc=Table('stoccaggio',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(Stoccaggio, stoc, properties={
        "arti" : relation(Articolo,primaryjoin=
                stoc.c.id_articolo==Articolo.id, backref="stoccaggio"),
        "maga" : relation(Magazzino,primaryjoin=
                stoc.c.id_magazzino==Magazzino.id, backref="stoccaggio"),
        }, order_by=stoc.c.id)

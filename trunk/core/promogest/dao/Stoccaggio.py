# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params, workingYear, conf
from Dao import Dao
from Articolo import Articolo
from Magazzino import Magazzino
from DaoUtils import giacenzaSel

class Stoccaggio(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

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

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        def _denominazione_gruppo_taglia(self):
            #if self.ATC: return self.ATC.denominazione or ""
            if self.arti:return self.arti.denominazione_gruppo_taglia
            #else: return ""
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            #if self.ATC: return self.ATC.id_articolo_padre or None
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            #if self.ATC: return self.ATC.id_gruppo_taglia or None
            if self.arti:return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            #if self.ATC: return self.ATC.id_genere or None
            if self.arti:return self.arti.id_genere
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.arti:return self.arti.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.arti:return self.arti.id_anno
        id_anno = property(_id_anno)

        def _denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.anno
        anno = property(_anno)

        def _stagione(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.stagione
        stagione = property(_stagione)

        def _genere(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.genere
        genere = property(_genere)

    def filter_values(self,k,v):
        if k== 'idArticolo':
            dic= {k:stoc.c.id_articolo == v}
        elif k == "idArticoloList":
            dic = {k:stoc.c.id_articolo.in_(v)}
        elif k == 'idMagazzino':
            dic = {k:stoc.c.id_magazzino == v}
        return  dic[k]
articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
stoc=Table('stoccaggio',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Stoccaggio, stoc, properties={
        "arti" : relation(Articolo,primaryjoin=
                stoc.c.id_articolo==articolo.c.id, backref="stoccaggio"),
        "maga" : relation(Magazzino,primaryjoin=
                stoc.c.id_magazzino==Magazzino.id, backref="stoccaggio"),
        }, order_by=stoc.c.id)

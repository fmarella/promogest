#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""
from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params, conf
from UnitaBase import UnitaBase
from Dao import Dao

class Multiplo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idArticolo':
            dic= { k : multiplo.c.id_articolo== v}
        elif k == 'idUnitaBase':
            dic = {k: multiplo.c.id_unita_base == v}
        elif k == 'denominazione':
            dic = {k: multiplo.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

    def _unitabase(self):
        if self.uniba:  return self.uniba.denominazione
        else: return ""
    unita_base = property(_unitabase)

    def _articolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo = property(_articolo)

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

multiplo=Table('multiplo',params['metadata'],schema = params['schema'], autoload=True)

std_mapper = mapper(Multiplo, multiplo, properties={
    "uniba":relation(UnitaBase,primaryjoin=multiplo.c.id_unita_base==UnitaBase.id),
    #"arti":relation(Articolo,primaryjoin=multiplo.c.id_articolo==Articolo.id)
        }, order_by=multiplo.c.id)

# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.PromoWear.dao.Taglia import Taglia


class GruppoTagliaTaglia(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'idGruppoTaglia':
            dic= {k: gruppotagliataglia.c.id_gruppo_taglia ==v}
        elif k == 'idTaglia':
            dic= {k: gruppotagliataglia.c.id_taglia ==v}
        return  dic[k]

    def _denominazione_breve_gt(self):
        if self.GTTGT: return self.GTTGT.denominazione_breve or ""
    denominazione_breve_gruppo_taglia= property(_denominazione_breve_gt)

    def _denominazione_gt(self):
        if self.GTTGT: return self.GTTGT.denominazione or ""
    denominazione_gruppo_taglia= property(_denominazione_gt)

    def _denominazione_breve_ta(self):
        if self.TAG: return self.TAG.denominazione_breve or ""
    denominazione_breve_taglia= property(_denominazione_breve_ta)

    def _denominazione_ta(self):
        if self.TAG: return self.TAG.denominazione or ""
    denominazione_taglia= property(_denominazione_ta)

gruppotagliataglia=Table('gruppo_taglia_taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(GruppoTagliaTaglia, gruppotagliataglia, properties={
            "TAG": relation(Taglia,primaryjoin=
            (Taglia.id==gruppotagliataglia.c.id_taglia), backref="GTTTAG"), },
    order_by=(gruppotagliataglia.c.id_gruppo_taglia,gruppotagliataglia.c.ordine))

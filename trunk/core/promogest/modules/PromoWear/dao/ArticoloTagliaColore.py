# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.dao.Dao import Dao, Base
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
from promogest.modules.PromoWear.dao.Modello import Modello


class ArticoloTagliaColore(Base, Dao):
    try:
        __table__ = Table('articolo_taglia_colore',params['metadata'],schema = params['schema'],autoload=True)
    except:
        __table__ = Table('articolo_taglia_colore', params['metadata'],
                    Column('id_articolo',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('id_articolo_padre',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_gruppo_taglia',Integer,ForeignKey(fk_prefix+'gruppo_taglia.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_taglia',Integer,ForeignKey(fk_prefix+"taglia.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_colore',Integer,ForeignKey(fk_prefix+"colore.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_anno',Integer,ForeignKey(fk_prefix_main+"anno_abbigliamento.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_stagione',Integer,ForeignKey(fk_prefix+'stagione_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_genere',Integer,ForeignKey(fk_prefix+'genere_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_modello',Integer,ForeignKey(fk_prefix+'modello.id',onupdate="CASCADE",ondelete="CASCADE")),
                    UniqueConstraint('id_articolo_padre', 'id_gruppo_taglia', "id_taglia", "id_colore"),
                    ForeignKeyConstraint(['id_gruppo_taglia', 'id_taglia'],[fk_prefix+'gruppo_taglia_taglia.id_gruppo_taglia',fk_prefix+'gruppo_taglia_taglia.id_taglia']),
                    schema=params['schema'])

    gruppoTaglia = relationship("GruppoTaglia", backref="ATCGT")
    taglia = relationship("Taglia",backref="ATCTA")
    colore = relationship("Colore",backref="ATCCO")
    AA = relationship("AnnoAbbigliamento",backref="ATCAA")
    SA = relationship("StagioneAbbigliamento",backref="ATCSA")
    GA = relationship("GenereAbbigliamento",backref="ATCGA")
    modello = relationship("Modello",backref="ATCMO")

    __mapper_args__ = {
        'order_by' : "id_taglia"
    }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    #@property
    #def gruppoTaglia(self):
        #""" Restituisce il Dao GruppoTaglia collegato al Dao ArticoloTagliaColore """
        #return self.GT or None

    #@property
    #def taglia(self):
        #""" Restituisce il Dao Taglia collegato al Dao ArticoloTagliaColore """
        #return self.TA

    #@property
    #def modello(self):
        #""" Restituisce il Dao Modello collegato al Dao ArticoloTagliaColore """
        #return self.MO

    #@property
    #def colore(self):
        #""" Restituisce il Dao Colore collegato al Dao ArticoloTagliaColore """
        #return self.CO

    def articoloPadre(self):
        """ Restituisce il Dao Articolo padre del Dao ArticoloTagliaColore """
        #we can't make a property because of recusion articolotagliacolore - articolo
        #resolveProperties goes in loop
        if self.id_articolo_padre is None:
            return None
        from promogest.dao.Articolo import Articolo
        return Articolo().getRecord(id=self.id_articolo_padre)

    def articolo(self):
        """ Restituisce il Dao Articolo collegato al Dao ArticoloTagliaColore """
        #we can't make a property because of recusion articolotagliacolore - articolo
        #resolveProperties goes in loop
        if self.id_articolo is None:
            return None
        from promogest.dao.Articolo import Articolo
        return Articolo().getRecord(id=self.id_articolo)

    @property
    def denominazione_breve_gruppo_taglia(self):
        if self.gruppoTaglia:return self.gruppoTaglia.denominazione_breve or ""
    @property
    def denominazione_gruppo_taglia(self):
        if self.gruppoTaglia:return self.gruppoTaglia.denominazione or ""
    @property
    def denominazione_taglia(self):
        if self.taglia : return self.taglia.denominazione or ""
    @property
    def denominazione_modello(self):
        if self.modello : return self.modello.denominazione or ""
    @property
    def denominazione_breve_taglia(self):
        if self.taglia : return self.taglia.denominazione_breve or ""
    @property
    def denominazione_colore(self):
        if self.colore : return self.colore.denominazione or ""
    @property
    def denominazione_breve_colore(self):
        if self.colore : return self.colore.denominazione_breve or ""
    @property
    def anno(self):
        if self.AA : return self.AA.denominazione or ""
    @property
    def stagione(self):
        if self.SA : return self.SA.denominazione or ""
    @property
    def genere(self):
        if self.GA : return self.GA.denominazione or ""

    def filter_values(self,k,v):
        if k =='idArticolo':
            dic= {k:self.__table__.c.id_articolo ==v}
        elif k == "idTaglia":
            dic = {k:self.__table__.c.id_taglia ==v}
        elif k == "idGruppoTaglia":
            dic = {k:self.__table__.c.id_gruppo_taglia ==v}
        elif k == "idColore":
            dic = {k:self.__table__.c.id_colore ==v}
        elif k == "idArticoloPadre":
            dic = {k:self.__table__.c.id_articolo_padre ==v}
        return  dic[k]

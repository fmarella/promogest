# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from promogest.dao.Dao import Dao
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
from promogest.modules.PromoWear.dao.Modello import Modello


class ArticoloTagliaColore(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def _getGruppoTaglia(self):
        """ Restituisce il Dao GruppoTaglia collegato al Dao ArticoloTagliaColore """
        if self.id_gruppo_taglia is None:
            return None
        return self.GT
        #return GruppoTaglia().getRecord(id=self.id_gruppo_taglia)

    gruppoTaglia = property(_getGruppoTaglia)


    def _getTaglia(self):
        """ Restituisce il Dao Taglia collegato al Dao ArticoloTagliaColore """
        if self.id_taglia is None:
            return None
        return self.TA
        #return Taglia().getRecord(id=self.id_taglia)
    taglia = property(_getTaglia)

    def _getModello(self):
        """ Restituisce il Dao Taglia collegato al Dao ArticoloTagliaColore """
        if self.id_modello is None:
            return None
        return self.MO
        #return Modello().getRecord(id=self.id_modello)
    modello = property(_getModello)

    def _getColore(self):
        """ Restituisce il Dao Colore collegato al Dao ArticoloTagliaColore """
        if self.id_colore is None:
            return None
        return self.CO
        #return Colore().getRecord(id=self.id_colore)
    colore = property(_getColore)

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

    def _denominazione_breve_gruppo_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.GT:return self.GT.denominazione_breve or ""
    denominazione_breve_gruppo_taglia = property(_denominazione_breve_gruppo_taglia)

    def _denominazione_gruppo_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.GT:return self.GT.denominazione or ""
    denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

    def _denominazione_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.TA : return self.TA.denominazione or ""
    denominazione_taglia = property(_denominazione_taglia)

    def _denominazione_modello(self):
        """ esempio di funzione  unita alla property """
        if self.MO : return self.MO.denominazione or ""
    denominazione_modello = property(_denominazione_modello)

    def _denominazione_breve_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.TA : return self.TA.denominazione_breve or ""
    denominazione_breve_taglia = property(_denominazione_breve_taglia)

    def _denominazione_colore(self):
        """ esempio di funzione  unita alla property """
        if self.CO : return self.CO.denominazione or ""
    denominazione_colore = property(_denominazione_colore)

    def _denominazione_breve_colore(self):
        """ esempio di funzione  unita alla property """
        if self.CO : return self.CO.denominazione_breve or ""
    denominazione_breve_colore = property(_denominazione_breve_colore)


    def _denominazione_anno(self):
        """ esempio di funzione  unita alla property """
        if self.AA : return self.AA.denominazione or ""
    anno = property(_denominazione_anno)

    def _denominazione_stagione(self):
        """ esempio di funzione  unita alla property """
        if self.SA : return self.SA.denominazione or ""
    stagione = property(_denominazione_stagione)

    def _denominazione_genere(self):
        """ esempio di funzione  unita alla property """
        if self.GA : return self.GA.denominazione or ""
    genere = property(_denominazione_genere)

    def filter_values(self,k,v):
        if k =='idArticolo':
            dic= {k:articolotagliacolore.c.id_articolo ==v}
        elif k == "idTaglia":
            dic = {k:articolotagliacolore.c.id_taglia ==v}
        elif k == "idGruppoTaglia":
            dic = {k:articolotagliacolore.c.id_gruppo_taglia ==v}
        elif k == "idColore":
            dic = {k:articolotagliacolore.c.id_colore ==v}
        elif k == "idArticoloPadre":
            dic = {k:articolotagliacolore.c.id_articolo_padre ==v}
        return  dic[k]

articolo=Table('articolo',params['metadata'],schema = params['schema'],autoload=True)
articolotagliacolore=Table('articolo_taglia_colore',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(ArticoloTagliaColore, articolotagliacolore,properties={

    "GT":relation(GruppoTaglia,primaryjoin=
                    (GruppoTaglia.id==articolotagliacolore.c.id_gruppo_taglia), backref="ATCGT"),
    "TA":relation(Taglia,primaryjoin=
                    (Taglia.id==articolotagliacolore.c.id_taglia), backref="ATCTA"),
    "CO":relation(Colore,primaryjoin=
                    (Colore.id==articolotagliacolore.c.id_colore), backref="ATCCO"),
    "AA":relation(AnnoAbbigliamento,primaryjoin=
                    (AnnoAbbigliamento.id==articolotagliacolore.c.id_anno), backref="ATCAA"),
    "SA":relation(StagioneAbbigliamento,primaryjoin=
                    (StagioneAbbigliamento.id==articolotagliacolore.c.id_stagione), backref="ATCSA"),
    "GA":relation(GenereAbbigliamento,primaryjoin=
                    (GenereAbbigliamento.id==articolotagliacolore.c.id_genere), backref="ATCGA"),
    "MO":relation(Modello,primaryjoin=
                    (Modello.id==articolotagliacolore.c.id_modello), backref="ATCMO"),
        },
                order_by=articolotagliacolore.c.id_taglia)



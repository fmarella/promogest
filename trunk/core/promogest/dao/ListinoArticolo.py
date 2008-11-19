#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import and_, or_
from promogest.Environment import *
from Dao import Dao
from AliquotaIva import AliquotaIva
from Listino import Listino
from Articolo import Articolo

import datetime

class ListinoArticolo(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _denominazione(self):
        if self.listi:return self.listi.denominazione
        else: return ""
    denominazione= property(_denominazione)

    def _data_listino(self):
        if self.listi:return self.listi.data_listino
        else: return ""
    data_listino= property(_data_listino)

    def _codice_articolo(self):
        if self.arti:return self.arti.codice
        else: return ""
    codice_articolo= property(_codice_articolo)

    def _articolo(self):
        if self.arti:return self.arti.denominazione
        else: return ""
    articolo= property(_articolo)

    def _aliquota_iva(self):
        if self.arti:return self.arti.denominazione_aliquota_iva
        else: return ""
    aliquota_iva= property(_aliquota_iva)

    def _percentuale_iva(self):
        if self.arti:return self.arti.percentuale_aliquota_iva
        else: return ""
    percentuale_iva= property(_percentuale_iva)

    def _codice_a_barre(self):
        if self.arti:return self.arti.codice_a_barre
        else: return ""
    codice_a_barre= property(_codice_a_barre)


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
        if k=="listinoAttuale":
            dic={ k : listinoarticolo.c.listino_attuale ==v}
        elif k=="idArticolo":
            dic= { k : listinoarticolo.c.id_articolo==v}
        elif k=='idArticoloList':
            dic={ k :listinoarticolo.c.id_articolo.in_(v)}
        elif k=="idListino":
            dic={ k: listinoarticolo.c.id_listino==v}
        return  dic[k]

    def persist(self):
        if not self.data_listino_articolo:
            self.data_listino_articolo = datetime.datetime.today()
        if not self.listino_attuale:
            self.listino_attuale = True
        else:
            self.listino_attuale = True
        params["session"].add(self)
        params["session"].commit()
        params["session"].flush()


listinoarticolo=Table('listino_articolo',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper=mapper(ListinoArticolo, listinoarticolo, properties={
            "arti" : relation(Articolo,primaryjoin=
                and_(listinoarticolo.c.id_articolo==Articolo.id,Articolo.cancellato==False)),
            "listi" : relation(Listino,primaryjoin=
                listinoarticolo.c.id_listino==Listino.id)},
                order_by=listinoarticolo.c.id_listino)

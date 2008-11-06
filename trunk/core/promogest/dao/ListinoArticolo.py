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
from Articolo import Articolo
from Listino import Listino
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
#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import *
from Dao import Dao
from Magazzino import Magazzino
from Listino import Listino
from Multiplo import Multiplo
from Articolo import Articolo
from UnitaBase import UnitaBase

class Riga(Dao):
    """ Mapper to handle the Row Table """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        """ Filtro del Mapper Riga"""
        if k=='descrizione':
            dic= {  k : riga.c.descrizione.ilike("%"+v+"%")}
        elif k=="id_articolo":
            dic={k:riga.c.id_articolo==v}
        return  dic[k]

    def __magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""
    magazzino= property(__magazzino)

    def __listino(self):
        if self.listi: return self.listi.denominazione
        else: return ""
    listino= property(__listino)

    def __multiplo(self):
        if self.multi: return self.multi.denominazione
        else: return ""
    multiplo = property(__multiplo)

    def __codiceArticolo(self):
        if self.arti:return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _getAliquotaIva(self):
        #_denominazioneBreveAliquotaIva = Articolo().getRecord(id=self.id_articolo).denominazione_breve_aliquota_iva
        #return _denominazioneBreveAliquotaIva
        if self.arti:return self.arti.denominazione_breve_aliquota_iva
        else: return ""
    aliquota = property(_getAliquotaIva, )

    def __unita_base(self):
        a =  params["session"].query(Articolo).with_parent(self).filter(self.arti.id_unita_base==UnitaBase.id).all()
        if not a:
            return a
        else:
            return a[0].den_unita.denominazione_breve
    unita_base = property(__unita_base)



riga=Table('riga', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Riga, riga, properties={
            "maga":relation(Magazzino,primaryjoin=riga.c.id_magazzino==Magazzino.id),
            "listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
            "multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),
            "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
}, order_by=riga.c.id)


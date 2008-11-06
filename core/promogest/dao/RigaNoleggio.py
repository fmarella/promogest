#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.Multiplo import Multiplo


riga_mov=Table('riga_movimento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

class RigaMovimento(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def __magazzino(self):
        a =  params["session"].query(Magazzino).with_parent(self).filter(RigaMovimento.id_magazzino==Magazzino.c.id).all()
        if not a: return a
        else: return a[0].denominazione
    magazzino= property(__magazzino)

    def __listino(self):
        a =  params["session"].query(Listino).with_parent(self).filter(RigaMovimento.id_listino==Listino.c.id).all()
        if not a: return a
        else: return a[0].denominazione
    listino= property(__listino)

    def __multiplo(self):
        a =  params["session"].query(Multiplo).with_parent(self).filter(RigaMovimento.id_multiplo==Multiplo.c.id).all()
        if not a: return a
        else: return a[0].denominazione
    multiplo = property(__multiplo)

    def __codiceArticolo(self):
        """ esempio di funzione  unita alla property """
        a =  params["session"].query(Articolo).with_parent(self).filter(RigaMovimento.id_articolo==Articolo.c.id).all()
        if not a: return a
        else: return a[0].codice
    codice_articolo= property(__codiceArticolo)
 
    def _getScontiRigaMovimento(self):
        #if self.__dbScontiRigaMovimento is None:
        self.__dbScontiRigaMovimento = ScontoRigaMovimento(isList=True).select(id=self.id,
                                                                            offset = None,
                                                                            batchSize = None)
        #if self.__scontiRigaMovimento is None:
        self.__scontiRigaMovimento = self.__dbScontiRigaMovimento[:]
        return self.__scontiRigaMovimento

    def _setScontiRigaMovimento(self, value):
        self.__scontiRigaMovimento = value

    sconti = property(_getScontiRigaMovimento, _setScontiRigaMovimento)

    def filter_values(self,k,v):
        dic= {  'idTestataMovimento' :self.id_testata_movimento ==v,
        }
        return  dic[k]


j = join(riga_mov, Riga)

std_mapper = mapper(RigaMovimento, j,properties={
        'id':[riga_mov.c.id, Riga.id],
        "maga":relation(Magazzino,primaryjoin=Riga.id_magazzino==Magazzino.id),
        "arti":relation(Articolo,primaryjoin=Riga.id_articolo==Articolo.id),
        "listi":relation(Listino,primaryjoin=Riga.id_listino==Listino.id),
        "multi":relation(Multiplo,primaryjoin=Riga.id_multiplo==Multiplo.id),
        })





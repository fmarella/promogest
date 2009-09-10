# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Articolo import Articolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
#from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
#import promogest.dao.ScontoRigaScontrino
from promogest.dao.Sconto import Sconto
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import scontoRigaScontrinoDel
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino

class RigaScontrino(Dao):


    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _getScontiRigaScontrino(self):
        self.__dbScontiRigaScontrino = ScontoRigaScontrino().select(idRigaScontrino=self.id, batchSize=None)
        if self.__dbScontiRigaScontrino:
            self.__scontiRigaScontrino = self.__dbScontiRigaScontrino[:]
        else:
            self.__scontiRigaScontrino = None
        return self.__scontiRigaScontrino

    def _setScontiRigaScontrino(self, value):
        if not value:
            self.__scontiRigaScontrino = []
        else:
            self.__scontiRigaScontrino = value
    sconti = property(_getScontiRigaScontrino, _setScontiRigaScontrino)

    def _valoreSconto(self):
        #if self.srs:return self.srs.valore_sconto
        #else: return ""
        a = params["session"].query(ScontoRigaScontrino).with_parent(self).filter(and_(ScontoRigaScontrino.id_riga_scontrino==riga_scontrino.c.id, ScontoRigaScontrino.id==Sconto.id)).all()
        if not a:
            return a
        else:
            return a[0].valore
    valore_sconto= property(_valoreSconto)

    def _tipoSconto(self):
        a = params["session"].query(ScontoRigaScontrino).with_parent(self).filter(ScontoRigaScontrino.id_riga_scontrino==riga_scontrino.c.id).all()
        #if self.srs:return self.srs.tipo_sconto
        #else: return ""
        if not a:
            return a
        else:
            return a[0].tipo_sconto
    tipo_sconto= property(_tipoSconto)

    def __codiceArticolo(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _codice_a_barre(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.codice_a_barre
        else: return ""
    codice_a_barre = property(_codice_a_barre)

    def filter_values(self,k,v):
        dic= {'id':riga_scontrino.c.id ==v,
            'idArticolo':riga_scontrino.c.id_articolo==v,
            'idTestataScontrino': riga_scontrino.c.id_testata_scontrino==v}
        return  dic[k]

    def persist(self):
        params['session'].add(self)
        params['session'].commit()

        #cancellazione sconti associati alla riga
        #scontoRigaScontrinoDel(id=self.id)
        if self.__scontiRigaScontrino:
            for rigasconto in self.__scontiRigaScontrino:
                #annullamento id dello sconto
                rigasconto._resetId()
                #associazione allo sconto della riga
                rigasconto.id_riga_scontrino = self.id
                #salvataggio sconto
                rigasconto.persist()
        #params['session'].flush()



riga_scontrino=Table('riga_scontrino',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(RigaScontrino, riga_scontrino,properties={
        "arti":relation(Articolo,primaryjoin=riga_scontrino.c.id_articolo==Articolo.id),
        "srs":relation(ScontoRigaScontrino, primaryjoin=riga_scontrino.c.id ==ScontoRigaScontrino.id_riga_scontrino)
        }, order_by=riga_scontrino.c.id)
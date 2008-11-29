# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Multiplo import Multiplo
from ScontoFornitura import ScontoFornitura
from Fornitore import Fornitore
#from Articolo import Articolo

class Fornitura(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _getScontiFornitura(self):
        self.__dbScontiFornitura = params['session'].query(ScontoFornitura).with_parent(self).filter_by(id_fornitura=fornitura.c.id).all()
        self.__scontiFornitura = self.__dbScontiFornitura[:]
        return self.__scontiFornitura

    def _setScontiFornitura(self, value):
        self.__scontiFornitura = value

    sconti = property(_getScontiFornitura, _setScontiFornitura)

    def _fornitore(self):
        if self.forni: return self.forni.ragione_sociale or ""
        #else: return ""
    fornitore= property(_fornitore)

    def _codice_fornitore(self):
        if self.forni: return self.forni.codice or ""
        #else: return ""
    codice_fornitore= property(_codice_fornitore)

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice or ""
        #else: return ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione or ""
        #else: return ""
    articolo= property(_denoArticolo)

    def _multiplo(self):
        if self.multi: return self.multi.denominazione_breve or ""
        #else: return ""
    multiplo= property(_multiplo)


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
        if k == 'codiceArticoloFornitore':
            dic = {k:fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%")}
        elif k== 'idFornitore':
            dic= {k:fornitura.c.id_fornitore ==v}
        elif k== 'idFornitoreList':
            dic= {k:fornitura.c.id_fornitore.in_(v)}
        elif k == 'idArticolo':
            dic = {k:fornitura.c.id_articolo==v}
        elif k == 'idArticoloList':
            dic = {k:fornitura.c.id_articolo.in_(v)}
        elif k == 'daDataPrezzo':
            dic = {k:fornitura.c.data_prezzo >= v}
        elif k == 'aDataPrezzo':
            dic = {k:fornitura.c.data_prezzo <= v}
        elif k == 'daDataFornitura':
            dic= {k:fornitura.c.data_fornitura >= v}
        elif k == 'aDataFornitura':
            dic = {k:fornitura.c.data_fornitura <= v}
        elif k == 'codiceArticoloFornitoreEsatto':
            dic = {k:fornitura.c.codice_articolo_fornitore ==v}
        return  dic[k]

    #def persist(self, conn=None):

    """FIXME:
            ##cancellazione sconti associati alla fornitura
            #conn.execStoredProcedure('ScontiFornituraDel',
                                    #(self.id, ))

            #if self.__scontiFornitura is not None:
                #for i in range(0, len(self.__scontiFornitura)):
                    ##annullamento id dello sconto
                    #self.__scontiFornitura[i]._resetId()
                    ##associazione allo sconto della fornitura
                    #self.__scontiFornitura[i].id_fornitura = self.id
                    ##salvataggio sconto
                    #self.__scontiFornitura[i].persist(conn)
                    """

fornitura=Table('fornitura',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(Fornitura,fornitura, properties={
        "multi": relation(Multiplo,primaryjoin=fornitura.c.id_multiplo==Multiplo.id),
        "sconto_fornitura": relation(ScontoFornitura, backref="fornitura"),
        "forni" : relation(Fornitore,primaryjoin=fornitura.c.id_fornitore==Fornitore.id),
        #"arti" : relation(Articolo,primaryjoin=fornitura.c.id_articolo==Articolo.id, backref=backref("artic", uselist=False)),
                }, order_by=fornitura.c.id)
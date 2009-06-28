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
from promogest.Environment import *
from Dao import Dao
from DaoUtils import *
from Listino import Listino
from Articolo import Articolo
from ScontoVenditaDettaglio import ScontoVenditaDettaglio
from ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.ui.utils import *

import datetime

class ListinoArticolo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

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

        def _denominazione_modello(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_modello
        denominazione_modello = property(_denominazione_modello)

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


    def _getScontiVenditaDettaglio(self):
        self.__dbScontiVenditaDett = params['session'].query(ScontoVenditaDettaglio).filter_by(id_listino=self.id_listino,
                                                                                            id_articolo=self.id_articolo,
                                                                                            data_listino_articolo=self.data_listino_articolo).all()
        self.__scontiVenditaDett= self.__dbScontiVenditaDett
        return self.__scontiVenditaDett

    def _setScontiVenditaDettaglio(self,value):
         self.__scontiVenditaDett = value

    sconto_vendita_dettaglio = property(_getScontiVenditaDettaglio, _setScontiVenditaDettaglio)

    def _getApplicazioneScontiDettaglio(self):
        return "scalare"

##    def _setApplicazioneScontiDettaglio(self,value):
##        return

    applicazione_sconti_dettaglio = property(_getApplicazioneScontiDettaglio)

    def _getScontiVenditaIngrosso(self):
        self.__dbScontiVenditaIngr = params['session'].\
                                    query(ScontoVenditaIngrosso).\
                                    filter_by(id_listino=self.id_listino,
                                            id_articolo=self.id_articolo,
                                            data_listino_articolo=self.data_listino_articolo).all()
        self.__scontiVenditaIngr= self.__dbScontiVenditaIngr
        return self.__scontiVenditaIngr

    def _setScontiVenditaIngrosso(self,value):
        self.__scontiVenditaIngr = value

    sconto_vendita_ingrosso = property(_getScontiVenditaIngrosso, _setScontiVenditaIngrosso)

    def _getStringaScontiDettaglio(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiVenditaDettaglio(),daoApplicazione = 'scalare')
        return getStringaSconti(listSconti)

    stringaScontiDettaglio = property(_getStringaScontiDettaglio)

    def _getStringaScontiIngrosso(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiVenditaIngrosso(),daoApplicazione = 'scalare')
        return getStringaSconti(listSconti)

    stringaScontiIngrosso = property(_getStringaScontiIngrosso)



    def _getApplicazioneScontiIngrosso(self):
        return "scalare"

##    def _setApplicazioneScontiIngrosso(self,value):
##        self._applicazione_sconti_ingrosso = value

    applicazione_sconti_ingrosso = property(_getApplicazioneScontiIngrosso)


    def filter_values(self,k,v):
        if k=="listinoAttuale":
            dic={ k : listinoarticolo.c.listino_attuale ==v}
        elif k=="idArticolo":
            dic= { k : listinoarticolo.c.id_articolo==v}
        elif k=='idArticoloList':
            dic={ k :listinoarticolo.c.id_articolo.in_(v)}
        elif k=="idListino":
            dic={ k: listinoarticolo.c.id_listino==v}
        elif k=="idListinoList":
            dic={ k: listinoarticolo.c.id_listino.in_(v)}
        elif k=="dataListinoArticoloList":
            dic={ k: listinoarticolo.c.data_listino_articolo.in_(v)}
        elif k=="dataListinoArticolo":
            dic={ k: listinoarticolo.c.data_listino_articolo ==v}
        return  dic[k]

    def persist(self,sconti=None):

        if not self.data_listino_articolo:
            self.data_listino_articolo = datetime.datetime.today()
        check = ListinoArticolo().select(idListino=self.id_listino, idArticolo=self.id_articolo, batchSize=None)
        if check:
            for che in check:
                che.listino_attuale = False
                params["session"].add(che)
                self.saveAppLog(che)
        if not self.listino_attuale:
            self.listino_attuale = True
        else:
            self.listino_attuale = True
        params["session"].add(self)
        self.saveAppLog(self)
        scontiVenditaDettaglioDel(idListino=self.id_listino,
                                    idArticolo=self.id_articolo,
                                    dataListinoArticolo=self.data_listino_articolo)
        scontiVenditaIngrossoDel(idListino=self.id_listino,
                                            idArticolo=self.id_articolo,
                                            dataListinoArticolo=self.data_listino_articolo)
        if sconti:
            for key,value in sconti.items():
                if (key=="dettaglio") and (value):
                    for v in value:
                        v.id_listino = self.id_listino
                        v.id_articolo = self.id_articolo
                        v.data_listino_articolo = self.data_listino_articolo
                        params["session"].add(v)
                        self.saveAppLog(v)
                elif (key=="ingrosso") and (value):
                    for u in value:
                        u.id_listino = self.id_listino
                        u.id_articolo = self.id_articolo
                        u.data_listino_articolo = self.data_listino_articolo
                        params["session"].add(u)
                        self.saveAppLog(u)
        try:
            self.__scontiVenditaDett[0].id_listino=self.id_listino
            self.__scontiVenditaDett[0].id_articolo = self.id_articolo
            self.__scontiVenditaDett[0].data_listino_articolo = self.data_listino_articolo
            params["session"].add(self.__scontiVenditaDett[0])
            self.saveAppLog(self.__scontiVenditaDett[0])
        except:
            pass

        try:
            self.__scontiVenditaIngr[0].id_listino=self.id_listino
            self.__scontiVenditaIngr[0].id_articolo = self.id_articolo
            self.__scontiVenditaIngr[0].data_listino_articolo = self.data_listino_articolo
            params["session"].add(self.__scontiVenditaIngr[0])
            self.saveAppLog(self.__scontiVenditaIngr[0])
        except:
            pass

        params["session"].commit()



listinoarticolo=Table('listino_articolo',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper=mapper(ListinoArticolo, listinoarticolo, properties={
            "arti" : relation(Articolo,primaryjoin=
                and_(listinoarticolo.c.id_articolo==Articolo.id,Articolo.cancellato==False), backref="listinoarticolo"),
            "SVD": relation(ScontoVenditaDettaglio,primaryjoin=and_(
                listinoarticolo.c.id_listino==ScontoVenditaDettaglio.id_listino,
                listinoarticolo.c.id_articolo==ScontoVenditaDettaglio.id_articolo,
                listinoarticolo.c.data_listino_articolo==ScontoVenditaDettaglio.data_listino_articolo)),
            "SVI": relation(ScontoVenditaIngrosso,primaryjoin=and_(
                listinoarticolo.c.id_listino==ScontoVenditaIngrosso.id_listino,
                listinoarticolo.c.id_articolo==ScontoVenditaIngrosso.id_articolo,
                listinoarticolo.c.data_listino_articolo==ScontoVenditaIngrosso.data_listino_articolo)),
            "listi" : relation(Listino,primaryjoin=
                listinoarticolo.c.id_listino==Listino.id, backref="listinoarticolo")},
                order_by=listinoarticolo.c.id_articolo)

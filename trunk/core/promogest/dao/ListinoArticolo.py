# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

import datetime
from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import *

try:
    t_listino_articolo=Table('listino_articolo',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    from data.listinoArticolo import t_listino_articolo

from promogest.dao.Dao import Dao
from promogest.dao.DaoUtils import *
from promogest.dao.Listino import Listino
from promogest.dao.Articolo import Articolo
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.lib.utils import *





class ListinoArticolo(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__scontiVenditaDett = None
        self.__scontiVenditaIngr = None

    @reconstructor
    def init_on_load(self):
        self.__scontiVenditaDett = None
        self.__scontiVenditaIngr = None

    def cleann(self):
        falsi = self.select(listinoAttuale=bool(0), batchSize=None)
        if falsi:
            for f in falsi:
                f.delete()

    @property
    def denominazione(self):
        if self.listi:return self.listi.denominazione
        else: return ""

    @property
    def data_listino(self):
        if self.listi:return self.listi.data_listino
        else: return ""

    @property
    def codice_articolo(self):
        if self.arti:return self.arti.codice
        else: return ""

    @property
    def articolo_famiglia(self):
        if self.arti:return self.arti.denominazione_famiglia
        else: return ""

    @property
    def articolo_categoria(self):
        if self.arti:return self.arti.denominazione_categoria
        else: return ""

    @property
    def articolo(self):
        if self.arti:return self.arti.denominazione
        else: return ""

    @property
    def aliquota_iva(self):
        if self.arti:return self.arti.denominazione_aliquota_iva
        else: return ""

    @property
    def percentuale_iva(self):
        if self.arti:return self.arti.percentuale_aliquota_iva
        else: return ""

    @property
    def codice_a_barre(self):
        if self.arti:return self.arti.codice_a_barre
        else: return ""

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":

        @property
        def denominazione_gruppo_taglia(self):
            if self.arti:return self.arti.denominazione_gruppo_taglia

        def _id_articolo_padre(self):
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            if self.arti:return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            if self.arti:return self.arti.id_genere
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

        @property
        def denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_colore

        @property
        def denominazione_modello(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_modello

        @property
        def anno(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.anno

        @property
        def stagione(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.stagione

        @property
        def genere(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.genere

    def _getScontiVenditaDettaglio(self):
        #self.__dbScontiVenditaDett = params['session'].\
                        #query(ScontoVenditaDettaglio).\
                        #filter_by(id_listino=self.id_listino,
                        #id_articolo=self.id_articolo,
                        #data_listino_articolo=self.data_listino_articolo).all()
        self.__dbScontiVenditaDett = self.SVD
        self.__scontiVenditaDett= self.__dbScontiVenditaDett
        return self.__scontiVenditaDett

    def _setScontiVenditaDettaglio(self,value):
         self.__scontiVenditaDett = value

    sconto_vendita_dettaglio = property(_getScontiVenditaDettaglio,
                                                 _setScontiVenditaDettaglio)

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
        self.__dbScontiVenditaIngr = self.SVI
        self.__scontiVenditaIngr= self.__dbScontiVenditaIngr
        return self.__scontiVenditaIngr

    def _setScontiVenditaIngrosso(self,value):
        self.__scontiVenditaIngr = value

    sconto_vendita_ingrosso = property(_getScontiVenditaIngrosso, _setScontiVenditaIngrosso)

    @property
    def sconto_vendita_ingrosso_valore(self):
        if self.sconto_vendita_ingrosso:return self.sconto_vendita_ingrosso[0].valore
        else: return ""

    @property
    def sconto_vendita_dettaglio_valore(self):
        if self.sconto_vendita_dettaglio:return self.sconto_vendita_dettaglio[0].valore
        else: return ""

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
            dic={ k : t_listino_articolo.c.listino_attuale ==v}
        elif k=="idArticolo":
            dic= { k : t_listino_articolo.c.id_articolo==v}
        elif k=='idArticoloList':
            dic={ k :t_listino_articolo.c.id_articolo.in_(v)}
        elif k=="idListino":
            dic={ k: t_listino_articolo.c.id_listino==v}
        elif k=="idListinoList":
            dic={ k: t_listino_articolo.c.id_listino.in_(v)}
        elif k=="dataListinoArticoloList":
            dic={ k: t_listino_articolo.c.data_listino_articolo.in_(v)}
        elif k=="dataListinoArticolo":
            dic={ k: t_listino_articolo.c.data_listino_articolo ==v}
        return  dic[k]

    def scontiVenditaDettaglioDel(self, idListino=None,idArticolo=None,dataListinoArticolo=None):
        """
        cancella gli sconti associati al listino articolo
        """
        if self.SVD:
            for r in self.SVD:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def scontiVenditaIngrossoDel(self, idListino=None,idArticolo=None,dataListinoArticolo=None):
        """
        cancella gli sconti associati al listino articolo
        """
        if self.SVI:
            for r in self.SVI:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def persist(self,sconti=None):

        if not self.data_listino_articolo:
            self.data_listino_articolo = datetime.datetime.today()
        check = ListinoArticolo().select(idListino=self.id_listino, idArticolo=self.id_articolo, batchSize=None)
        if check:
            for che in check:
                che.listino_attuale = False
                params["session"].add(che)
        if not self.listino_attuale:
            self.listino_attuale = True
        else:
            self.listino_attuale = True
        params["session"].add(self)

        self.scontiVenditaDettaglioDel(idListino=self.id_listino,
                                    idArticolo=self.id_articolo,
                                    dataListinoArticolo=self.data_listino_articolo)
        self.scontiVenditaIngrossoDel(idListino=self.id_listino,
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
                        #self.saveAppLog(v)
                elif (key=="ingrosso") and (value):
                    for u in value:
                        u.id_listino = self.id_listino
                        u.id_articolo = self.id_articolo
                        u.data_listino_articolo = self.data_listino_articolo
                        params["session"].add(u)
                        #self.saveAppLog(u)
        elif self.__scontiVenditaDett:
            try:
                self.__scontiVenditaDett[0].id_listino=self.id_listino
                self.__scontiVenditaDett[0].id_articolo = self.id_articolo
                self.__scontiVenditaDett[0].data_listino_articolo = self.data_listino_articolo
                params["session"].add(self.__scontiVenditaDett[0])
            except:
                pass
        elif self.__scontiVenditaIngr:
            try:
                self.__scontiVenditaIngr[0].id_listino=self.id_listino
                self.__scontiVenditaIngr[0].id_articolo = self.id_articolo
                self.__scontiVenditaIngr[0].data_listino_articolo = self.data_listino_articolo
                params["session"].add(self.__scontiVenditaIngr[0])
            except:
                pass

        params["session"].commit()


std_mapper=mapper(ListinoArticolo, t_listino_articolo, properties={
            "arti" : relation(Articolo,primaryjoin=
                and_(t_listino_articolo.c.id_articolo==Articolo.id,Articolo.cancellato==False), backref=backref("listinoarticolo",cascade="all, delete")),
            "SVD": relation(ScontoVenditaDettaglio,primaryjoin=and_(
                t_listino_articolo.c.id_listino==ScontoVenditaDettaglio.id_listino,
                t_listino_articolo.c.id_articolo==ScontoVenditaDettaglio.id_articolo,
                t_listino_articolo.c.data_listino_articolo==ScontoVenditaDettaglio.data_listino_articolo)),
            "SVI": relation(ScontoVenditaIngrosso,primaryjoin=and_(
                t_listino_articolo.c.id_listino==ScontoVenditaIngrosso.id_listino,
                t_listino_articolo.c.id_articolo==ScontoVenditaIngrosso.id_articolo,
                t_listino_articolo.c.data_listino_articolo==ScontoVenditaIngrosso.data_listino_articolo)),
            "listi" : relation(Listino,primaryjoin=
                t_listino_articolo.c.id_listino==Listino.id, backref="listinoarticolo")},
                order_by=t_listino_articolo.c.id_listino)

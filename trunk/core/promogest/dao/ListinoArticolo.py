# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

from promogest.dao.Dao import Dao, Base
from promogest.dao.DaoUtils import *
from promogest.dao.Listino import Listino
from promogest.dao.Articolo import Articolo
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.lib.utils import *


class ListinoArticolo(Base, Dao):
    try:
        __table__ =Table('listino_articolo',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)
    except:
        from data.listinoArticolo import t_listino_articolo
        __table__ = t_listino_articolo

    arti = relationship("Articolo",primaryjoin=and_(
                __table__.c.id_articolo==Articolo.id,Articolo.cancellato==False), backref=backref("listinoarticolo",cascade="all, delete"))
    SVD = relationship("ScontoVenditaDettaglio",primaryjoin=and_(
                __table__.c.id_listino==ScontoVenditaDettaglio.id_listino,
                __table__.c.id_articolo==ScontoVenditaDettaglio.id_articolo,
                __table__.c.data_listino_articolo==ScontoVenditaDettaglio.data_listino_articolo))
    SVI = relationship("ScontoVenditaIngrosso",primaryjoin=and_(
                __table__.c.id_listino==ScontoVenditaIngrosso.id_listino,
                __table__.c.id_articolo==ScontoVenditaIngrosso.id_articolo,
                __table__.c.data_listino_articolo==ScontoVenditaIngrosso.data_listino_articolo))
    listi = relationship("Listino",primaryjoin=
                __table__.c.id_listino==Listino.id, backref="listinoarticolo")


    __mapper_args__ = {
        'order_by' : "id_listino"
     }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__scontiVenditaDett = None
        self.__scontiVenditaIngr = None

    def __repr__(self):
        return "<VariazioneListino ID_LIST={0} ID_ART={1} DATA_LI={2}>".format(self.id_listino, self.id_articolo, self.data_listino_articolo)

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
    def id_aliquota_iva(self):
        if self.arti:return self.arti.id_aliquota_iva
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

        @property
        def id_gruppo_taglia(self):
            if self.arti:return self.arti.id_gruppo_taglia
        @property
        def id_genere(self):
            if self.arti:return self.arti.id_genere
        @property
        def id_stagione(self):
            if self.arti:return self.arti.id_stagione
        @property
        def id_anno(self):
            if self.arti:return self.arti.id_anno
        @property
        def denominazione_taglia(self):
            if self.arti:return self.arti.denominazione_taglia
        @property
        def denominazione_colore(self):
            if self.arti:return self.arti.denominazione_colore
        @property
        def denominazione_modello(self):
            if self.arti:return self.arti.denominazione_modello
        @property
        def anno(self):
            if self.arti:return self.arti.anno
        @property
        def stagione(self):
            if self.arti:return self.arti.stagione
        @property
        def genere(self):
            if self.arti:return self.arti.genere

    def _getScontiVenditaDettaglio(self):
        self.__dbScontiVenditaDett = self.SVD
        self.__scontiVenditaDett= self.__dbScontiVenditaDett
        return self.__scontiVenditaDett

    def _setScontiVenditaDettaglio(self,value):
         self.__scontiVenditaDett = value

    sconto_vendita_dettaglio = property(_getScontiVenditaDettaglio,
                                                 _setScontiVenditaDettaglio)

    def _getApplicazioneScontiDettaglio(self):
        return "scalare"

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
    @property
    def stringaScontiDettaglio(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiVenditaDettaglio(),daoApplicazione = 'scalare')
        return getStringaSconti(listSconti)

    @property
    def stringaScontiIngrosso(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiVenditaIngrosso(),daoApplicazione = 'scalare')
        return getStringaSconti(listSconti)

    @property
    def applicazione_sconti_ingrosso(self):
        return "scalare"

    def filter_values(self,k,v):
        if k=="listinoAttuale":
            dic={ k : ListinoArticolo.__table__.c.listino_attuale ==v}
        elif k=="idArticolo":
            dic= { k : ListinoArticolo.__table__.c.id_articolo==v}
        elif k=='idArticoloList':
            dic={ k :ListinoArticolo.__table__.c.id_articolo.in_(v)}
        elif k=="idListino":
            dic={ k: ListinoArticolo.__table__.c.id_listino==v}
        elif k=="idListinoList":
            dic={ k: ListinoArticolo.__table__.c.id_listino.in_(v)}
        elif k=="dataListinoArticoloList":
            dic={ k: ListinoArticolo.__table__.c.data_listino_articolo.in_(v)}
        elif k=="dataListinoArticolo":
            dic={ k: ListinoArticolo.__table__.c.data_listino_articolo ==v}
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

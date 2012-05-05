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
from promogest.dao.Dao import Dao
from promogest.dao.Listino import Listino
from promogest.Environment import *
from promogest.lib.utils import *
from promogest.modules.SchedaLavorazione.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.modules.SchedaLavorazione.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.modules.SchedaLavorazione.dao.CarattereStampa import CarattereStampa
from promogest.modules.SchedaLavorazione.dao.PromemoriaSchedaOrdinazione import PromemoriaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.Datario import Datario
from promogest.modules.SchedaLavorazione.dao.ContattoScheda import ContattoScheda
from promogest.modules.SchedaLavorazione.dao.NotaScheda import NotaScheda
from promogest.modules.SchedaLavorazione.dao.RecapitoSpedizione import RecapitoSpedizione
from promogest.dao.Cliente import Cliente
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.dao.Riga import Riga

class SchedaOrdinazione(Dao):
    """ Fornisce nuove funzionalità abbinate alla personalizzazione"
    """

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

        self.__dbScontiSchedaOrdinazione = None
        self.__scontiSchedaOrdinazione = None
        self.__dbRigheSchedaOrdinazione = None
        self.__righeSchedaOrdinazione = None
        self.__dbPromemoriaSchedaOrdinazione = None
        self.__promemoriaSchedaOrdinazione = None

    @reconstructor
    def init_on_load(self):
        self.__dbScontiSchedaOrdinazione = None
        self.__scontiSchedaOrdinazione = None
        self.__dbRigheSchedaOrdinazione = None
        self.__righeSchedaOrdinazione = None
        self.__dbPromemoriaSchedaOrdinazione = None
        self.__promemoriaSchedaOrdinazione = None
        self._referente = None
        self._prima_email = None
        self._data_matrimonio = None
        self._data_presa_in_carico = None
        self._data_consegna = None
        self._data_consegna_bozza = None
        self._data_ordine_al_fornitore = None
        self._data_ricevuta = None
        self._data_spedizione = None
        self._colore_stampa = None
        self._carattere_stampa = None
        self._note_final= None
        self._note_fornitore = None
        self._nome_contatto = None
        self._note_spedizione = None
        self._note_text = None
        self._presso = None
        self._via_piazza = None
        self._num_civ = None
        self._zip = None
        self._localita = None
        self._provincia = None
        self._stato = None
        self._telefono = None
        self._cellulare = None
        self._skype = None
        self.seconda_email=None


    def _getRigheSchedaOrdinazione(self):
        #if self.__dbRigheSchedaOrdinazione is None and self.id:
        if self.id:
            self.__dbRigheSchedaOrdinazione = RigaSchedaOrdinazione().select(idSchedaOrdinazione=self.id, batchSize=None)
        #if self.__righeSchedaOrdinazione is None:
            self.__righeSchedaOrdinazione = self.__dbRigheSchedaOrdinazione[:]
        else:
            self.__righeSchedaOrdinazione = []
        return self.__righeSchedaOrdinazione

    def _setRigheSchedaOrdinazione(self, value):
        self.__righeSchedaOrdinazione = value

    righe = property(_getRigheSchedaOrdinazione, _setRigheSchedaOrdinazione)

    def _getScontiSchedaOrdinazione(self):
        #if self.__dbScontiSchedaOrdinazione is None:
        if self.id:
            self.__dbScontiSchedaOrdinazione = ScontoSchedaOrdinazione().select(idSchedaOrdinazione=self.id,batchSize=None)
        #if self.__scontiSchedaOrdinazione is None:
            self.__scontiSchedaOrdinazione = self.__dbScontiSchedaOrdinazione[:]
        else:
            self.__scontiSchedaOrdinazione = []
        return self.__scontiSchedaOrdinazione

    def _setScontiSchedaOrdinazione(self, value):
        self.__scontiSchedaOrdinazione = value

    sconti = property(_getScontiSchedaOrdinazione, _setScontiSchedaOrdinazione)

    def _getStringaScontiSchedaOrdinazione(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiSchedaOrdinazione(), self.applicazione_sconti)
        return getStringaSconti(listSconti)

    stringaSconti = property(_getStringaScontiSchedaOrdinazione)

    def _getPromemoriaSchedaOrdinazione(self):
        if self.__dbPromemoriaSchedaOrdinazione is None:
            self.__dbPromemoriaSchedeOrdinazioni = PromemoriaSchedaOrdinazione().select(idScheda=self.id,
                                                                        batchSize=None)
        if self.__promemoriaSchedaOrdinazione is None:
            self.__promemoriaSchedaOrdinazione = self.__dbPromemoriaSchedaOrdinazione
        return self.__promemoriaSchedaOrdinazione

    def _setPromemoriaSchedaOrdinazione(self, value):
        self.__promemoriaSchedaOrdinazione = value

    promemoria = property(_getPromemoriaSchedaOrdinazione, _setPromemoriaSchedaOrdinazione)

    #property da datario

    def _get_data_matrimonio(self):
        if self._data_matrimonio:
            return self._data_matrimonio
        else:
            if self.datar: return self.datar.matrimonio
            else: return ""
    def _set_data_matrimonio(self, value):
        self._data_matrimonio = value
    data_matrimonio = property(_get_data_matrimonio, _set_data_matrimonio)

    def _get_data_presa_in_carico(self):
        if self._data_presa_in_carico:
            return self._data_presa_in_carico
        else:
            if self.datar: return self.datar.presa_in_carico
            else: return ""
    def _set_data_presa_in_carico(self, value):
        self._data_presa_in_carico = value
    data_presa_in_carico = property(_get_data_presa_in_carico, _set_data_presa_in_carico)

    def _get_data_ordine_al_fornitore(self):
        if self._data_ordine_al_fornitore:
            return self._data_ordine_al_fornitore
        else:
            if self.datar: return self.datar.ordine_al_fornitore
            else: return ""
    def _set_data_ordine_al_fornitore(self, value):
        self._data_ordine_al_fornitore = value
    data_ordine_al_fornitore = property(_get_data_ordine_al_fornitore, _set_data_ordine_al_fornitore)

    def _get_data_consegna_bozza(self):
        if self._data_consegna_bozza:
            return self._data_consegna_bozza
        else:
            if self.datar: return self.datar.consegna_bozza
            else: return ""
    def _set_data_consegna_bozza(self, value):
        self._data_consegna_bozza = value
    data_consegna_bozza = property(_get_data_consegna_bozza, _set_data_consegna_bozza)

    def _get_data_spedizione(self):
        if self._data_spedizione:
            return self._data_spedizione
        else:
            if self.datar: return self.datar.spedizione
            else: return ""
    def _set_data_spedizione(self, value):
        self._data_spedizione = value
    data_spedizione = property(_get_data_spedizione, _set_data_spedizione)

    def _get_data_consegna(self):
        if self._data_consegna:
            return self._data_consegna
        else:
            if self.datar: return self.datar.consegna
            else: return ""
    def _set_data_consegna(self, value):
        self._data_consegna = value
    data_consegna = property(_get_data_consegna, _set_data_consegna)


    def _get_data_ricevuta(self):
        if self._data_ricevuta:
            return self._data_ricevuta
        else:
            if self.datar: return self.datar.ricevuta
            else: return ""
    def _set_data_ricevuta(self, value):
        self._data_ricevuta = value
    data_ricevuta = property(_get_data_ricevuta, _set_data_ricevuta)

    def _get_prima_email(self):
        if self._prima_email:
            return self._prima_email
        else:
            if self.cont_sched: return self.cont_sched.prima_email
            else: return ""
    def _set_prima_email(self, value):
        self._prima_email = value
    prima_email = property(_get_prima_email, _set_prima_email)

    def _get_seconda_email(self):
        if self._seconda_email:
            return self._seconda_email
        else:
            if self.cont_sched: return self.cont_sched.seconda_email
            else: return ""
    def _set_seconda_email(self, value):
        self._seconda_email = value
    seconda_email = property(_get_seconda_email, _set_seconda_email)

    def _get_telefono(self):
        if self._telefono:
            return self._telefono
        else:
            if self.cont_sched: return self.cont_sched.telefono
            else: return ""
    def _set_telefono(self, value):
        self._telefono = value
    telefono = property(_get_telefono, _set_telefono)

    def _get_cellulare(self):
        if self._cellulare:
            return self._cellulare
        else:
            if self.cont_sched: return self.cont_sched.cellulare
            else: return ""
    def _set_cellulare(self, value):
        self._cellulare = value
    cellulare = property(_get_cellulare, _set_cellulare)

    def _get_skype(self):
        if self._skype:
            return self._skype
        else:
            if self.cont_sched: return self.cont_sched.skype
            else: return ""
    def _set_skype(self, value):
        self._skype = value
    skype = property(_get_skype, _set_skype)

    #property recapito spedizione
    def _get_referente(self):
        if self._referente:
            return self._referente
        else:
            if self.recapito_sped: return self.recapito_sped.referente
            else: return ""
    def _set_referente(self, value):
        self._referente = value
    referente = property(_get_referente, _set_referente)

    def _get_presso(self):
        if self._presso:
            return self._presso
        else:
            if self.recapito_sped: return self.recapito_sped.presso
            else: return ""
    def _set_presso(self, value):
        self._presso = value
    presso = property(_get_presso, _set_presso)

    def _get_via_piazza(self):
        if self._via_piazza:
            return self._via_piazza
        else:
            if self.recapito_sped: return self.recapito_sped.via_piazza
            else: return ""
    def _set_via_piazza(self, value):
        self._via_piazza = value
    via_piazza = property(_get_via_piazza, _set_via_piazza)

    def _get_num_civ(self):
        if self._num_civ:
            return self._num_civ
        else:
            if self.recapito_sped: return self.recapito_sped.num_civ
            else: return ""
    def _set_num_civ(self, value):
        self._num_civ = value
    num_civ = property(_get_num_civ, _set_num_civ)

    def _get_zip(self):
        if self._zip:
            return self._zip
        else:
            if self.recapito_sped: return self.recapito_sped.zip
            else: return ""
    def _set_zip(self, value):
        self._zip = value
    zip = property(_get_zip, _set_zip)

    def _get_localita(self):
        if self._localita:
            return self._localita
        else:
            if self.recapito_sped: return self.recapito_sped.localita
            else: return ""
    def _set_localita(self, value):
        self._localita = value
    localita = property(_get_localita, _set_localita)

    def _get_provincia(self):
        if self._provincia:
            return self._provincia
        else:
            if self.recapito_sped: return self.recapito_sped.provincia
            else: return ""
    def _set_provincia(self, value):
        self._provincia = value
    provincia = property(_get_provincia, _set_provincia)

    def _get_stato(self):
        if self._stato:
            return self._stato
        else:
            if self.recapito_sped: return self.recapito_sped.stato
            else: return ""
    def _set_stato(self, value):
        self._stato = value
    stato = property(_get_stato, _set_stato)

    #property colore_stampa
    def _get_colore_stampa(self):
        #if self._colore_stampa:
            #return self._colore_stampa
        #else:
        if self.COLOSTAMP: return self.COLOSTAMP.denominazione
        else: return ""
    def _set_colore_stampa(self, value):
        self._colore_stampa = value
    colore_stampa = property(_get_colore_stampa, _set_colore_stampa)
    #property carattere_stampa
    def _get_carattere_stampa(self):
        #if self._carattere_stampa:
            #return self._carattere_stampa
        #else:
        if self.CARATTSTAM: return self.CARATTSTAM.denominazione
        else: return ""
    def _set_carattere_stampa(self, value):
        self._carattere_stampa = value
    carattere_stampa = property(_get_carattere_stampa, _set_carattere_stampa)
    #property nota scheda
    def _get_note_final(self):
        if self._note_final:
            return self._note_final
        else:
            if self.nota_scheda: return self.nota_scheda.note_final
            else: return ""
    def _set_note_final(self, value):
        self._note_final = value
    note_final = property(_get_note_final, _set_note_final)

    def _get_note_text(self):
        if self._note_text:
            return self._note_text
        else:
            if self.nota_scheda: return self.nota_scheda.note_text
            else: return ""
    def _set_note_text(self, value):
        self._note_text = value
    note_text = property(_get_note_text, _set_note_text)

    def _cliente(self):
        if self.cli: return self.cli.ragione_sociale
        else: return ""
    #def _set_note_text(self, value):
        #self._note_text = value
    cliente = property(_cliente)


    def _get_note_fornitore(self):
        if self._note_fornitore:
            return self._note_fornitore
        else:
            if self.nota_scheda: return self.nota_scheda.note_fornitore
            else: return ""
    def _set_note_fornitore(self, value):
        self._note_fornitore = value
    note_fornitore = property(_get_note_fornitore, _set_note_fornitore)

    def _get_note_spedizione(self):
        if self._note_spedizione:
            return self._note_spedizione
        else:
            if self.nota_scheda: return self.nota_scheda.note_spedizione
            else: return ""
    def _set_note_spedizione(self, value):
        self._note_spedizione = value
    note_spedizione = property(_get_note_spedizione, _set_note_spedizione)

    def righeSchedaDel(self, id=None):
        """Cancella le righe associate ad un documento"""
        row = RigaSchedaOrdinazione().select(idSchedaOrdinazione= id,
                                                    batchSize = None)
        if row:
            for r in row:
                rowsconto = ScontoRigaScheda().select(idRigaScheda= r.id,
                                                    batchSize = None)
                for ro in rowsconto:
                    params['session'].delete(ro)
                    params["session"].commit()
                params['session'].delete(r)
            params["session"].commit()

            return True

    def scontiSchedaOrdinazioneDel(self, id=None):
        """Cancella gli sconti associati ad una scheda ordinazione"""
        row = ScontoSchedaOrdinazione().select(idScontoSchedaOrdinazione= id,
                                                        batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def promemoriaSchedaDel(self,id=None):
        """Cancella gli sconti legati ad una riga movimento"""
        row = PromemoriaSchedaOrdinazione().select(idPromemoria= id,
                                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def persist(self):
        params["session"].add(self)
        params["session"].commit()
        #cancellazione righe associate alla scheda
        self.righeSchedaDel(self.id)

        #cancellazione sconti associati alla scheda
        self.scontiSchedaOrdinazioneDel(self.id)

        #cancellazione promemoria associati alla scheda
        self.promemoriaSchedaDel(self.id)

        dtt = Datario().select(idScheda=self.id)
        if not dtt:
            dt = Datario()
        else:
            dt = dtt[0]
        dt.matrimonio = self._data_matrimonio
        dt.presa_in_carico = self._data_presa_in_carico
        dt.ordine_al_fornitore = self._data_ordine_al_fornitore
        dt.consegna_bozza =self._data_consegna_bozza
        dt.spedizione = self._data_spedizione
        dt.consegna = self._data_consegna
        dt.ricevuta =  self._data_ricevuta
        dt.id_scheda = self.id
        params["session"].add(dt)
        #params["session"].commit()

        nss = NotaScheda().select(idScheda=self.id)
        if not nss:
            ns = NotaScheda()
        else:
            ns = nss[0]
        ns.note_final = self._note_final
        ns.note_fornitore = self._note_fornitore
        ns.note_spedizione = self._note_spedizione
        ns.note_text =self._note_text
        ns.id_scheda = self.id
        params["session"].add(ns)
        #params["session"].commit()

        rss = RecapitoSpedizione().select(idScheda=self.id)
        if not rss:
            rs = RecapitoSpedizione()
        else:
            rs= rss[0]
        rs.referente = self._referente
        rs.presso = self._presso
        rs.via_piazza = self._via_piazza
        rs.num_civ = self._num_civ
        rs.zip = self._zip
        rs.localita = self._localita
        rs.provincia = self._provincia
        rs.stato = self._stato
        rs.id_scheda = self.id
        params["session"].add(rs)
        #params["session"].commit()

        css = ContattoScheda().select(idScheda=self.id)
        if not css:
            cs = ContattoScheda()
        else:
            cs = css[0]
        cs.referente = self._referente
        cs.prima_email = self._prima_email
        cs.seconda_email = self._seconda_email
        cs.telefono = self._telefono
        cs.cellulare = self._cellulare
        cs.skype = self._skype
        cs.id_scheda = self.id
        params["session"].add(cs)
        #params["session"].commit()

        # salvataggio degli articoli associati alla scheda
        for riga in self.__righeSchedaOrdinazione:
            #riga._resetId()
            riga.id_scheda = self.id
            riga.persist()

        #salvataggio degli sconti associati alla scheda
        if self.scontiSuTotale is not None:
            for scont in self.scontiSuTotale:
                #annullamento id dello sconto
                #scont._resetId()
                #associazione allo sconto della testata
                scont.id_scheda_ordinazione = self.id
                #salvataggio sconto
                scont.persist()
        params["session"].commit()


    def filter_values(self,k,v):
        if k=="id":
            dic= {k:schedaordinazione.c.id ==v}
        elif k == 'daDataMatrimonio':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.matrimonio >= v)}
        elif k== 'aDataMatrimonio':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.matrimonio <= v)}
        elif k == 'daNumero':
            dic = {k:schedaordinazione.c.numero >= v}
        elif k== 'aNumero':
            dic = {k:schedaordinazione.c.numero <= v}
        elif k == 'daDataSpedizione':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.spedizione >= v)}
        elif k== 'aDataSpedizione':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.spedizione <= v)}
        elif k == 'daDataScheda':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.presa_in_carico >= v)}
        elif k== 'aDataScheda':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.presa_in_carico <= v)}
        elif k == 'daDataConsegna':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.consegna >= v)}
        elif k== 'aDataConsegna':
            dic = {k:and_(Datario.id_scheda==schedaordinazione.c.id,Datario.consegna <= v)}
        elif k== 'codiceSpedizione':
            dic = {k:schedaordinazione.c.codice_spedizione.ilike("%"+v+"%")}
        elif k== 'coloreStampa':
            dic = {k:schedaordinazione.c.id_colore_stampa==v}
        elif k== 'carattereStampa':
            dic = {k:schedaordinazione.c.id_carattere_stampa==v}
        elif k== 'nomiSposi':
            dic = {k:schedaordinazione.c.nomi_sposi.ilike("%"+v+"%")}
        elif k== 'referente':
            dic = {k:and_(ContattoScheda.id_scheda==schedaordinazione.c.id,ContattoScheda.referente.ilike("%"+v+"%"))}
        elif k== 'ricevutaAssociata':
            dic = {k:schedaordinazione.c.ricevuta_associata.ilike("%"+v+"%")}
        elif k== 'schedeAperte':
            dic = {k:schedaordinazione.c.fattura ==v}
        elif k == 'idArticolo':
            dic = {k: and_(Articolo.id ==Riga.id_articolo,
                            Riga.id==RigaSchedaOrdinazione.id,
                            RigaSchedaOrdinazione.id_scheda == SchedaOrdinazione.id,
                            Articolo.id ==v),
                                }
        return  dic[k]

schedaordinazione=Table('schede_ordinazioni',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

std_mapper = mapper(SchedaOrdinazione, schedaordinazione, properties={
                "cli":relation(Cliente,primaryjoin=
                    schedaordinazione.c.id_cliente==Cliente.id, backref="sched_ord"),
                "CARATTSTAM":relation(CarattereStampa,primaryjoin=
                    schedaordinazione.c.id_carattere_stampa==CarattereStampa.id, backref="sched_ord"),
                "COLOSTAMP":relation(ColoreStampa,primaryjoin=
                    schedaordinazione.c.id_colore_stampa==ColoreStampa.id, backref="sched_ord"),
                "magazz":relation(Magazzino,primaryjoin=
                    schedaordinazione.c.id_magazzino==Magazzino.id, backref="sched_ord"),
                "promemo":relation(PromemoriaSchedaOrdinazione,primaryjoin=
                    schedaordinazione.c.id==PromemoriaSchedaOrdinazione.id_scheda, backref="sched_ord"),
                "datar":relation(Datario,primaryjoin=
                    Datario.id_scheda==schedaordinazione.c.id,
                    cascade="all, delete",
                    backref="sched_ord", uselist=False),
                "cont_sched":relation(ContattoScheda,primaryjoin=
                    ContattoScheda.id_scheda==schedaordinazione.c.id,
                    cascade="all, delete",
                    backref="sched_ord", uselist=False),
               "recapito_sped":relation(RecapitoSpedizione,primaryjoin=
                    RecapitoSpedizione.id_scheda==schedaordinazione.c.id,
                    cascade="all, delete",
                    backref="sched_ord", uselist=False),
                "nota_scheda":relation(NotaScheda,primaryjoin=
                    NotaScheda.id_scheda==schedaordinazione.c.id,
                    cascade="all, delete",
                    backref="sched_ord", uselist=False) },
                order_by=desc(schedaordinazione.c.id))

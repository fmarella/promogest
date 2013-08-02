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
from promogest.lib.migrate import *
from promogest.Environment import *

try:
    t_testata_movimento = Table('testata_movimento',
                            params['metadata'],
                            schema=params['schema'],
                            autoload=True)
except:
    from data.testataMovimento import t_testata_movimento

from Dao import Dao
from DaoUtils import *
from promogest.dao.Articolo import Articolo
from promogest.dao.Multiplo import Multiplo
from promogest.dao.RigaMovimento import RigaMovimento, t_riga_movimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Riga import Riga
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
#from promogest.dao.RigaMovFornituraRigaMovVendita import RMovFornituraRMovVendita
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from Fornitore import Fornitore
from Cliente import Cliente, t_cliente
from Fornitura import Fornitura
from Operazione import Operazione
from ScontoFornitura import ScontoFornitura
from promogest.dao.Magazzino import Magazzino
from promogest.lib.utils import *
if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo



class TestataMovimento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__righeMovimento = []
        self.__dbRigheMovimento = []
        #setattr(self, "rev",False)

    @reconstructor
    def init_on_load(self):
        self.__righeMovimento = []
        self.__dbRigheMovimento = []
        #setattr(self, "rev",False)


    def _getRigheMovimento(self):
        #if not self.__righeMovimento:
        self.__dbRigheMovimento = self.rigamov
        self.__righeMovimento = self.__dbRigheMovimento[:]
        if self.operazione == "Trasferimento merce magazzino" and self.id_to_magazzino:
            for r in self.__righeMovimento[:]:
                if r.id_magazzino==self.id_to_magazzino:
                    self.__righeMovimento.remove(r)
                else:
                    if r.quantita <0:
                        r.quantita= -1*r.quantita
        if self.operazione == "Carico da composizione kit":
            for r in self.__righeMovimento[:]:
                if r.quantita <0:
                    self.__righeMovimento.remove(r)
        if self.operazione == "Scarico Scomposizione kit":

            for r in self.__righeMovimento[:]:
                if "$SSK$" in r.descrizione:
                    self.__righeMovimento.remove(r)
                else:
                    if r.quantita <0:
                        r.quantita= -1*r.quantita
                        #self.rev = True

        return self.__righeMovimento

    def _setRigheMovimento(self, value):
        self.__righeMovimento = value

    righe = property(_getRigheMovimento, _setRigheMovimento)

    def _segno_operazione(self):
        if self.opera: return self.opera.segno
        else: return ""
    segnoOperazione = property(_segno_operazione)

    def _ragioneSocialeFornitore(self):
        if self.forni: return self.forni.ragione_sociale
        else: return ""
    ragione_sociale_fornitore = property(_ragioneSocialeFornitore)

    def _ragioneSocialeCliente(self):
        if self.cli: return self.cli.ragione_sociale
        else: return ""
    ragione_sociale_cliente= property(_ragioneSocialeCliente)

    def _cognome_cliente(self):
        if self.cli: return self.cli.cognome
        else: return ""
    cognome_cliente= property(_cognome_cliente)

    def _nome_cliente(self):
        if self.cli: return self.cli.nome
        else: return ""
    nome_cliente= property(_nome_cliente)

    def _cognome_fornitore(self):
        if self.forni: return self.forni.cognome
        else: return ""
    cognome_fornitore= property(_cognome_fornitore)

    def _nome_fornitore(self):
        if self.forni: return self.forni.nome
        else: return ""
    nome_fornitore= property(_nome_fornitore)

    def _to_magazzino(self):
        if self.id_to_magazzino:
            a = Magazzino().getRecord(id=self.id_to_magazzino)
            return a.denominazione
        else: return ""
    tomagazzino= property(_to_magazzino)



    def _getNumeroMagazzini(self):
        """
        Restituisce il numero di magazzini presenti nel documento. Ci serve per poter effettuare
        il trasferimento di articoli che partono tutti dallo stesso magazzino
        """
        __numeroMagazzini = []
        for riga in self.righe:
            if riga.id_magazzino not in __numeroMagazzini:
                __numeroMagazzini.append(riga.id_magazzino)
        return len(__numeroMagazzini)

    numeroMagazzini = property(_getNumeroMagazzini)

    def filter_values(self,k,v):
        if k == 'daNumero':
            dic = {k:t_testata_movimento.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:t_testata_movimento.c.numero <= v}
        elif k == 'daParte':
            dic = {k:t_testata_movimento.c.parte >= v}
        elif k == 'aParte':
            dic = {k:t_testata_movimento.c.parte <= v}
        elif k == 'daData':
            dic = {k:t_testata_movimento.c.data_movimento >= v}
        elif k == 'aData':
            dic = {k:t_testata_movimento.c.data_movimento <= v}
        elif k == 'idOperazione':
            dic = {k:t_testata_movimento.c.operazione == v}
        elif k == 'idMagazzino':
            dic = {k:t_testata_movimento.c.id.in_(select([RigaMovimento.id_testata_movimento],
                     and_(Riga.id==RigaMovimento.id,Riga.id_magazzino== v)))}
        elif k == 'idMagazzinoList':
            dic = {k:t_testata_movimento.c.id.in_(select([RigaMovimento.id_testata_movimento],
                     and_(Riga.id==RigaMovimento.id,Riga.id_magazzino.in_(v))))}
        elif k == 'idCliente':
            dic = {k:t_testata_movimento.c.id_cliente == v}
        elif k == 'idClienteList':
            dic = {k:and_(t_testata_movimento.c.id_cliente.in_(v))}
        elif k == 'idFornitore':
            dic = {k:t_testata_movimento.c.id_fornitore == v}
        elif k == 'dataMovimento':
            dic = {k: t_testata_movimento.c.data_movimento == v}
        elif k == 'registroNumerazione':
            dic = {k:t_testata_movimento.c.registro_numerazione==v}
        elif k == 'id_testata_documento':
            dic = {k:t_testata_movimento.c.id_testata_documento ==v}
        elif k == 'idTestataDocumento':
            dic = {k:t_testata_movimento.c.id_testata_documento ==v}
        elif k == 'idArticolo':
            dic = {k:and_(RigaMovimento.id_testata_movimento == TestataMovimento.id,
                            Riga.id==RigaMovimento.id,
                            Articolo.id ==Riga.id_articolo,
                           Articolo.id ==v)}
        elif k == 'idArticoloList':
            dic = {k: and_(RigaMovimento.id_testata_movimento==TestataMovimento.id,
                           Riga.id==RigaMovimento.id,
                           Articolo.id==Riga.id_articolo,
                           Articolo.id.in_(v))}
        return  dic[k]

    def righeMovimentoDel(self, sm = False):
        """
        Cancella le righe associate ad un documento
        """

        self.rmfv= None
        row = self.rigamov
        if row :
            #sm = posso("SM")
            gl = setconf("General", "gestione_lotti")
            lt = setconf("Documenti", "lotto_temp")
            for r in row:
                if r.SCM:
                    for a in r.SCM:
                        params['session'].delete(a)
                if sm:
                    mp = MisuraPezzo().select(idRiga=r.id, batchSize=None)
                    if mp:
                        for m in mp:
                            params['session'].delete(m)
                if gl:
                    rmfa = r.rmfac
                    if rmfa:
                        for f in rmfa:
                            params['session'].delete(f)
                    rmfve = r.rmfve
                    if rmfve:
                        for p in rmfve:
                            params["session"].delete(p)
                #nn = NumeroLottoTemp().select(idRigaMovimentoVenditaTemp=r.id)
                if lt:
                    nn = r.NLT
                    if nn:
                        for n in nn:
                            params["session"].delete(n)
                        #params["session"].commit()
                params['session'].delete(r)
            #params["session"].commit()
        return True

    def persist(self):
        """cancellazione righe associate alla testata
            conn.execStoredProcedure('RigheMovimentoDel',(self.id, ))"""
        if not self.numero:
            valori = numeroRegistroGet(tipo="Movimento", date=self.data_movimento)
            self.numero = valori[0]
            self.registro_numerazione= valori[1]
        params["session"].add(self)


        sm = posso("SM")
        if self.righeMovimento:
            self.righeMovimentoDel(sm=sm)
            if self.operazione == "Carico da composizione kit":
                #print "DEVO AGGIUNGERE IN NEGATIVO LE RIGHE KIT"
                righeMov = []
                for riga in self.righeMovimento:
                    arto = Articolo().getRecord(id=riga.id_articolo)
                    #print "KIT", arto.articoli_kit
                    for art in arto.articoli_kit:
                        #print art.id_articolo_filler, art.quantita
                        a = leggiArticolo(art.id_articolo_filler)
                        r = RigaMovimento()
                        r.valore_unitario_netto = 0
                        r.valore_unitario_lordo = 0
                        r.quantita = -1*(art.quantita*riga.quantita)
                        r.moltiplicatore = 1
                        r.applicazione_sconti = riga.applicazione_sconti
                        r.sconti = []
                        r.percentuale_iva = a["percentualeAliquotaIva"]
                        r.descrizione  = a["denominazione"]
                        r.id_articolo = art.id_articolo_filler
                        r.id_magazzino = riga.id_magazzino
                        r.id_multiplo = riga.id_multiplo
                        r.id_listino = riga.id_listino
                        r.id_iva = a["idAliquotaIva"]
                        r.id_riga_padre = riga.id_riga_padre
                        r.scontiRigheMovimento = riga.scontiRigheMovimento
                        righeMov.append(r)
                self.righeMovimento = self.righeMovimento+righeMov
            if self.operazione == "Scarico Scomposizione kit":
                #print "DEVO AGGIUNGERE IN NEGATIVO LE RIGHE KIT"
                righeMov = []
                for riga in self.righeMovimento:
                    arto = Articolo().getRecord(id=riga.id_articolo)
                    #print "KIT", arto.articoli_kit
                    for art in arto.articoli_kit:
                        print art.id_articolo_filler, art.quantita
                        a = leggiArticolo(art.id_articolo_filler)
                        r = RigaMovimento()
                        r.valore_unitario_netto = 0
                        r.valore_unitario_lordo = 0
                        r.quantita = art.quantita*riga.quantita
                        r.moltiplicatore = 1
                        r.applicazione_sconti = riga.applicazione_sconti
                        r.sconti = []
                        r.percentuale_iva = a["percentualeAliquotaIva"]
                        r.descrizione  = a["denominazione"] +" $SSK$"
                        r.id_articolo = art.id_articolo_filler
                        r.id_magazzino = riga.id_magazzino
                        r.id_multiplo = riga.id_multiplo
                        r.id_listino = riga.id_listino
                        r.id_iva = a["idAliquotaIva"]
                        r.id_riga_padre = riga.id_riga_padre
                        r.scontiRigheMovimento = riga.scontiRigheMovimento
                        righeMov.append(r)
                    riga.quantita = -1*riga.quantita
                self.righeMovimento = self.righeMovimento+righeMov
            if self.operazione == "Trasferimento merce magazzino" and self.id_to_magazzino:
                righeMov = []
                for riga in self.righeMovimento:
                    r = RigaMovimento()
                    r.valore_unitario_netto = riga.valore_unitario_netto
                    r.valore_unitario_lordo = riga.valore_unitario_lordo
                    r.quantita = riga.quantita
                    r.moltiplicatore = riga.moltiplicatore
                    r.applicazione_sconti = riga.applicazione_sconti
                    r.sconti = riga.sconti
                    r.percentuale_iva = riga.percentuale_iva
                    r.descrizione  = riga.descrizione
                    r.id_articolo = riga.id_articolo
                    r.id_magazzino = self.id_to_magazzino
                    r.id_multiplo = riga.id_multiplo
                    r.id_listino = riga.id_listino
                    r.id_iva = riga.id_iva
                    r.id_riga_padre = riga.id_riga_padre
                    r.scontiRigheMovimento = riga.scontiRigheMovimento
                    righeMov.append(r)
                    riga.quantita = -1*riga.quantita
                self.righeMovimento = self.righeMovimento+righeMov
            #sm = posso("SM")
            lt = setconf("Documenti", "lotto_temp")
            gl = setconf("General", "gestione_lotti")
            for riga in self.righeMovimento:
                if "RigaDocumento" in str(riga.__module__):
                    riga.id_testata_documento = self.id_testata_documento
                    riga.persist(sm=sm)
                else:
                    #se non ho un id salvo il dao e me ne faccio dare uno
                    if not self.id:
                        params["session"].commit()
                    riga.id_testata_movimento = self.id
                    # vado a salvare le righe movimento
                    riga.persist(sm=sm)
                    datta = self.data_movimento
                    if hasattr(riga,"data_prezzo") and riga.data_prezzo is not None:
                        datta = stringToDateTime(riga.data_prezzo)
                    if self.id_fornitore and riga.id_articolo:
                        fors = Fornitura().select(idArticolo=riga.id_articolo,
                                                    idFornitore=self.id_fornitore,
                                                    dataPrezzo =  datta,
                                                    orderBy = 'data_fornitura DESC',
                                                    batchSize = None)
                        if fors:
                            #if len(fors) >1:
                                #fors[0].delete()
                            daoFornitura = fors[0]
                        else:
                            daoFornitura = Fornitura()

                        if hasattr(riga,"data_prezzo") and riga.data_prezzo is not None and riga.data_prezzo != "":
                            daoFornitura.data_prezzo = stringToDateTime(riga.data_prezzo)
                        if hasattr(riga, "ordine_minimo") and riga.ordine_minimo is not None and riga.ordine_minimo != "":
                            daoFornitura.scorta_minima = int(riga.ordine_minimo)
                        if hasattr(riga, "tempo_arrivo") and riga.tempo_arrivo is not None and riga.tempo_arrivo != "":
                            daoFornitura.tempo_arrivo_merce = int(riga.tempo_arrivo)
                        if hasattr(riga,"numero_lotto"):
                            daoFornitura.numero_lotto = riga.numero_lotto or ""
                        if hasattr(riga, "data_scadenza"):
                            daoFornitura.data_scadenza = stringToDate(riga.data_scadenza) or None
                        if hasattr(riga, "data_produzione"):
                            daoFornitura.data_produzione = stringToDate(riga.data_produzione) or None

                        daoFornitura.data_fornitura = self.data_movimento
                        daoFornitura.fornitore_preferenziale = True
                        daoFornitura.id_fornitore = self.id_fornitore
                        daoFornitura.id_articolo = riga.id_articolo
                        if not daoFornitura.data_prezzo:
                            daoFornitura.data_prezzo = self.data_movimento
                        if "_RigaMovimento__codiceArticoloFornitore" in riga.__dict__:
                            daoFornitura.codice_articolo_fornitore = riga.__dict__["_RigaMovimento__codiceArticoloFornitore"]
                        daoFornitura.prezzo_lordo = riga.valore_unitario_lordo
                        daoFornitura.prezzo_netto = riga.valore_unitario_netto
                        daoFornitura.percentuale_iva = riga.percentuale_iva
                        daoFornitura.applicazione_sconti = riga.applicazione_sconti
                        sconti = []
                        for s in riga.sconti:
                            daoSconto = ScontoFornitura()
                            daoSconto.id_fornitura = daoFornitura.id
                            daoSconto.valore = s.valore
                            daoSconto.tipo_sconto = s.tipo_sconto
                            sconti.append(daoSconto)

                        daoFornitura.sconti = sconti
                        params["session"].add(daoFornitura)
                        params["session"].commit()
                        if gl:
                            #cambiata la logica, adesso le righe su rmf sono sempre e solo una
                            #viene gestita invece un'altra tabella di raccordo per le quantità
                            a = RigaMovimentoFornitura()
                            a.id_articolo = riga.id_articolo
                            a.id_riga_movimento_acquisto = riga.id
                            a.id_fornitura = daoFornitura.id
                            params["session"].add(a)
                            #params["session"].commit()

                    elif gl:
                        if hasattr(riga,"righe_movimento_fornitura"):
                            for g in riga.righe_movimento_fornitura:
                                a = RigaMovimentoFornitura()
                                a.id_articolo = riga.id_articolo
                                a.id_riga_movimento_vendita = riga.id
                                a.id_fornitura = g
                                params["session"].add(a)
                            #params["session"].commit()

                        if lt and hasattr(riga,"lotto_temp") and riga.lotto_temp:
                            # Salvare il lotto temporaneo
                            n = NumeroLottoTemp()
                            n.id_riga_movimento_vendita_temp = riga.id
                            n.lotto_temp = riga.lotto_temp
                            params["session"].add(n)
            params["session"].commit()
        self.init_on_load()


if "id_to_magazzino" not in [c.name for c in t_testata_movimento.columns]:
    col = Column('id_to_magazzino', Integer)
    col.create(t_testata_movimento)

std_mapper = mapper(TestataMovimento, t_testata_movimento,properties={
        "rigamov": relation(RigaMovimento,primaryjoin=
                t_testata_movimento.c.id==t_riga_movimento.c.id_testata_movimento,
                cascade="all, delete",
                backref="testata_movimento"),
        #"fornitore": relation(Fornitore, backref="testata_movimento"),
        "forni":relation(Fornitore,primaryjoin=
                    (t_testata_movimento.c.id_fornitore==Fornitore.id), backref="testata_movimento"),
        "cli":relation(Cliente,primaryjoin=
                    (t_testata_movimento.c.id_cliente==t_cliente.c.id), backref="testata_movimento"),
        "opera": relation(Operazione,primaryjoin = (t_testata_movimento.c.operazione==Operazione.denominazione),backref="testata_movimento"),
        }, order_by=t_testata_movimento.c.id)

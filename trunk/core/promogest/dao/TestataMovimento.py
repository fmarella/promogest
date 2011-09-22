# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from migrate import *
from promogest.Environment import *
from Dao import Dao
from DaoUtils import *
from promogest.dao.Articolo import Articolo
from promogest.dao.Multiplo import Multiplo
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Riga import Riga
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.ui.utils import numeroRegistroGet
from Fornitore import Fornitore
from Cliente import Cliente
from Fornitura import Fornitura
from Operazione import Operazione
from ScontoFornitura import ScontoFornitura
from promogest.ui.utils import *
if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo



class TestataMovimento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__righeMovimento = []
        self.__dbRigheMovimento = []

    @reconstructor
    def init_on_load(self):
        self.__righeMovimento = []
        self.__dbRigheMovimento = []

    def _getRigheMovimento(self):
        #if not self.__righeMovimento:
        self.__dbRigheMovimento = params['session'].query(RigaMovimento)\
                                        .with_parent(self)\
                                        .filter_by(id_testata_movimento=self.id)\
                                        .all()

        self.__righeMovimento = self.__dbRigheMovimento[:]
        if self.operazione == "Trasferimento merce magazzino" and self.id_to_magazzino:
            for r in self.__righeMovimento[:]:
                if r.id_magazzino==self.id_to_magazzino:
                    self.__righeMovimento.remove(r)
                else:
                    if r.quantita <0:
                        setattr(r, "reversed", True)
                        r.quantita= -1*r.quantita
        if self.operazione == "Carico da composizione kit":
            for r in self.__righeMovimento[:]:
                if r.quantita <0:
                    self.__righeMovimento.remove(r)
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
            dic = {k:testata_mov.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:testata_mov.c.numero <= v}
        elif k == 'daParte':
            dic = {k:testata_mov.c.parte >= v}
        elif k == 'aParte':
            dic = {k:testata_mov.c.parte <= v}
        elif k == 'daData':
            dic = {k:testata_mov.c.data_movimento >= v}
        elif k == 'aData':
            dic = {k:testata_mov.c.data_movimento <= v}
        elif k == 'idOperazione':
            dic = {k:testata_mov.c.operazione == v}
        elif k == 'idMagazzino':
            dic = {k:testata_mov.c.id.in_(select([RigaMovimento.id_testata_movimento],and_(Riga.id==RigaMovimento.id,Riga.id_magazzino== v)))}
        elif k == 'idMagazzinoList':
            dic = {k:testata_mov.c.id.in_(select([RigaMovimento.id_testata_movimento],and_(Riga.id==RigaMovimento.id,Riga.id_magazzino.in_(v))))}
        elif k == 'idCliente':
            dic = {k:testata_mov.c.id_cliente == v}
        elif k == 'idClienteList':
            dic = {k:and_(testata_mov.c.id_cliente.in_(v))}
        elif k == 'idFornitore':
            dic = {k:testata_mov.c.id_fornitore == v}
        elif k == 'dataMovimento':
            dic = {k: testata_mov.c.data_movimento == v}
        elif k == 'registroNumerazione':
            dic = {k:testata_mov.c.registro_numerazione==v}
        elif k == 'id_testata_documento':
            dic = {k:testata_mov.c.id_testata_documento ==v}
        elif k == 'idTestataDocumento':
            dic = {k:testata_mov.c.id_testata_documento ==v}
        elif k == 'idArticolo':
            dic = {k:and_(RigaMovimento.id_testata_movimento == TestataMovimento.id,
                            Riga.id==RigaMovimento.id,
                            Articolo.id ==Riga.id_articolo,
                           Articolo.id ==v)}

        return  dic[k]

    def righeMovimentoDel(self,id=None):
        """
        Cancella le righe associate ad un documento
        """
        #from promogest.dao.RigaMovimento import RigaMovimento
        row = RigaMovimento().select(idTestataMovimento= id,
                                    offset = None,
                                    batchSize = None)
        self.rmfv= None
        if row:
            self.rmfv = RigaMovimentoFornitura().select(idRigaMovimentoVenditaBool = True, batchSize=None)
            sm = posso("SM")
            for r in row:
                if sm:
                    mp = MisuraPezzo().select(idRiga=r.id, batchSize=None)
                    if mp:
                        for m in mp:
                            params['session'].delete(m)
                        params["session"].commit()
                rmfa = RigaMovimentoFornitura().select(idRigaMovimentoAcquisto = r.id, batchSize=None)
                if rmfa:
                    for f in rmfa:
                        params['session'].delete(f)
                    params["session"].commit()
                precedentiRighe= RigaMovimentoFornitura().select(idRigaMovimentoVendita=r.id, batchSize=None)
                if precedentiRighe:
                    for p in precedentiRighe:
                        p.id_riga_movimento_vendita = None
                        params["session"].add(p)
                    params['session'].commit()
                params['session'].delete(r)
            params["session"].commit()
        return True


    def persist(self):
        """cancellazione righe associate alla testata
            conn.execStoredProcedure('RigheMovimentoDel',(self.id, ))"""
        pg2log.info("DENTRO IL TESTATA MOVIMENTO")
        print "INIZIO SALVATAGGIO MOVIMENTO", tempo()
        if not self.numero:
            valori = numeroRegistroGet(tipo="Movimento", date=self.data_movimento)
            self.numero = valori[0]
            self.registro_numerazione= valori[1]
        params["session"].add(self)
        params["session"].commit()
        if self.righeMovimento:
            self.righeMovimentoDel(id=self.id)
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
            sm = posso("SM")
            for riga in self.righeMovimento:
                if "RigaDocumento" in str(riga.__module__):
                    riga.persist()
                else:
                    #print "DEEEEEEEEEEEEEEFI", riga.id, riga.quantita, riga.id_articolo, riga.descrizione
                    riga._resetId()
                    riga.id_testata_movimento = self.id
                    riga.persist(sm=sm)
                    if self.id_fornitore and riga.id_articolo:
                        if hasattr(riga,"data_prezzo"):
                            data_prezzo = stringToDateTime(riga.data_prezzo) or stringToDateTime(self.data_movimento)
                        else:
                            data_prezzo = stringToDateTime(self.data_movimento)
                        """aggiornamento forniture cerca la fornitura relativa al fornitore
                            con data <= alla data del movimento"""
                        fors = Fornitura().select(idArticolo=riga.id_articolo,
                                                    idFornitore=self.id_fornitore,
                                                    daDataPrezzo=None,
                                                    aDataPrezzo= data_prezzo,
                                                    orderBy = 'data_prezzo DESC',
                                                    offset = None,
                                                    batchSize = None)
                        if not fors:
                            # a causa dell'aggiunta di lotti e scadenze, qui è necessario
                            # controllare anche per data prezzo
                            fors = Fornitura().select(idArticolo=riga.id_articolo,
                                                        idFornitore=self.id_fornitore,
                                                        #daDataPrezzo=None,
                                                        aDataFornitura = data_prezzo,
                                                        orderBy = 'data_fornitura DESC',
                                                        offset = None,
                                                        batchSize = None)
                        daoFornitura = None
                        if fors:
                            if fors[0].data_prezzo == data_prezzo:
                                # ha trovato una fornitura con stessa data: aggiorno questa fornitura
                                #daoFornitura = Fornitura().getRecord(id=fors[0].id)
                                daoFornitura = fors[0]
                            else:
                                """creo una nuova fornitura con data_prezzo pari alla data del movimento
                                    copio alcuni dati dalla fornitura piu' prossima"""
                                daoFornitura = Fornitura()
                        else:
                            # nessuna fornitura utilizzabile, ne creo una nuova (alcuni dati mancheranno)
                            daoFornitura = Fornitura()
                        if hasattr(riga, "ordine_minimo") and riga.ordine_minimo:
                            daoFornitura.scorta_minima = int(riga.ordine_minimo)
                        #daoFornitura.id_multiplo = None
                        if hasattr(riga, "tempo_arrivo") and riga.tempo_arrivo:
                            daoFornitura.tempo_arrivo_merce = int(riga.tempo_arrivo)
                        daoFornitura.fornitore_preferenziale = True
                        if hasattr(riga,"numero_lotto"):
                            daoFornitura.numero_lotto = riga.numero_lotto or ""
                        if hasattr(riga, "data_scadenza"):
                            daoFornitura.data_scadenza = stringToDate(riga.data_scadenza) or None
                        if hasattr(riga, "data_produzione"):
                            daoFornitura.data_produzione = stringToDate(riga.data_produzione) or None
                        if hasattr(riga,"data_prezzo"):
                            daoFornitura.data_prezzo = data_prezzo
                        if not daoFornitura.data_prezzo:
                            daoFornitura.data_prezzo = stringToDateTime(self.data_movimento)
                        daoFornitura.id_fornitore = self.id_fornitore
                        daoFornitura.id_articolo = riga.id_articolo
                        if daoFornitura.data_fornitura is not None:
                            if self.data_movimento > daoFornitura.data_fornitura:
                                daoFornitura.data_fornitura = self.data_movimento
                        else:
                            daoFornitura.data_fornitura = self.data_movimento
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
                    if self.id_fornitore and riga.id_articolo:
                        for q in range(0,riga.quantita):
                            a = RigaMovimentoFornitura()
                            a.id_articolo = riga.id_articolo
                            a.id_riga_movimento_acquisto = riga.id
                            if self.rmfv:
                                for v in self.rmfv:
                                    if v.id_articolo==riga.id_articolo and v.id_fornitura == daoFornitura.id:
                                        a.id_riga_movimento_vendita = v.id_riga_movimento_vendita
                                        self.rmfv.remove(v)
                            a.id_fornitura = daoFornitura.id
                            params["session"].add(a)
                        params["session"].commit()
                    else:
                        if hasattr(riga,"righe_movimento_fornitura"):
                            if riga.righe_movimento_fornitura:
                                precedentiRighe= RigaMovimentoFornitura().select(idRigaMovimentoVendita=riga.id, batchSize=None)
                                if precedentiRighe:
                                    for p in precedentiRighe:
                                        p.id_riga_movimento_vendita = None
                                        params["session"].add(p)
                                    params["session"].commit()
                                for r in riga.righe_movimento_fornitura:
                                    r.id_riga_movimento_vendita = riga.id
                                    params["session"].add(r)
                                params["session"].commit()
                        #print "E una vendita"
            print "DOPO il for generale di riga movimento", tempo()
            self.__righeMovimento = []

#riga=Table('riga',params['metadata'],schema = params['schema'],autoload=True)
testata_mov=Table('testata_movimento', params['metadata'],schema = params['schema'],autoload=True)
clie = Table('cliente',params['metadata'],schema = params['schema'],autoload=True)
rigamovi = Table('riga_movimento',params['metadata'],schema = params['schema'],autoload=True)
operaz = Table('operazione',params['metadata'],schema = params['mainSchema'],autoload=True)

if "id_to_magazzino" not in [c.name for c in testata_mov.columns]:
    col = Column('id_to_magazzino', Integer)
    col.create(testata_mov)

std_mapper = mapper(TestataMovimento, testata_mov,properties={
        "rigamov": relation(RigaMovimento,primaryjoin=
                testata_mov.c.id==rigamovi.c.id_testata_movimento,
                cascade="all, delete",
                backref="testata_movimento"),
        #"fornitore": relation(Fornitore, backref="testata_movimento"),
        "forni":relation(Fornitore,primaryjoin=
                    (testata_mov.c.id_fornitore==Fornitore.id), backref="testata_movimento"),
        "cli":relation(Cliente,primaryjoin=
                    (testata_mov.c.id_cliente==clie.c.id), backref="testata_movimento"),
        "opera": relation(Operazione,primaryjoin = (testata_mov.c.operazione==Operazione.denominazione),backref="testata_movimento"),
        }, order_by=testata_mov.c.id)

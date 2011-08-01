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
        if not self.__righeMovimento:
            self.__dbRigheMovimento = params['session'].query(RigaMovimento)\
                                            .with_parent(self)\
                                            .filter_by(id_testata_movimento=self.id)\
                                            .all()
        self.__righeMovimento = self.__dbRigheMovimento[:]
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
            #if self.rmfv:
                #print "QUESTO ARTICOLO è stato venduto", len(self.rmfv), "volte"
            for r in row:
                if posso("SM"):
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
        if not self.numero:
            valori = numeroRegistroGet(tipo="Movimento", date=self.data_movimento)
            self.numero = valori[0]
            self.registro_numerazione= valori[1]
        params["session"].add(self)
        params["session"].commit()
        if self.righeMovimento:
            #print "PRIMA DI CANCELLA RIGHE MOV", tempo()
            self.righeMovimentoDel(id=self.id)
            #print "DOPO CANCELLA RIGHE MOV", tempo()
            for riga in self.righeMovimento:
                if "RigaDocumento" in str(riga.__module__):
                    riga.persist()
                else:
                    #annullamento id della riga
                    riga._resetId()
                    #associazione alla riga della testata
                    riga.id_testata_movimento = self.id
                    #salvataggio riga
                    riga.persist()
                    #print "DOPO il persist della riga", tempo()
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
                                                    aDataPrezzo=   data_prezzo,
                                                    orderBy = 'data_prezzo DESC',
                                                    offset = None,
                                                    batchSize = None)
                        #print "DOPO dopo FORS", fors
                        daoFornitura = None
                        if fors:
                            if fors[0].data_prezzo == data_prezzo:
                                # ha trovato una fornitura con stessa data: aggiorno questa fornitura
                                #pg2log.info("TROVATO UNA FORNITURA CON STESSA DATA: AGGIORNO QUESTA FORNITURA")
                                daoFornitura = Fornitura().getRecord(id=fors[0].id)
                            else:
                                """creo una nuova fornitura con data_prezzo pari alla data del movimento
                                    copio alcuni dati dalla fornitura piu' prossima"""
                                #pg2log.info("CREO UNA NUOVA FORNITURA CON DATA_PREZZO PARI ALLA DATA DEL MOVIMENTO COPIO ALCUNI DATI DALLA FORNITURA PIU' PROSSIMA")
                                daoFornitura = Fornitura()
                        else:
                            # nessuna fornitura utilizzabile, ne creo una nuova (alcuni dati mancheranno)
                            #pg2log.info("NESSUNA FORNITURA UTILIZZABILE, NE CREO UNA NUOVA (ALCUNI DATI MANCHERANNO)")
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
                #print "DOPO il for generale di riga movimento", tempo()
            self.__righeMovimento = []

#riga=Table('riga',params['metadata'],schema = params['schema'],autoload=True)
testata_mov=Table('testata_movimento', params['metadata'],schema = params['schema'],autoload=True)
clie = Table('cliente',params['metadata'],schema = params['schema'],autoload=True)
rigamovi = Table('riga_movimento',params['metadata'],schema = params['schema'],autoload=True)
operaz = Table('operazione',params['metadata'],schema = params['mainSchema'],autoload=True)

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

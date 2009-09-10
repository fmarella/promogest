#-*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
"""


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from DaoUtils import *
from Multiplo import Multiplo
from RigaMovimento import RigaMovimento
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

    def __init__(self, arg=None):
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
            dic = {k:testata_mov.c.id.in_(select([RigaMovimento.id_testata_movimento],RigaMovimento.id_magazzino== v))}
        elif k == 'idCliente':
            dic = {k:testata_mov.c.id_cliente == v}
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
            #'statoDocumento': testata_mov.c.stato_documento == v,
            #'idArticolo': testata_movimento.c.id_articolo == v  ARRIVANO QUI TRAMITE RIGA - RIGA DOCUMENTO
        return  dic[k]

    def righeMovimentoDel(self,id=None):
        """
        Cancella le righe associate ad un documento
        """
        #from promogest.dao.RigaMovimento import RigaMovimento
        row = RigaMovimento().select(idTestataMovimento= id,
                                    offset = None,
                                    batchSize = None
)
        if row:
            for r in row:
                if "SuMisura" in modulesList:
                    mp = MisuraPezzo().select(idRiga=r.id)
                    if mp:
                        for m in mp:
                            params['session'].delete(m)
                        params["session"].commit()
                params['session'].delete(r)
            params["session"].commit()
        return True


    def persist(self):
        """cancellazione righe associate alla testata
            conn.execStoredProcedure('RigheMovimentoDel',(self.id, ))"""
        pg2log.debug("DENTRO IL TESTATA MOVIMENTO")
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
                    if self.id_fornitore is not None and riga.id_articolo:
                        """aggiornamento forniture cerca la fornitura relativa al fornitore
                            con data <= alla data del movimento"""
                        fors = Fornitura().select(idArticolo=riga.id_articolo,
                                                    idFornitore=self.id_fornitore,
                                                    daDataPrezzo=None,
                                                    aDataPrezzo=self.data_movimento,
                                                    orderBy = 'data_prezzo DESC',
                                                    offset = None,
                                                    batchSize = None)
                        #print "DOPO dopo FORS", tempo()
                        daoFornitura = None
                        if fors:
                            if fors[0].data_prezzo == self.data_movimento:
                                # ha trovato una fornitura con stessa data: aggiorno questa fornitura
                                pg2log.info("TROVATO UNA FORNITURA CON STESSA DATA: AGGIORNO QUESTA FORNITURA")
                                daoFornitura = Fornitura().getRecord(id=fors[0].id)
                            else:
                                """creo una nuova fornitura con data_prezzo pari alla data del movimento
                                    copio alcuni dati dalla fornitura piu' prossima"""
                                pg2log.info("CREO UNA NUOVA FORNITURA CON DATA_PREZZO PARI ALLA DATA DEL MOVIMENTO COPIO ALCUNI DATI DALLA FORNITURA PIU' PROSSIMA")
                                daoFornitura = Fornitura()
                                daoFornitura.scorta_minima = fors[0].scorta_minima
                                daoFornitura.id_multiplo = fors[0].id_multiplo
                                daoFornitura.tempo_arrivo_merce = fors[0].tempo_arrivo_merce
                                daoFornitura.fornitore_preferenziale = fors[0].fornitore_preferenziale
                        else:
                            # nessuna fornitura utilizzabile, ne creo una nuova (alcuni dati mancheranno)
                            pg2log.info("NESSUNA FORNITURA UTILIZZABILE, NE CREO UNA NUOVA (ALCUNI DATI MANCHERANNO)")
                            daoFornitura = Fornitura()

                        daoFornitura.id_fornitore = self.id_fornitore
                        daoFornitura.id_articolo = riga.id_articolo
                        if daoFornitura.data_fornitura is not None:
                            if self.data_movimento > daoFornitura.data_fornitura:
                                daoFornitura.data_fornitura = self.data_movimento
                        else:
                            daoFornitura.data_fornitura = self.data_movimento
                        daoFornitura.data_prezzo = self.data_movimento
                        daoFornitura.codice_articolo_fornitore = riga.codiceArticoloFornitore
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
                #print "DOPO il for generale di riga movimento", tempo()
            self.__righeMovimento = []
            #params["session"].flush()

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
        "opera": relation(Operazione, backref="testata_movimento"),
        }, order_by=testata_mov.c.id)

# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>

from Dao import Dao

from sqlalchemy import *
from sqlalchemy.orm import *
from ScontoTestataDocumento import ScontoTestataDocumento
from DestinazioneMerce import DestinazioneMerce
from TestataMovimento import TestataMovimento
from Pagamento import Pagamento
from Vettore import Vettore
from promogest.modules.Agenti.dao.Agente import Agente
from Fornitore import Fornitore
from Cliente import Cliente
from RigaDocumento import RigaDocumento
from RigaDocumento import *
from AliquotaIva import AliquotaIva
from RigaMovimento import RigaMovimento
from Banca import Banca
from Riga import Riga
from ScontoRigaMovimento import ScontoRigaMovimento
from TestataDocumentoScadenza import TestataDocumentoScadenza

#from DaoUtils import *
from decimal import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *

from promogest.Environment import *
from promogest import Environment

class TestataDocumento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

        self.__righeDocumento = None
        self.__operazione = None
        self.__dbScadenzeDocumento = []
        self.__ScadenzeDocumento = []
        self.__dbScontiTestataDocumento = []
        self.__scontiTestataDocumento = []
        self.__dbRigheDocumentoPart = []
        self.__dbRigheMovimentoPart = []
        self.__righeDocumento = []
        self._totaleImponibile = 0
        self._totaleNonScontato = 0
        self._totaleScontato = 0
        self._totaleImponibile = 0
        self._totaleImponibileScontato = 0
        self._totaleImposta = 0
        self._totaleImpostaScontata = 0
        self._totaleScontato = 0
        self._castellettoIva = 0
        self.__data_inizio_noleggio = None
        self.__data_fine_noleggio = None
        self.__numeroMagazzini = 0

    @reconstructor
    def init_on_load(self):
        self.__dbScadenzeDocumento = []
        self.__dbScontiTestataDocumento = []
        self.__dbRigheDocumentoPart = []
        self.__dbRigheMovimentoPart = []
        self.__righeDocumento = []
        self.__ScadenzeDocumento = []
        self.__scontiTestataDocumento = []
        self.__data_inizio_noleggio = None
        self.__data_fine_noleggio = None

    def _getScadenzeDocumento(self):
        if self.id:
            self.__dbScadenzeDocumento = params['session']\
                                    .query(TestataDocumentoScadenza)\
                                    .with_parent(self)\
                                    .filter_by(id_testata_documento=self.id)\
                                    .all()
        self.__ScadenzeDocumento = self.__dbScadenzeDocumento[:]
        return self.__ScadenzeDocumento

    def _setScadenzeDocumento(self, value):
        self.__ScadenzeDocumento = value

    #if Environment.conf.hasPagamenti == True:
    scadenze = property(_getScadenzeDocumento, _setScadenzeDocumento)

    def sort_by_attr(self,seq,attr):
        intermed = [ (getattr(seq[i],attr), i, seq[i]) for i in xrange(len(seq)) ]
        intermed.sort()
        return [ tup[-1] for tup in intermed ]

    def _getRigheDocumento(self):
        if self.id:
            self.__dbRigheDocumentoPart = params['session']\
                                        .query(RigaDocumento )\
                                        .filter(RigaDocumento.id_testata_documento == self.id).all()
            self.__dbRigheMovimentoPart = params['session']\
                                        .query(RigaMovimento )\
                                        .join(RigaMovimento.testata_movimento)\
                                        .filter(RigaMovimento.id_testata_movimento==select([TestataMovimento.id], \
                                                TestataMovimento.id_testata_documento==self.id)).all()

            self.__dbRigheDocumento = self.__dbRigheDocumentoPart + self.__dbRigheMovimentoPart
            self.__dbRigheDocumento = self.sort_by_attr(self.__dbRigheDocumento,"id")
            self.__righeDocumento = self.__dbRigheDocumento[:]
        else:
            self.__righeDocumento = []
        return self.__righeDocumento

    def _setRigheDocumento(self, value):
        self.__righeDocumento =value

    righe = property(_getRigheDocumento, _setRigheDocumento)

    def _getDocumentTotalConfections(self):
        """
        Ritorna il numero totale delle confezioni inserite nelle righe del documento:
        quantità Totale = sommatoria(i=1 to n)[quantità(riga i) * moltiplicatore(riga i)]
        """
        __quantitaTotale = 0
        if len(self.righe) > 0:
            for r in self.righe:
                __quantitaTotale += float(r.quantita*r.moltiplicatore)
        return __quantitaTotale

    totalConfections = property(_getDocumentTotalConfections)

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

        #__numeroMagazzini = 0
        
        #if len(self.righe) > 0 and self.id:
          #mov_query = params['session'].query(RigaMovimento.id).filter(RigaMovimento.id_testata_movimento == self.id)
          #doc_query = params['session'].query(RigaDocumento.id).filter(RigaDocumento.id_testata_documento == self.id)
          #res = params['session'].query(Riga.id_magazzino).filter(or_(Riga.id.in_(mov_query),Riga.id.in_(doc_query))).distinct().count()
          #__numeroMagazzini = res
        #return __numeroMagazzini
        
    numeroMagazzini = property(_getNumeroMagazzini)

    def _getScontiTestataDocumento(self):
        if not self.__scontiTestataDocumento and self.id:
            self.__dbScontiTestataDocumento = ScontoTestataDocumento().select(join = ScontoTestataDocumento.TD,
                                                                                idScontoTestataDocumento=self.id,
                                                                                batchSize=None)
        self.__scontiTestataDocumento = self.__dbScontiTestataDocumento
        return self.__scontiTestataDocumento

    def _setScontiTestataDocumento(self, value):
        self.__scontiTestataDocumento = value

    sconti = property(_getScontiTestataDocumento, _setScontiTestataDocumento)

    def _getStringaScontiTestataDocumento(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiTestataDocumento(), self.applicazione_sconti)
        return getStringaSconti(listSconti)
    stringaSconti = property(_getStringaScontiTestataDocumento)


    def _getIntestatario(self):
        """
        Restituisce la ragione sociale o cognome + nome
        se la ragione sociale e' vuota
        """
        intestatario = ''

        if self.id_cliente is not None:
            if (hasattr(self, 'ragione_sociale_cliente') and
                hasattr(self, 'cognome_cliente') and
                hasattr(self, 'nome_cliente')):
                intestatario = self.ragione_sociale_cliente
                if intestatario == '':
                    intestatario = self.cognome_cliente + ' ' + self.nome_cliente
                return intestatario
            else:
                cliente = leggiCliente(self.id_cliente)
                intestatario = cliente['ragioneSociale']
                if intestatario == '':
                    intestatario = cliente['cognome'] + ' ' + cliente['nome']
                return intestatario
        elif self.id_fornitore is not None:
            if (hasattr(self, 'ragione_sociale_fornitore') and
                hasattr(self, 'cognome_fornitore') and
                hasattr(self, 'nome_fornitore')):
                intestatario = self.ragione_sociale_fornitore
                if intestatario == '':
                    intestatario = self.cognome_fornitore + ' ' + self.nome_fornitore
                return intestatario
            else:
                fornitore = leggiFornitore(self.id_fornitore)
                intestatario = fornitore['ragioneSociale']
                if intestatario == '':
                    intestatario = fornitore['cognome'] + ' ' + fornitore['nome']
                return intestatario
        else:
            return ''

    intestatario = property(_getIntestatario, )


    def _getTotaliDocumento(self):
        self.__operazione = leggiOperazione(self.operazione)
        fonteValore = self.__operazione["fonteValore"]

        # FIXME: duplicated in AnagraficaDocumenti.py
        totaleImponibile = Decimal(0)
        totaleImposta = Decimal(0)
        totaleNonScontato = Decimal(0)
        totaleImpostaScontata = Decimal(0)
        totaleImponibileScontato = Decimal(0)
        totaleScontato = Decimal(0)
        castellettoIva = {}
        righeDocumento = self.righe
        for riga in righeDocumento:

            # FIXME: added for supporting dumb rows when printing
            if riga is None:
                continue
            #print "VALORIIIIIIIIIIIIIIIII", riga.quantita, riga.moltiplicatore, riga.valore_unitario_netto
            if not riga.moltiplicatore:
                riga.moltiplicatore = 1
            totaleRiga = Decimal(str(riga.quantita)) * Decimal(str(riga.moltiplicatore)) * mN(str(riga.valore_unitario_netto))
            percentualeIvaRiga = Decimal(str(riga.percentuale_iva))
            if percentualeIvaRiga != Environment.percentualeIvaRiga:
                aliquotaIvaRiga = riga.aliquota
                Environment.percentualeIvaRiga = percentualeIvaRiga
                Environment.aliquotaIvaRiga = aliquotaIvaRiga
            else:
                aliquotaIvaRiga = Environment.aliquotaIvaRiga
            #aliquotaIvaRiga = righeDocumento[i].aliquota


            if (fonteValore == "vendita_iva" or fonteValore == "acquisto_iva"):
                totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga)
            else:
                totaleImponibileRiga = mN(totaleRiga,2)
                totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)

            totaleImpostaRiga = mN(totaleRiga,2) - totaleImponibileRiga
            totaleNonScontato += totaleRiga
            totaleImponibile += totaleImponibileRiga
            totaleImposta += totaleImpostaRiga

            if aliquotaIvaRiga not in castellettoIva.keys():
                castellettoIva[aliquotaIvaRiga] = {'percentuale': percentualeIvaRiga,
                                                    'imponibile': totaleImponibileRiga,
                                                    'imposta': totaleImpostaRiga,
                                                    'totale': totaleRiga}
            else:
                castellettoIva[aliquotaIvaRiga]['percentuale'] = percentualeIvaRiga
                castellettoIva[aliquotaIvaRiga]['imponibile'] += totaleImponibileRiga
                castellettoIva[aliquotaIvaRiga]['imposta'] += totaleImpostaRiga
                castellettoIva[aliquotaIvaRiga]['totale'] += totaleRiga

        totaleNonScontato = mN(totaleNonScontato, 2)
        totaleImponibile = mN(totaleImponibile, 2)
        totaleImposta = totaleNonScontato - totaleImponibile
        for aliquotaIva in castellettoIva:
            castellettoIva[aliquotaIva]['imponibile'] = mN(castellettoIva[aliquotaIva]['imponibile'], 2)
            castellettoIva[aliquotaIva]['imposta'] = mN(castellettoIva[aliquotaIva]['imposta'], 2)
            castellettoIva[aliquotaIva]['totale'] = mN(castellettoIva[aliquotaIva]['totale'], 2)

        totaleImpostaScontata = totaleImposta
        totaleImponibileScontato = totaleImponibile
        totaleScontato = totaleNonScontato
        scontiSuTotale = self.sconti
        applicazioneSconti = self.applicazione_sconti

        if len(scontiSuTotale) > 0:
            for s in scontiSuTotale:
                if s.tipo_sconto == 'percentuale':
                    if applicazioneSconti == 'scalare':
                        totaleScontato = mN(totaleScontato) * (1 - mN(s.valore) / 100)
                    elif applicazioneSconti == 'non scalare':
                        totaleScontato = mN(totaleScontato) - mN(totaleNonScontato) * mN(s.valore) / 100
                    else:
                        raise Exception, ('BUG! Tipo di applicazione sconto '
                                          'sconosciuto: %s' % s.tipo_sconto)
                elif s.tipo_sconto == 'valore':
                    totaleScontato = mN(totaleScontato) - mN(s.valore)

            # riporta l'insieme di sconti ad una percentuale globale
            if totaleNonScontato == 0:
                totaleNonScontato = 1
            percentualeScontoGlobale = (1 - totaleScontato / totaleNonScontato) * 100
            totaleImpostaScontata = 0
            totaleImponibileScontato = 0
            totaleScontato = 0
            # riproporzione del totale, dell'imponibile e dell'imposta
            for k in castellettoIva.keys():
                castellettoIva[k]['totale'] = mN(castellettoIva[k]['totale'] * (1 - mN(percentualeScontoGlobale) / 100), 2)
                castellettoIva[k]['imponibile'] = mN(castellettoIva[k]['imponibile'] * (1 - mN(percentualeScontoGlobale) / 100),2)
                castellettoIva[k]['imposta'] = castellettoIva[k]['totale'] - castellettoIva[k]['imponibile']

                totaleImponibileScontato += castellettoIva[k]['imponibile']
                totaleImpostaScontata += castellettoIva[k]['imposta']

            totaleScontato = mN(totaleImponibileScontato) + mN(totaleImpostaScontata)

        self._totaleNonScontato = mN(totaleNonScontato,2)
        self._totaleScontato = mN(totaleScontato,2)
        self._totaleImponibile = mN(totaleImponibile,2)
        self._totaleImposta = mN(totaleImposta,2)
        self._totaleImponibileScontato = mN(totaleImponibileScontato,2)
        self._totaleImpostaScontata = mN(totaleImpostaScontata,2)
        self._castellettoIva = []
        for k in castellettoIva.keys():
            dictCastellettoIva = castellettoIva[k]
            dictCastellettoIva['aliquota'] = k
            self._castellettoIva.append(dictCastellettoIva)

        return None

    totali = property(_getTotaliDocumento, )

    def contieneMovimentazione(self, righe=None):
        """
            Verifica se sono e devono essere presenti righe di movimentazione magazzino
            dicesi riga di movimentazione se è legata ad una operazione che ha un segno
            sia esso positivo o negativo e deve avere anche un id_articolo abbinato
        """
        righeMovimentazione = False
        operazione = leggiOperazione(self.operazione)
        if operazione["segno"] != '':
            if righe is not None:
                for riga in righe:
                    if riga.id_articolo is not None:
                        righeMovimentazione = True
                        break
        return righeMovimentazione


    #Salvataggi subordinati alla testata Documento, iniziamo da righe documento e poi righe
    def persist(self):
        DaoTestataMovimento = None
        params["session"].add(self)
        params["session"].commit()

        Environment.pg2log.debug("INIZIO SALVATAGGIO DOCUMENTO")
        self.scontiTestataDocumentoDel(id=self.id)
        self.testataDocumentoScadenzaDel(id=self.id)
        self.righeDocumentoDel(id=self.id)
        #verifica se sono presenti righe di movimentazione magazzino
        contieneMovimentazione = self.contieneMovimentazione(righe=self.righeDocumento)
        #cerco le testate movimento associate al documento
        #FIXME: se ne trovo piu' di una ? (ad esempio se il documento e' in realta' un cappello)
        res = TestataMovimento().select(idTestataDocumento = self.id,batchSize=None)
        #Tutto nuovo non ci sono teste movimento relate a questa testata documento
        if not res:
            #se però c'è movimentazione vuol dire che ha un movimento abbinato
            if contieneMovimentazione:
                #creo una nuova testata movimento
                DaoTestataMovimento = TestataMovimento()
                DaoTestataMovimento.data_movimento = self.data_documento
                if not DaoTestataMovimento.numero:
                    valori = numeroRegistroGet(tipo="Movimento", date=self.data_documento)
                    DaoTestataMovimento.numero = valori[0]
                    DaoTestataMovimento.registro_numerazione= valori[1]
                DaoTestataMovimento.operazione = self.operazione
                DaoTestataMovimento.id_cliente = self.id_cliente
                DaoTestataMovimento.id_fornitore = self.id_fornitore
                DaoTestataMovimento.note_interne = self.note_interne
                DaoTestataMovimento.note_interne = self.note_interne
                DaoTestataMovimento.id_testata_documento = self.id # abbino la testata alla testata movimento
        elif len(res) == 1:
            #print "RES È UGUALE AD UNO.... ESITE UN MOVIMENTO USO RES"
            DaoTestataMovimento = res[0] #TestataMovimento().getRecord(id=res[0].id)
            if not contieneMovimentazione:
                #devo eliminare il movimento interamente, visto che non ci sono righe movimento
                #self.righeMovimentoDel(id=DaoTestataMovimento.id)
                DaoTestataMovimento.delete()
                DaoTestataMovimento = None
            else:
                #la testata movimento e` gia` presente, quindi devo aggiornarla
                DaoTestataMovimento.data_movimento = self.data_documento
                DaoTestataMovimento.operazione = self.operazione
                DaoTestataMovimento.id_cliente = self.id_cliente
                DaoTestataMovimento.id_fornitore = self.id_fornitore
                DaoTestataMovimento.note_interne = self.note_interne
                DaoTestataMovimento.note_interne = self.note_interne
                DaoTestataMovimento.id_testata_documento = self.id
                #righeMovimentoDel(id=DaoTestataMovimento.id)
        else:
            # ci sono piu' movimenti collegati al documento
            # FIXME: che fare ?
            raise Exception, "ATTENZIONE CI SONO PIU' MOVIMENTI LEGATI AD UN DOCUMENTO"
        #print "DOPO if di check di RES ", tempo()
        righeMovimento = []
        righeDocumento = []
        scontiRigaMovimento = []
        if self.righeDocumento:  #trattiamo le righe documento e movimento
            #print "Prima del FOR delle RIGHE ", tempo()
            for row in self.righeDocumento:
                if (row.id_articolo is not None and contieneMovimentazione):
                    #salvo tra le righe movimenti
                    #print "RIGHE ",row.id_articolo, tempo()
                    daoRigaMovimento = RigaMovimento()
                    #daoRigaMovimento.id_testata_movimento = DaoTestataMovimento.id
                    daoRigaMovimento.valore_unitario_netto = row.valore_unitario_netto
                    daoRigaMovimento.valore_unitario_lordo = row.valore_unitario_lordo
                    daoRigaMovimento.quantita = row.quantita
                    daoRigaMovimento.moltiplicatore = row.moltiplicatore
                    daoRigaMovimento.applicazione_sconti = row.applicazione_sconti
                    daoRigaMovimento.percentuale_iva = row.percentuale_iva
                    daoRigaMovimento.descrizione = row.descrizione
                    daoRigaMovimento.id_listino = row.id_listino
                    daoRigaMovimento.id_magazzino = row.id_magazzino
                    daoRigaMovimento.id_articolo = row.id_articolo
                    daoRigaMovimento.id_multiplo = row.id_multiplo
                    daoRigaMovimento.codiceArticoloFornitore = row.codiceArticoloFornitore
                    if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
                        daoRigaMovimento.prezzo_acquisto_noleggio = row.prezzo_acquisto_noleggio
                        daoRigaMovimento.coeficente_noleggio = row.coeficente_noleggio
                        daoRigaMovimento.isrent = row.isrent

                    scontiRigaMovimento = []
                    if row.scontiRigaDocumento:
                        for v in row.scontiRigaDocumento:
                            daoScontoMovimento = ScontoRigaMovimento()
                            daoScontoMovimento.valore = v.valore
                            daoScontoMovimento.tipo_sconto = v.tipo_sconto

                            scontiRigaMovimento.append(daoScontoMovimento)
                    if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable')=="yes":
                        if row.misura_pezzo:
                                daoRigaMovimento.misura_pezzo = row.misura_pezzo

                    daoRigaMovimento.scontiRigheMovimento = scontiRigaMovimento
                    righeMovimento.append(daoRigaMovimento)
                    #righeMovimento.scontiRigheMovimento = scontiRigaMovimento
                else:
                    Environment.pg2log.debug("RIGA SENZA RIFERMENTO ARTICOLO QUINDI DESCRITTIVA, SALVO IN RIGADOCUMENTO")
                    #annullamento id della riga
                    #row._resetId()
                    #associazione alla riga della testata
                    row.id_testata_documento = self.id
                    righeMovimento.append(row)

        #print "DOPO IL FOR", tempo()
        if (DaoTestataMovimento is not None):
            if righeMovimento:
                ##print "SE ARRIVI QUI DOVREBBE ANDARE TUTTO BENE" , righeMovimento
                DaoTestataMovimento.righeMovimento=righeMovimento
                DaoTestataMovimento.persist()
        else:
            for riga in righeMovimento:
                riga.persist()
        #print "DOPO IL PERSIST DI RIGA", tempo()

        if self.__ScadenzeDocumento:
            for scad in self.__ScadenzeDocumento:
                scad._resetId()
                scad.id_testata_documento = self.id
                scad.persist()
        #print "DOPO SCADENZE", tempo()

        if self.__data_fine_noleggio and self.__data_inizio_noleggio:
            tn = TestataGestioneNoleggio()
            tn.id_testata_documento = self.id
            tn.data_inizio_noleggio = self.data_inizio_noleggio
            tn.data_fine_noleggio = self.data_fine_noleggio
            tn.persist()
        #print "DOPO FINE NOLEGGIO", tempo()

        if self.scontiSuTotale:
            self.scontiTestataDocumentoDel(id=self.id)
            for scontisutot in self.scontiSuTotale:
                scontisutot.id_testata_documento = self.id
                scontisutot.persist()
        #params["session"].flush()
        Environment.pg2log.debug("FINE SALVATAGGIO DOCUMENTO")


    def righeDocumentoDel(self, id=None):
        """
        Cancella le righe associate ad un documento
        """
        row = RigaDocumento().select(idTestataDocumento= id,
                                                    offset = None,
                                                    batchSize = None)
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



    def scontiTestataDocumentoDel(self,id=None):
        """
        Cancella gli sconti associati ad un documento
        """
        row = ScontoTestataDocumento().select(idScontoTestataDocumento= id,
                                                        offset = None,
                                                        batchSize = None,
                                                        orderBy="id_testata_documento")
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True


    def testataDocumentoScadenzaDel(self,id=None):
        """
        Cancella la scadenza documento associato ad un documento
        """
        row = TestataDocumentoScadenza().select(idTestataDocumentoScadenza= id,
                                                                    offset = None,
                                                                    batchSize = None,
                                                                    orderBy="id_testata_documento")
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

    def scontiRigaDocumentoDel(self,id=None):
        """
        Cancella gli sconti legati ad una riga movimento
        """
        row = ScontoRigaDocumento().select(idRigaDocumento= id,
                                                    offset = None,
                                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True







    def _al(self):
        if self.AL: return self.AL.denominazione
        else: return ""
    aliquota_iva_esenzione = property(_al)


    #property vettore
    def _rag_soc_vett(self):
        if self.PV: return self.PV.ragione_sociale
        else: return ""
    ragione_sociale_vettore = property(_rag_soc_vett)


    #property destinazione_merce
    def _destMerc(self):
        if self.DM: dm = self.DM.denominazione
        else: return ""
    destinazione_merce = property(_destMerc)

    def _destMercInd(self):
        if self.DM: return self.DM.indirizzo
        else: return ""
    indirizzo_destinazione_merce = property(_destMercInd)

    def _destMercloca(self):
        if self.DM: return self.DM.localita
        else: return ""
    localita_destinazione_merce = property(_destMercloca)

    def _destMerccap(self):
        if self.DM: return self.DM.cap
        else: return ""
    cap_destinazione_merce = property(_destMerccap)

    def _destMercprov(self):
        if self.DM: return self.DM.provincia
        else: return ""
    provincia_destinazione_merce = property(_destMercprov)


    #property banca
    def _banca(self):
        if self.BN: return self.BN.denominazione
        else: return ""
    banca = property(_banca)

    def _agenzia(self):
        if self.BN: return self.BN.agenzia
        else: return ""
    agenzia = property(_agenzia)

    def _iban(self):
        if self.BN: return self.BN.iban
        else:return ""
    iban = property(_iban)


    #property pagamento
    def _pagamento(self):
        if self.PG: return self.PG.denominazione
        else:return ""
    pagamento = property(_pagamento)



    #property cliente
    def _ragione_sociale_cliente(self):
        if self.CLI: return self.CLI.ragione_sociale
        else: return ""
    ragione_sociale_cliente= property(_ragione_sociale_cliente)

    def _indirizzo_cliente(self):
        if self.CLI: return self.CLI.sede_legale_indirizzo
        else: return ""
    indirizzo_cliente= property(_indirizzo_cliente)

    def _indirizzo_cliente_operativa(self):
        if self.CLI: return self.CLI.sede_operativa_indirizzo
        else: return ""
    indirizzo_cliente_operativa= property(_indirizzo_cliente_operativa)

    def _cap_cliente(self):
        if self.CLI: return self.CLI.sede_legale_cap
        else:return ""
    cap_cliente= property(_cap_cliente)

    def _cap_cliente_operativa(self):
        if self.CLI: return self.CLI.sede_operativa_cap
        else:return ""
    cap_cliente_operativa= property(_cap_cliente_operativa)

    def _localita_cliente(self):
        if self.CLI: return self.CLI.sede_legale_localita
        else: return ""
    localita_cliente= property(_localita_cliente)

    def _localita_cliente_operativa(self):
        if self.CLI: return self.CLI.sede_operativa_localita
        else: return ""
    localita_cliente_operativa= property(_localita_cliente_operativa)

    def _provincia_cliente(self):
        if self.CLI: return self.CLI.sede_legale_provincia
        else: return ""
    provincia_cliente= property(_provincia_cliente)

    def _provincia_cliente_operativa(self):
        if self.CLI: return self.CLI.sede_operativa_provincia
        else: return ""
    provincia_cliente_operativa= property(_provincia_cliente_operativa)

    def _partita_iva_cliente(self):
        if self.CLI: return self.CLI.partita_iva
        else: return ""
    partita_iva_cliente= property(_partita_iva_cliente)

    def _codice_fiscale_cliente(self):
        if self.CLI: return self.CLI.codice_fiscale
        else: return ""
    codice_fiscale_cliente= property(_codice_fiscale_cliente)

    def _cognome_cliente(self):
        if self.CLI: return self.CLI.cognome
        else: return ""
    cognome_cliente= property(_cognome_cliente)

    def _nome_cliente(self):
        if self.CLI: return self.CLI.nome
        else: return ""
    nome_cliente= property(_nome_cliente)



    #property Fornitore
    def _ragione_sociale_fornitore(self):
        if self.FORN: return self.FORN.ragione_sociale
        else: return ""
    ragione_sociale_fornitore= property(_ragione_sociale_fornitore)

    def _indirizzo_fornitore(self):
        if self.FORN: return self.FORN.sede_legale_indirizzo
        else: return ""
    indirizzo_fornitore= property(_indirizzo_fornitore)

    def _indirizzo_fornitore_operativa(self):
        if self.FORN: return self.FORN.sede_operativa_indirizzo
        else: return ""
    indirizzo_fornitore_operativa= property(_indirizzo_fornitore_operativa)

    def _cap_fornitore(self):
        if self.FORN: return self.FORN.sede_legale_cap
        else: return ""
    cap_fornitore= property(_cap_fornitore)

    def _cap_fornitore_operativa(self):
        if self.FORN: return self.FORN.sede_operativa_cap
        else: return ""
    cap_fornitore_operativa= property(_cap_fornitore_operativa)

    def _localita_fornitore(self):
        if self.FORN: return self.FORN.sede_legale_localita
        else: return ""
    localita_fornitore= property(_localita_fornitore)

    def _localita_fornitore_operativa(self):
        if self.FORN: return self.FORN.sede_operativa_localita
        else: return ""
    localita_fornitore_operativa = property(_localita_fornitore_operativa)

    def _provincia_fornitore(self):
        if self.FORN: return self.FORN.sede_legale_provincia
        else: return ""
    provincia_fornitore= property(_provincia_fornitore)

    def _provincia_fornitore_operativa(self):
        if self.FORN: return self.FORN.sede_operativa_provincia
        else: return ""
    provincia_fornitore_operativa= property(_provincia_fornitore_operativa)

    def _partita_iva_fornitore(self):
        if self.FORN: return self.FORN.partita_iva
        else: return ""
    partita_iva_fornitore= property(_partita_iva_fornitore)

    def _codice_fiscale_fornitore(self):
        if self.FORN: return self.FORN.codice_fiscale
        else: return ""
    codice_fiscale_fornitore= property(_codice_fiscale_fornitore)

    def _cognome_fornitore(self):
        if self.FORN: return self.FORN.cognome
        else: return ""
    cognome_fornitore= property(_cognome_fornitore)

    def _nome_fornitore(self):
        if self.FORN: return self.FORN.nome
        else: return ""
    nome_fornitore= property(_nome_fornitore)

    #property Agente
    def _ragione_sociale_agente(self):
        if self.AGE: return self.AGE.ragione_sociale
        else: return ""
    ragione_sociale_agente= property(_ragione_sociale_agente)


    if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
        def _get_data_inizio_noleggio(self):
            if not self.__data_inizio_noleggio:
                if self.TGN:
                    self.__data_inizio_noleggio = self.TGN.data_inizio_noleggio
                else:
                    self.__data_inizio_noleggio =  ""
            return self.__data_inizio_noleggio
        def _set_data_inizio_noleggio(self, value):
            self.__data_inizio_noleggio = value
        data_inizio_noleggio = property(_get_data_inizio_noleggio, _set_data_inizio_noleggio)

        def _get_data_fine_noleggio(self):
            if not self.__data_fine_noleggio:
                if self.TGN:
                    self.__data_fine_noleggio = self.TGN.data_fine_noleggio
                else:
                    self.__data_fine_noleggio =  ""
            return self.__data_fine_noleggio
        def _set_data_fine_noleggio(self, value):
            self.__data_fine_noleggio = value
        data_fine_noleggio = property(_get_data_fine_noleggio, _set_data_fine_noleggio)


    def delete(self):
        #print "PARTIAMO DA QUI"
        #testataMovDel = TestataMovimento().select(id_testata_documento = self.id).all()

        params['session'].delete(self)
        params['session'].commit()

    def filter_values(self,k,v):
        if k == 'daNumero':
            dic = {k:testata_documento.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:testata_documento.c.numero <= v}
        elif k == 'daParte':
            dic = {k:testata_documento.c.parte >= v}
        elif k == 'aParte':
            dic = {k:testata_documento.c.parte <= v}
        elif k == 'daData':
            dic = {k:testata_documento.c.data_documento >= v}
        elif k== 'aData':
            dic = {k:testata_documento.c.data_documento <= v}
        elif k =='protocollo':
            dic = {k:testata_documento.c.protocollo.ilike("%"+v+"%")}
        elif k == 'idOperazione':
            dic = {k:testata_documento.c.operazione == v}
        elif k == 'idMagazzino':
            dic = {k:and_(or_(testata_documento.c.id== riga_doc.c.id_testata_documento,riga.c.id_magazzino==v),
                        or_(testata_documento.c.id==TestataMovimento.id_testata_documento,riga.c.id_magazzino==v))}
        elif k == 'idCliente':
            dic = {k:testata_documento.c.id_cliente == v}
        elif k == 'idFornitore':
            dic = {k:testata_documento.c.id_fornitore == v}
        elif k == 'idAgente':
            dic = {k:testata_documento.c.id_agente == v}
        elif k == 'statoDocumento':
            dic = {k:testata_documento.c.documento_saldato == v}
        elif k == 'idArticolo':
            dic = {k: and_(Articolo.id ==Riga.id_articolo,
                            riga.c.id==RigaMovimento.id,
                            RigaMovimento.id_testata_movimento == TestataMovimento.id,
                            TestataMovimento.id_testata_documento == testata_documento.c.id,
                            Articolo.id ==v),
                                }
        elif hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
            if k == 'daDataInizioNoleggio':
                dic = {k:and_(testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_inizio_noleggio >= v)}
            elif k== 'aDataInizioNoleggio':
                dic = {k:and_(testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_inizio_noleggio <= v)}
            if k == 'daDataFineNoleggio':
                dic = {k:and_(testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_fine_noleggio >= v)}
            elif k== 'aDataFineNoleggio':
                dic = {k:and_(testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_fine_noleggio <= v)}
        return  dic[k]

riga=Table('riga',params['metadata'],schema = params['schema'],autoload=True)
riga_doc=Table('riga_documento',params['metadata'],schema = params['schema'],autoload=True)
testata_documento=Table('testata_documento',params['metadata'],schema = params['schema'],autoload=True)
vettore = Table('vettore',params['metadata'],schema = params['schema'],autoload=True)
testata_movi=Table('testata_movimento',params['metadata'],schema = params['schema'],autoload=True)
agen = Table('agente',params['metadata'],schema = params['schema'],autoload=True)
paga = Table('pagamento',params['metadata'],schema = params['schema'],autoload=True)
clie = Table('cliente',params['metadata'],schema = params['schema'],autoload=True)
banc = Table('banca',params['metadata'],schema = params['schema'],autoload=True)
fornitor=Table('fornitore', params['metadata'], schema = params['schema'], autoload=True)

std_mapper = mapper(TestataDocumento, testata_documento, properties={
        "rigadoc": relation(RigaDocumento, backref="testata_documento"),
        "testata_documento_scadenza" :relation(TestataDocumentoScadenza,cascade="all, delete, delete-orphan", backref="testata_documento"),
        "PG":relation(Pagamento,primaryjoin = testata_documento.c.id_pagamento==paga.c.id),
        "BN":relation(Banca,primaryjoin = (testata_documento.c.id_banca==banc.c.id)),
        "AL":relation(AliquotaIva,primaryjoin = (testata_documento.c.id_aliquota_iva_esenzione==AliquotaIva.id)),
        "PV":relation(Vettore,primaryjoin = (testata_documento.c.id_vettore==vettore.c.id)),
        "DM":relation(DestinazioneMerce, primaryjoin=(testata_documento.c.id_destinazione_merce==DestinazioneMerce.id)),
        "TM":relation(TestataMovimento,primaryjoin = (testata_documento.c.id==testata_movi.c.id_testata_documento), backref='TD'),
        "CLI":relation(Cliente,primaryjoin = (testata_documento.c.id_cliente==clie.c.id)),
        "FORN":relation(Fornitore,primaryjoin = (testata_documento.c.id_fornitore==fornitor.c.id)),
        "AGE":relation(Agente,primaryjoin = (testata_documento.c.id_agente==agen.c.id)),
        "OP":relation(Operazione,primaryjoin = (testata_documento.c.operazione==Operazione.denominazione), backref="TD"),
        "STD":relation(ScontoTestataDocumento,primaryjoin = (testata_documento.c.id==ScontoTestataDocumento.id_testata_documento), backref="TD"),
        #'lang':relation(Language, backref='user')
        }, order_by=testata_documento.c.numero)

if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
    std_mapper.add_property("TGN",relation(TestataGestioneNoleggio,primaryjoin=(testata_documento.c.id==TestataGestioneNoleggio.id_testata_documento),backref="TD",uselist = False))



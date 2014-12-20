# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2014 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>
# Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.lib.alembic.migration import MigrationContext
from promogest.lib.alembic.operations import Operations
from promogest.lib.alembic import op

try:
    t_testata_documento = Table('testata_documento',
                              params['metadata'],
                              schema=params['schema'],
                              autoload=True)
except:
    from data.testataDocumento import t_testata_documento


from Dao import Dao
from Operazione import Operazione
from ScontoTestataDocumento import ScontoTestataDocumento
from DestinazioneMerce import DestinazioneMerce
from TestataMovimento import TestataMovimento, t_testata_movimento
from Pagamento import Pagamento, t_pagamento
from Vettore import Vettore, t_vettore
from promogest.dao.daoAgenti.Agente import Agente, t_agente
from Fornitore import Fornitore, t_fornitore
from Cliente import Cliente, t_cliente
from RigaDocumento import RigaDocumento
from RigaDocumento import *
from AliquotaIva import AliquotaIva
from RigaMovimento import RigaMovimento
from Banca import Banca, t_banca
from Riga import Riga, t_riga
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota
from promogest.modules.PrimaNota.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento, t_informazioni_fatturazione_documento
import promogest.lib.ibanlib

from promogest.dao.DaoUtils import get_columns  , numeroRegistroGet
from promogest.dao.CachedDaosDict import CachedDaosDict
from decimal import *

columns_t_t_doc = get_columns(t_testata_documento)

if "esclusione_spese" not in columns_t_t_doc:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('testata_documento', Column('esclusione_spese', Boolean, default=True),schema=params["schema"])

from promogest import Environment

import datetime

class TipoDocumento:
    DDT_VENDITA = 'DDT vendita'

class TestataDocumento(Dao):
    def __init__(self, req=None):
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
        self._totaleNonBaseImponibile = 0
        self._totaleNonScontato = 0
        self._totaleScontato = 0
        self._totaleImponibileScontato = 0
        self._totaleImposta = 0
        self._totaleImpostaScontata = 0
        self._castellettoIva = 0
        self.__data_inizio_noleggio = None
        self.__data_fine_noleggio = None
        self.__numeroMagazzini = 0
        self._totaleSpese = 0
        self._totaleImponibileSpese = 0
        self._totaleImpostaSpese = 0


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

    def __repr__(self):
        return '<Documento ID={0} operazione="{1}">'.format(self.numero, self.operazione)

    def _getScadenzeDocumento(self):
        #if not self.__dbScadenzeDocumento:
        if self.id:
            #self.__dbScadenzeDocumento = params['session']\
                                    #.query(TestataDocumentoScadenza)\
                                    #.with_parent(self)\
                                    #.filter_by(id_testata_documento=self.id)\
                                    #.all()
            self.__dbScadenzeDocumento = self.testata_documento_scadenza
        self.__ScadenzeDocumento = self.__dbScadenzeDocumento[:]
        return self.__ScadenzeDocumento

    def _setScadenzeDocumento(self, value):
        self.__ScadenzeDocumento = value

    scadenze = property(_getScadenzeDocumento, _setScadenzeDocumento)

    def _getRigheDocumento(self):
        #if not self.__righeDocumento:
        self.__dbRigheMovimentoPart = []
        self.__dbRigheDocumentoPart = []
        if self.id:
            self.__dbRigheDocumentoPart = self.rigadoc
            if self.TM and len(self.TM) ==1:
                self.__dbRigheMovimentoPart = self.TM[0].rigamov
            elif self.TM and len(self.TM) >1:
                if not Environment.web:
                    Environment.pg2log.info("ATTENZIONE due movimenti fanno riferimento ad una sola testata documento:"+str(self.id))
                print "ID DEL DOCUMENTO", str(self.id)
                raise Exception("Più di un movimento fa riferimento allo stesso documento!")
            self.__dbRigheDocumento = self.__dbRigheDocumentoPart + self.__dbRigheMovimentoPart
            self.__dbRigheDocumento.sort(key=lambda x: x.posizione or x.id)
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
            if riga.id_magazzino not in __numeroMagazzini and riga.id_magazzino !=None:
                __numeroMagazzini.append(riga.id_magazzino)
        return len(__numeroMagazzini)
    numeroMagazzini = property(_getNumeroMagazzini)

    def _getScontiTestataDocumento(self):
        if not self.__scontiTestataDocumento:
            if self.STD:
                self.__dbScontiTestataDocumento = self.STD
            self.__scontiTestataDocumento = self.__dbScontiTestataDocumento
        return self.__scontiTestataDocumento

    def _setScontiTestataDocumento(self, value):
        self.__scontiTestataDocumento = value

    sconti = property(_getScontiTestataDocumento, _setScontiTestataDocumento)

    def _getStringaScontiTestataDocumento(self):
        #(listSconti, applicazione) = getScontiFromDao(self._getScontiTestataDocumento(), self.applicazione_sconti)
        (listSconti, applicazione) = getScontiFromDao(self.STD, self.applicazione_sconti)
        return getStringaSconti(listSconti)
    stringaSconti = property(_getStringaScontiTestataDocumento)

    def _getIntestatario(self):
        """
        Restituisce la ragione sociale o cognome + nome
        se la ragione sociale e' vuota
        """
        if self.id_cliente is not None and self.CLI:
            if self.CLI.ragione_sociale != "":
                return  self.CLI.ragione_sociale
            else:
                return self.CLI.cognome + ' ' + self.CLI.nome
        elif self.id_fornitore is not None and self.FORN:
            if self.FORN.ragione_sociale != "":
                return  self.FORN.ragione_sociale
            else:
                return self.FORN.cognome + ' ' + self.FORN.nome
        else:
            return ''

    intestatario = property(_getIntestatario, )

    def _getPI_CF(self):
        """
        Restituisce la partita iva e/o il codice fiscale del cliente o fornitore.
        """
        if setconf("PrimaNota", "aggiungi_partita_iva"):
            pi = self.partita_iva_cliente or self.partita_iva_fornitore
            cf = self.codice_fiscale_cliente or self.codice_fiscale_fornitore
            if  (pi != cf) and ((pi and cf) != ''):
                return '; P.I: {0}'.format(pi) + '; C.F: {0}'.format(cf)
            elif pi:
                return '; P.I: {0}'.format(pi)
            elif cf:
                return '; C.F: {0}'.format(cf)
            else:
                return ''
        else:
            return ''


    @property
    def totali(self):
        """ funzione di calcolo dei totali documento """

        def getSpesePagamento(pagamento):
            cache = CachedDaosDict()
            if pagamento in cache['pagamento']:
                p = cache['pagamento'][pagamento]
                if Decimal(str(p.spese or 0)) != Decimal(0):
                    return Decimal(str(p.spese)), calcolaPrezzoIva(Decimal(str(p.spese)), Decimal(str(p.perc_aliquota_iva)))
                else:
                    return (Decimal(0), Decimal(0))
            else:
                return (Decimal(0), Decimal(0))

        self.__operazione = leggiOperazione(self.operazione)
        fonteValore = self.__operazione["fonteValore"]
        cache = CachedDaosDict()
        # FIXME: duplicated in AnagraficaDocumenti.py
        totaleImponibile = Decimal(0)
        totaleImposta = Decimal(0)
        totaleNonScontato = Decimal(0)
        totaleImpostaScontata = Decimal(0)
        totaleImponibileScontato = Decimal(0)
        totaleEsclusoBaseImponibile = Decimal(0)
        totaleRicaricatoLordo = Decimal(0)
        totaleScontato = Decimal(0)
        castellettoIva = {}

        spese = Decimal(0)
        impon_spese = Decimal(0)
        imposta_spese = Decimal(0)
        if self.esclusione_spese == False:
            for scad in self.scadenze:
                if scad:
                    impon_spese_, spese_ = getSpesePagamento(scad.pagamento)
                    spese += spese_
                    impon_spese += impon_spese_
                    imposta_spese += spese_ - impon_spese_
        self._totaleSpese = spese
        self._totaleImponibileSpese = impon_spese
        self._totaleImpostaSpese = imposta_spese
        totaleEsclusoBaseImponibileRiga = 0
        totaleImponibileRiga = 0
        merca = setconf("General", "gestione_totali_mercatino")
        for riga in self.righe:
            # FIXME: added for supporting dumb rows when printing
            if riga is None:
                continue
            if not riga.moltiplicatore:
                moltiplicatore = 1
            else:
                moltiplicatore = riga.moltiplicatore
            if merca:
                trn = riga.totaleRiga
                trl = riga.totaleRigaLordo
                if trn != 0 and trl != 0:
                    if riga.id_articolo and riga.id_listino:
                        from promogest.lib.utils import leggiListino
                        ll = leggiListino(riga.id_listino, riga.id_articolo)
                        totaleRicaricatoLordo += (trn * (ll["ultimoCosto"]*Decimal(riga.quantita or 0)) / trl)
                    elif riga.id_articolo and not riga.id_listino:
                        lf = leggiFornitura(riga.id_articolo)
                        totaleRicaricatoLordo += (trn * (lf["prezzoNetto"]*Decimal(riga.quantita or 0)) / trl)

            percentualeIvaRiga = Decimal(riga.percentuale_iva) #campo non più da usare
            idAliquotaIva = riga.id_iva  # campo da usare perchè l'id è più preciso
            daoiva = None
            aliquotaIvaRiga = None
            if idAliquotaIva:
                if idAliquotaIva in cache['aliquotaiva']:
                    daoiva = cache['aliquotaiva'][idAliquotaIva][0]
                if daoiva:
                    aliquotaIvaRiga = daoiva.percentuale
            if not aliquotaIvaRiga: # solo se non l'ho trovato dall'id prendo quello della percentuale
                aliquotaIvaRiga =  percentualeIvaRiga
            totaleRiga = riga.totaleRiga

            if (fonteValore == "vendita_iva" or fonteValore == "acquisto_iva"):
                if daoiva and cache['aliquotaiva'][idAliquotaIva][1] == "Non imponibile":
                    totaleEsclusoBaseImponibileRiga = totaleRiga
                    totaleImponibileRiga = 0
                else:
                    totaleEsclusoBaseImponibileRiga = 0
                    totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga)
            else:
                if daoiva and cache['aliquotaiva'][idAliquotaIva][1] == "Non imponibile":
                    totaleEsclusoBaseImponibileRiga = totaleRiga
                    totaleImponibileRiga = 0
                    totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)
                else:
                    totaleEsclusoBaseImponibileRiga = 0
                    totaleImponibileRiga = totaleRiga or 0
                    totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)
            totaleImpostaRiga = totaleRiga - (totaleImponibileRiga + totaleEsclusoBaseImponibileRiga)
            totaleNonScontato += totaleRiga
            totaleImponibile += totaleImponibileRiga
            totaleImposta += totaleImpostaRiga
            totaleEsclusoBaseImponibile += totaleEsclusoBaseImponibileRiga
            if daoiva:
                denominazione = daoiva.denominazione
                denominazione_breve = daoiva.denominazione_breve
            else:
                denominazione = ""
                denominazione_breve = ""
            if idAliquotaIva not in castellettoIva.keys():
                castellettoIva[idAliquotaIva] = {
                    'percentuale': percentualeIvaRiga,
                    'imponibile': totaleImponibileRiga,
                    'imposta': totaleImpostaRiga,
                    'totale': (totaleImponibileRiga+totaleImpostaRiga),
                    "denominazione_breve": denominazione_breve,
                    "denominazione": denominazione}
            else:
                castellettoIva[idAliquotaIva]['percentuale'] = percentualeIvaRiga
                castellettoIva[idAliquotaIva]['imponibile'] += totaleImponibileRiga
                castellettoIva[idAliquotaIva]['imposta'] += totaleImpostaRiga
                castellettoIva[idAliquotaIva]['totale'] += (totaleImponibileRiga+totaleImpostaRiga)
        #totaleImposta = totaleNonScontato - (totaleImponibile+totaleEsclusoBaseImponibile)
        totaleImposta = totaleImposta + totaleEsclusoBaseImponibile
        totaleImponibileScontato = totaleImponibile
        totaleImpostaScontata = totaleImposta
        totaleScontato = totaleNonScontato
        scontiSuTotale = self.sconti
        applicazioneSconti = self.applicazione_sconti

        if len(scontiSuTotale) > 0:
            for s in scontiSuTotale:
                if s.tipo_sconto == 'percentuale':
                    if applicazioneSconti == 'scalare':
                        totaleImponibileScontato = totaleImponibileScontato * (1 - Decimal(s.valore) / 100)
                    elif applicazioneSconti == 'non scalare':
                        totaleImponibileScontato = totaleImponibileScontato - totaleNonScontato * totaleImponibileScontato * Decimal(s.valore) / 100
                    else:
                        raise Exception, ('BUG! Tipo di applicazione sconto '
                                          'sconosciuto: %s' % s.tipo_sconto)
                elif s.tipo_sconto == 'valore':
                    totaleImponibileScontato = totaleImponibileScontato - Decimal(s.valore)
            # riporta l'insieme di sconti ad una percentuale globale
            if totaleScontato >0:
                try:
                    percentualeScontoGlobale = (1 - totaleImponibileScontato / totaleImponibile) * 100
                except:
                    percentualeScontoGlobale = 100

            else:
                percentualeScontoGlobale = 100

            totaleImpostaScontata = 0
            totaleImponibileScontato = 0
            # riproporzione del totale, dell'imponibile e dell'imposta
            for k in castellettoIva.keys():
                castellettoIva[k]['totale'] = castellettoIva[k]['totale'] * (1 - Decimal(percentualeScontoGlobale) / 100)
                castellettoIva[k]['imponibile'] = castellettoIva[k]['imponibile'] * (1 - Decimal(percentualeScontoGlobale) / 100)
                castellettoIva[k]['imposta'] = castellettoIva[k]['totale'] * (1 - Decimal(percentualeScontoGlobale) / 100) - castellettoIva[k]['imponibile'] * (1 - Decimal(percentualeScontoGlobale) / 100)

                totaleImponibileScontato += Decimal(castellettoIva[k]['imponibile'])
                totaleImpostaScontata += Decimal(castellettoIva[k]['imposta'])


            totaleScontato = mN(totaleImponibileScontato + totaleImpostaScontata, 2)
        self._totaleNonScontato = mN(totaleImponibile,2) + mN(totaleImposta,2) + mN(totaleEsclusoBaseImponibile,2) + mN(spese, 2)
        self._totaleScontato = mN(totaleImponibileScontato,2) + mN(totaleImpostaScontata,2) + mN(totaleEsclusoBaseImponibile,2) + mN(spese, 2)
        self._totaleScontatoIT = mNLC(self._totaleScontato,2)
        self._totaleImponibile = mN(totaleImponibile,2) + mN(impon_spese,2)
        self._totaleNonBaseImponibile = totaleEsclusoBaseImponibile
        self._totaleImposta = mN(totaleImposta,2)  + mN(imposta_spese,2)
        self._totaleImponibileScontato = mN(totaleImponibileScontato,2) + mN(impon_spese,2)
        self._totaleImponibileScontatoIT = mNLC(self._totaleImponibileScontato,2)
        self._totaleValoreSconto = self._totaleImponibile - self._totaleImponibileScontato
        self._totaleRicaricatoLordo = self._totaleImponibileScontato - mN(totaleRicaricatoLordo,2)
        try:
            if self.data_documento < datetime.datetime(2011,9,16):
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(20)/100)
            elif self.data_documento < datetime.datetime(2013,10,1):
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(21)/100)
            else:
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(22)/100)
        except:
            if self.data_documento < datetime.date(2011,9,16):
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(20)/100)
            elif self.data_documento < datetime.date(2013,10,1):
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(21)/100)
            else:
                self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(22)/100)

        self._totaleRicaricatoIva = mN(self._totaleRicaricatoLordo,2) - mN(self._totaleRicaricatoImponibile,2)
        self._totaleOggetti = self._totaleScontato - self._totaleRicaricatoLordo
        self._totaleImpostaScontata = mN(totaleImpostaScontata,2) + mN(imposta_spese,2)
        self._totaleImpostaScontataIT = mNLC(self._totaleImpostaScontata,2)
        self._castellettoIva = []
        imposta = 0
        imponibile = 0
        for k in castellettoIva.keys():
            dictCastellettoIva = castellettoIva[k]
            dictCastellettoIva['aliquota'] = castellettoIva[k]["percentuale"]
            dictCastellettoIva["imponibile"] = mN(dictCastellettoIva["imponibile"],2)
            imponibile += dictCastellettoIva["imponibile"]
            dictCastellettoIva["imposta"] = mN(dictCastellettoIva["imposta"],2)
            imposta += dictCastellettoIva["imposta"]
            dictCastellettoIva["totale"] = mN(dictCastellettoIva["imponibile"],2)+ mN(dictCastellettoIva["imposta"],2)
            self._castellettoIva.append(dictCastellettoIva)
        if imposta !=  self._totaleImpostaScontata:
            self._totaleImpostaScontata = imposta
        if imponibile != self._totaleImponibileScontato:
            self._totaleImponibileScontato = imponibile
        if (imposta+imponibile) != self._totaleScontato:
            self._totaleScontato = imposta+imponibile
        return None


    #@property
    #def totali(self, anag=None):
        #""" funzione di calcolo dei totali documento """

        #def getSpesePagamento(pagamento):
            #cache = CachedDaosDict()
            #if pagamento in cache['pagamento']:
                #p = cache['pagamento'][pagamento]
                #if Decimal(str(p.spese or 0)) != Decimal(0):
                    #return Decimal(str(p.spese)), calcolaPrezzoIva(Decimal(str(p.spese)), Decimal(str(p.perc_aliquota_iva)))
                #else:
                    #return (Decimal(0), Decimal(0))
            #else:
                #return (Decimal(0), Decimal(0))

        #self.__operazione = leggiOperazione(self.operazione)
        #fonteValore = self.__operazione["fonteValore"]
        #cache = CachedDaosDict()
        ## FIXME: duplicated in AnagraficaDocumenti.py

        #totaleImponibile = Decimal(0)
        #totaleImposta = Decimal(0)
        #totaleNonScontato = Decimal(0)
        #totaleImpostaScontata = Decimal(0)
        #totaleImponibileScontato = Decimal(0)
        #totaleEsclusoBaseImponibile = Decimal(0)
        #totaleRicaricatoLordo = Decimal(0)
        #totaleScontato = Decimal(0)
        #castellettoIva = {}
        #totaleEsclusoBaseImponibileRiga = 0
        #totaleImponibileRiga = 0

        #spese = Decimal(0)
        #impon_spese = Decimal(0)
        #imposta_spese = Decimal(0)
        #if self.esclusione_spese == False:
            #for scad in self.scadenze:
                #if scad:
                    #impon_spese_, spese_ = getSpesePagamento(scad.pagamento)
                    #spese += spese_
                    #impon_spese += impon_spese_
                    #imposta_spese += spese_ - impon_spese_
        #self._totaleSpese = spese
        #self._totaleImponibileSpese = impon_spese
        #self._totaleImpostaSpese = imposta_spese
        #merca = setconf("General", "gestione_totali_mercatino")

        #for riga in self.righe:
            ## FIXME: added for supporting dumb rows when printing
            #if riga is None:
                #continue
            #if not riga.moltiplicatore:
                #moltiplicatore = 1
            #else:
                #moltiplicatore = riga.moltiplicatore

            #if merca:
                #trn = riga.totaleRiga
                #trl = riga.totaleRigaLordo
                #if trn != 0 and trl != 0:
                    #if riga.id_articolo and riga.id_listino:
                        #from promogest.lib.utils import leggiListino
                        #ll = leggiListino(riga.id_listino, riga.id_articolo)
                        #totaleRicaricatoLordo += (trn * (ll["ultimoCosto"]*Decimal(riga.quantita or 0)) / trl)
                    #elif riga.id_articolo and not riga.id_listino:
                        #lf = leggiFornitura(riga.id_articolo)
                        #totaleRicaricatoLordo += (trn * (lf["prezzoNetto"]*Decimal(riga.quantita or 0)) / trl)


            #percentualeIvaRiga = Decimal(riga.percentuale_iva) #campo non più da usare
            #idAliquotaIva = riga.id_iva  # campo da usare perchè l'id è più preciso
            #daoiva = None
            #aliquotaIvaRiga = None
            #if idAliquotaIva:
                #if idAliquotaIva in cache['aliquotaiva']:
                    #daoiva = cache['aliquotaiva'][idAliquotaIva][0]
                #if daoiva:
                    #aliquotaIvaRiga = daoiva.percentuale
            #if not aliquotaIvaRiga: # solo se non l'ho trovato dall'id prendo quello della percentuale
                #aliquotaIvaRiga =  percentualeIvaRiga
            #if daoiva:
                #denominazione = daoiva.denominazione
                #denominazione_breve = daoiva.denominazione_breve
            #else:
                #denominazione = ""
                #denominazione_breve = ""

            #totaleRiga = mN(riga.totaleRiga,2)

            #if (fonteValore == "vendita_iva" or fonteValore == "acquisto_iva"):
                #if daoiva and cache['aliquotaiva'][idAliquotaIva][1] == "Non imponibile":
                    #totaleEsclusoBaseImponibileRiga = totaleRiga
                    #totaleImponibileRiga = 0
                #else:
                    #totaleEsclusoBaseImponibileRiga = 0
                    #totaleImponibileRiga = mN(calcolaPrezzoIva(Decimal(totaleRiga), Decimal(-1 * percentualeIvaRiga)), 2)
            #else:
                #if daoiva and cache['aliquotaiva'][idAliquotaIva][1] == "Non imponibile":
                    #totaleEsclusoBaseImponibileRiga = totaleRiga
                    #totaleImponibileRiga = 0
                    #totaleRiga = mN(calcolaPrezzoIva(Decimal(totaleRiga), Decimal(percentualeIvaRiga)), 2)
                #else:
                    #totaleEsclusoBaseImponibileRiga = 0
                    #totaleImponibileRiga = totaleRiga or 0
                    #totaleRiga = mN(calcolaPrezzoIva(Decimal(totaleRiga), Decimal(percentualeIvaRiga)), 2)

            #if idAliquotaIva not in castellettoIva.keys():
                #castellettoIva[idAliquotaIva] = {
                    #'percentuale': percentualeIvaRiga,
                    #'imponibile': totaleImponibileRiga,
                    #'esclusoBaseImponibile': totaleEsclusoBaseImponibileRiga,
                    #"denominazione_breve": denominazione_breve,
                    #"denominazione": denominazione
                #}
            #else:
                #castellettoIva[idAliquotaIva]['imponibile'] += totaleImponibileRiga
                #castellettoIva[idAliquotaIva]['esclusoBaseImponibile'] += totaleEsclusoBaseImponibileRiga

        ## totali e calcolo imposta
        #totaleImponibile = 0
        #totaleEsclusoBaseImponibile = 0
        #totaleImposta = 0
        #totaleNonScontato = 0
        #for k in castellettoIva.keys():

            #totaleImponibile += castellettoIva[k]['imponibile']
            #totaleEsclusoBaseImponibile += castellettoIva[k]['esclusoBaseImponibile']
            #if castellettoIva[k]['percentuale'] != Decimal(0):
                #castellettoIva[k]['imposta'] = mN(castellettoIva[k]['imponibile'] * castellettoIva[k]['percentuale'] / 100, 2) + castellettoIva[k]['esclusoBaseImponibile']
                #totaleImposta += castellettoIva[k]['imposta']
            #else:
                #castellettoIva[k]['imposta'] = 0

            #castellettoIva[k]['totale'] = castellettoIva[k]['imponibile'] + castellettoIva[k]['esclusoBaseImponibile'] + castellettoIva[k]['imposta']
            #totaleNonScontato += castellettoIva[k]['totale']

        #self._totaleNonScontato = mN(totaleImponibile, 2) + mN(totaleImposta, 2) + mN(totaleEsclusoBaseImponibile, 2) + mN(spese, 2)
        #self._totaleNonBaseImponibile = totaleEsclusoBaseImponibile
        #self._totaleImponibile = mN(totaleImponibile, 2) + mN(impon_spese, 2)
        #self._totaleImposta = mN(totaleImposta,2)  + mN(imposta_spese,2)

        ## ricalcolo totali con sconti
        #totaleImponibileScontato = totaleImponibile
        #totaleImpostaScontata = totaleImposta
        #totaleScontato = totaleNonScontato

        #scontiSuTotale = self.sconti
        #applicazioneSconti = self.applicazione_sconti

        #if len(scontiSuTotale) > 0:
            #for s in scontiSuTotale:
                #if s.tipo_sconto == 'percentuale':
                    #if applicazioneSconti == 'scalare':
                        #totaleImponibileScontato = totaleImponibileScontato * (1 - Decimal(s.valore) / 100)
                    #elif applicazioneSconti == 'non scalare':
                        #totaleImponibileScontato = totaleImponibileScontato - totaleNonScontato * totaleImponibileScontato * Decimal(s.valore) / 100
                    #else:
                        #pass
                #elif s.tipo_sconto == 'valore':
                    #totaleImponibileScontato = totaleImponibileScontato - Decimal(s.valore)
            ## riporta l'insieme di sconti ad una percentuale globale
            #if totaleScontato >0:
                #percentualeScontoGlobale = (1 - totaleImponibileScontato / totaleImponibile) * 100
            #else:
                #percentualeScontoGlobale = 100

            #totaleImpostaScontata = 0
            #totaleImponibileScontato = 0
            ## riproporzione del totale, dell'imponibile e dell'imposta
            #for k in castellettoIva.keys():
                #castellettoIva[k]['totale'] = mN(castellettoIva[k]['totale'] * (1 - Decimal(percentualeScontoGlobale) / 100), 2)
                #castellettoIva[k]['imponibile'] = mN(castellettoIva[k]['imponibile'] * (1 - Decimal(percentualeScontoGlobale) / 100),2)
                #castellettoIva[k]['imposta'] = mN(castellettoIva[k]['totale'] - castellettoIva[k]['imponibile'],2)

                #totaleImponibileScontato += Decimal(castellettoIva[k]['imponibile'])
                #totaleImpostaScontata += Decimal(castellettoIva[k]['imposta'])

            #totaleScontato = mN(totaleImponibileScontato + totaleImpostaScontata, 2)

        #self._totaleScontato = mN(totaleImponibileScontato,2) + mN(totaleImpostaScontata,2) + mN(totaleEsclusoBaseImponibile,2) + mN(spese, 2)
        #self._totaleImponibileScontato = mN(totaleImponibileScontato,2) + mN(impon_spese,2)
        #self._totaleRicaricatoLordo = self._totaleImponibileScontato - mN(totaleRicaricatoLordo,2)

        #try:
            #if self.data_documento < datetime.datetime(2011,9,16):
                #self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(20)/100)
            #else:
                #self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(21)/100)
        #except:
            #if self.data_documento < datetime.date(2011,9,16):
                #self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(20)/100)
            #else:
                #self._totaleRicaricatoImponibile = Decimal(self._totaleRicaricatoLordo)/(1+Decimal(21)/100)

        #self._totaleRicaricatoIva = mN(self._totaleRicaricatoLordo,2) - mN(self._totaleRicaricatoImponibile,2)
        #self._totaleOggetti = self._totaleScontato - self._totaleRicaricatoLordo
        #self._totaleImpostaScontata = mN(totaleImpostaScontata,2) + mN(imposta_spese,2)

        #self._castellettoIva = []
        #for k in castellettoIva.keys():
            #dictCastellettoIva = castellettoIva[k]
            #dictCastellettoIva['aliquota'] = castellettoIva[k]["percentuale"]
            #self._castellettoIva.append(dictCastellettoIva)
        #return None

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
        if not self.ckdd(self):
            return
        DaoTestataMovimento = None

        if not self.numero:
            valori = numeroRegistroGet(tipo=self.operazione, date=self.data_documento)
            self.numero = valori[0]
            self.registro_numerazione = valori[1]

        params["session"].add(self)
        self.commit()

        #Environment.pg2log.info("INIZIO SALVATAGGIO DOCUMENTO")

        self.scontiTestataDocumentoDel(id=self.id)

        if posso("GN"):
            self.testataDocumentoGestioneNoleggioDel(id=self.id)
        self.righeDocumentoDel(id=self.id)
        #verifica se sono presenti righe di movimentazione magazzino
        contieneMovimentazione = False
        if hasattr(self, 'righeDocumento'):
            contieneMovimentazione = self.contieneMovimentazione(righe=self.righeDocumento)
        #cerco le testate movimento associate al documento
        #FIXME: se ne trovo piu' di una ? (ad esempio se il documento e' in realta' un cappello)
#        res = TestataMovimento().select(idTestataDocumento = self.id,batchSize=None)
        #Tutto nuovo non ci sono teste movimento relate a questa testata documento
        if not self.TM and contieneMovimentazione:
            #se però c'è movimentazione vuol dire che ha un movimento abbinato
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
        elif self.TM and len(self.TM) == 1:
            #print "RES È UGUALE AD UNO.... ESITE UN MOVIMENTO USO RES"
            DaoTestataMovimento = self.TM[0]  #TestataMovimento().getRecord(id=res[0].id)
            if not contieneMovimentazione:
                #devo eliminare il movimento interamente, visto che non ci sono righe movimento
                #self.righeMovimentoDel(id=DaoTestataMovimento.id)
                self.TM[0].delete()
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
        elif self.TM and len(self.TM) > 1:
            # ci sono piu' movimenti collegati al documento
            # FIXME: che fare ?
            raise Exception, "ATTENZIONE CI SONO PIU' MOVIMENTI LEGATI AD UN DOCUMENTO"

        if (DaoTestataMovimento is not None):
            if self.righeDocumento:
                ##print "SE ARRIVI QUI DOVREBBE ANDARE TUTTO BENE" , righeMovimento
                DaoTestataMovimento.righeMovimento=self.righeDocumento
                DaoTestataMovimento.persist()
        else:
            sm = posso("SM")
            if hasattr(self, 'righeDocumento'):
                for riga in self.righeDocumento:
                    if self.id:
                        riga.id_testata_documento = self.id
                        riga.persist(sm=sm)

        #Gestione anche della prima nota abbinata al pagamento
        #agganciare qui con dei controlli, le cancellazioni preventive ed i
        #reinserimenti.
        self.testataDocumentoScadenzaDel(dao=self)

        if not(self.__ScadenzeDocumento) and self.ripartire_importo:
            tds = TestataDocumentoScadenza()
            tds.data = datetime.datetime.now()
            tds.numero_scadenza = 1
            tds.pagamento = 'n/a'
            tds.note_per_primanota = ''
            tds.importo = self.totale_sospeso + self.totale_pagato
            self.__ScadenzeDocumento.append(tds)

        num_scadenze = len(self.__ScadenzeDocumento)
        for scad in self.__ScadenzeDocumento:
            scad.id_testata_documento = self.id
            Environment.session.add(scad)

            if self.ripartire_importo:
                if scad.data_pagamento is None:
                    if not setconf('PrimaNota', 'inserisci_senza_data_pagamento'):
                        continue

                ope = leggiOperazione(self.operazione)
                tipo = 'n/a'
                if scad.pagamento != 'n/a':
                    p = Pagamento().select(denominazione=scad.pagamento)
                    if p:
                        tipo = p[0].tipo

                if scad.numero_scadenza == 0:
                    tipo_pag = "ACCONTO"
                    num_scadenze -= 1
                else:
                    tipo_pag = 'pagam. %s' % scad.numero_scadenza
                    if self.documento_saldato and num_scadenze == scad.numero_scadenza:
                        tipo_pag = 'saldo'
                    if scad.data_pagamento is None:
                        if ope['tipoPersonaGiuridica'] == 'fornitore':
                            tipo_pag += ' ricevuta'
                        elif ope['tipoPersonaGiuridica'] == 'cliente':
                            tipo_pag += ' emessa'
                        else:
                            pass

                stringa = "%s %s - %s Rif.interni N.%s " %(self.operazione, self.protocollo, \
                    dateToString(self.data_documento), str(self.numero))
                if ope["denominazione"] in Environment.solo_vendita:
                    stringa += 'a '
                    segno = "entrata"
                elif ope["denominazione"] in Environment.solo_acquisto:
                    stringa += 'da '
                    segno = "uscita"
                else:  # FIXME: non mi piace molto
                    segno = "entrata"
                str_importo_doc = "Importo doc. %s " % mN(self.totale_sospeso + self.totale_pagato, 2)
                stringa += "%s \n%s%s, %s" %(self.intestatario, str_importo_doc, self._getPI_CF(), tipo_pag)

                tpn = TestataPrimaNota()
                tpn.data_inizio = scad.data_pagamento
                tpn.note = ""
                rigaprimanota = RigaPrimaNota()
                rigaprimanota.denominazione = stringa
                rigaprimanota.numero = 1
                rigaprimanota.data_registrazione = scad.data_pagamento
                if tipo:
                    rigaprimanota.tipo = tipo.lower()
                else:
                    rigaprimanota.tipo = 'n/a'
                rigaprimanota.segno = segno
                rigaprimanota.valore = scad.importo
                rigaprimanota.id_banca = scad.id_banca
                rigaprimanota.note_primanota = scad.note_per_primanota or ''
                rigaprimanota.id_testata_documento = self.id
                tpn.righeprimanota = [rigaprimanota]
                tpn.persist()
                a = RigaPrimaNotaTestataDocumentoScadenza()
                a.id_riga_prima_nota = rigaprimanota.id
                a.id_testata_documento_scadenza = scad.id
                params["session"].add(a)
                #params["session"].commit()
        Environment.session.commit()

        #parte relativa al noleggio
        if self.__data_fine_noleggio and self.__data_inizio_noleggio:
            tn = TestataGestioneNoleggio()
            tn.id_testata_documento = self.id
            tn.data_inizio_noleggio = self.data_inizio_noleggio
            tn.data_fine_noleggio = self.data_fine_noleggio
            tn.persist()

        if hasattr(self, 'scontiSuTotale'):
            self.scontiTestataDocumentoDel(id=self.id)
            for scontisutot in self.scontiSuTotale:
                scontisutot.id_testata_documento = self.id
                params["session"].add(scontisutot)
            params["session"].commit()
            self.sconti = []
            self.scontiSuTotale = []
#                scontisutot.persist()
        if not Environment.web:
            Environment.pg2log.info("FINE SALVATAGGIO DOCUMENTO")
        self.init_on_load()

    def righeDocumentoDel(self, id=None):
        """
        Cancella le righe associate ad un documento
        """
        #row = RigaDocumento().select(idTestataDocumento= id,
                                                    #offset = None,
                                                    #batchSize = None)
        sm = posso('SM')
        row = self.rigadoc
        if row:
            for r in row:
                if r.SCD:
                    for a in r.SCD:
                        params['session'].delete(a)
                if sm:
                    mp = MisuraPezzo().select(idRiga=r.id, batchSize=None)
                    if mp:
                        for m in mp:
                            params['session'].delete(m)
                        #params["session"].commit()
                params['session'].delete(r)
            #params["session"].commit()
            return True

    def scontiTestataDocumentoDel(self,id=None):
        """
        Cancella gli sconti associati ad un documento
        """
        #row = ScontoTestataDocumento().select(idScontoTestataDocumento= id,
                            #offset = None,
                            #batchSize = None,
                            #orderBy=ScontoTestataDocumento.id_testata_documento)
        if self.STD:
            for r in self.STD:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def testataDocumentoScadenzaDel(self,dao=None):
        """
        Cancella la scadenza documento associato ad un documento
        """
        #row = TestataDocumentoScadenza().select(idTestataDocumento= dao.id,
                        #offset = None,
                        #batchSize = None)
        row = self.testata_documento_scadenza
        for r in row:
            #a cascata
#            if dao.ripartire_importo: #aka prima nota
            #rpntds = RigaPrimaNotaTestataDocumentoScadenza().\
                    #select(idTestataDocumentoScadenza=r.id, batchSize=None)
            #r.rpntds
            if r.rpntds:
                for p in r.rpntds:
                    try:
                        rpn = r._rpn_
                    except:
                        rpn = RigaPrimaNota().getRecord(id=p.id_riga_prima_nota)
                    tpn = None
                    if rpn:
                        try:
                            tpn = rpn.__tpn
                        except:
                            tpn = TestataPrimaNota().getRecord(id=rpn.id_testata_prima_nota)
                    params['session'].delete(p)
                    #params["session"].commit()
                    if rpn:
                        params['session'].delete(rpn)
                        #params["session"].commit()
                    if tpn and len(tpn.righeprimanota)==0:
                        params['session'].delete(tpn)
                        #params["session"].commit()
            params['session'].delete(r)
        params["session"].commit()
        return True



    def testataDocumentoGestioneNoleggioDel(self,id=None):
        """
        Cancella la gestione noleggio
        """
        row = TestataGestioneNoleggio().select(idTestataDocumento= id,
                        offset = None,
                        batchSize = None,
                        orderBy=TestataGestioneNoleggio.id_testata_documento)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
        return True


    @property
    def aliquota_iva_esenzione(self):
        if self.AL:
            return self.AL.denominazione
        else:
            return ""

    @property
    def ragione_sociale_vettore(self):
        if self.PV:
            return self.PV.ragione_sociale
        else:
            return ""

    @property
    def sede_operativa_localita_vettore(self):
        if self.PV:
            return self.PV.sede_operativa_localita
        else:
            return ""

    @property
    def sede_operativa_indirizzo_vettore(self):
        if self.PV:
            return self.PV.sede_operativa_indirizzo
        else:
            return ""

    @property
    def destinazione_merce(self):
        if self.DM: return self.DM.denominazione
        else: return ""

    @property
    def indirizzo_destinazione_merce(self):
        if self.DM: return self.DM.indirizzo
        else: return ""

    @property
    def localita_destinazione_merce(self):
        if self.DM: return self.DM.localita
        else: return ""

    @property
    def cap_destinazione_merce(self):
        if self.DM:
            return self.DM.cap
        else:
            return ""

    @property
    def provincia_destinazione_merce(self):
        if self.DM:
            return self.DM.provincia
        else:
            return ""

    @property
    def banca(self):
        if self.BN:
            return self.BN.denominazione
        else:
            return ""

    @property
    def agenzia(self):
        if self.BN:
            return self.BN.agenzia
        else:
            return ""

    @property
    def iban(self):
        if self.BN:
            return self.BN.iban
        else:
            return ""

    @property
    def bic_swift(self):
        if self.BN:
            return self.BN.bic_swift
        else:
            return ''

    @property
    def abi(self):
        if self.BN:
            abi = self.BN.abi or ""
            if not abi and self.BN.iban:
                try:
                    ibanlib.dividi_iban(self.BN.iban)[ibanlib.ABI]
                except:
                    abi = ''
            return abi
        else:
            return ""

    @property
    def cab(self):
        if self.BN:
            cab = self.BN.cab or ""
            if not cab and self.BN.iban:
                try:
                    ibanlib.dividi_iban(self.BN.iban)[ibanlib.CAB]
                except: # IBANError:
                    cab = ''
            return cab
        else:
            return ""

    @property
    def pagamento(self):
        if self.PG:
            return self.PG.denominazione
        else:
            return ""

    @property
    def pagamento_tipo(self):
        if self.PG:
            return self.PG.tipo
        else:
            return ""

    @property
    def pagamento_codice(self):
        if self.PG:
            return self.PG.codice
        else:
            return ""

    @property
    def ragione_sociale_cliente(self):
        if self.CLI:
            return self.CLI.ragione_sociale
        else:
            return ""

    @property
    def codice_cliente(self):
        if self.CLI:
            return self.CLI.codice
        else:
            return ""

    @property
    def nazione_cliente(self):
        if self.CLI:
            return self.CLI.nazione
        else:
            return ""

    def _insegna_cliente(self):
        if self.CLI: return self.CLI.insegna
        else: return ""
    insegna_cliente= property(_insegna_cliente)


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
    provincia_cliente_operativa = property(_provincia_cliente_operativa)

    def _partita_iva_cliente(self):
        if self.CLI: return self.CLI.partita_iva
        else: return ""
    partita_iva_cliente = property(_partita_iva_cliente)

    def _codice_fiscale_cliente(self):
        if self.CLI: return self.CLI.codice_fiscale
        else: return ""
    codice_fiscale_cliente = property(_codice_fiscale_cliente)

    def _cognome_cliente(self):
        if self.CLI: return self.CLI.cognome
        else: return ""
    cognome_cliente = property(_cognome_cliente)

    def _nome_cliente(self):
        if self.CLI: return self.CLI.nome
        else: return ""
    nome_cliente = property(_nome_cliente)



    #property Fornitore
    def _ragione_sociale_fornitore(self):
        if self.FORN: return self.FORN.ragione_sociale
        else: return ""
    ragione_sociale_fornitore= property(_ragione_sociale_fornitore)

    def _codice_fornitore(self):
        if self.FORN: return self.FORN.codice
        else: return ""
    codice_fornitore= property(_codice_fornitore)


    def _insegna_fornitore(self):
        if self.FORN: return self.FORN.insegna
        else: return ""
    insegna_fornitore= property(_insegna_fornitore)

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


    if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in Environment.modulesList):
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
        """ Cancelliamo una testata documento con tutti i cascade"""
        from promogest.dao.StoricoDocumento import rimuovi_da_storico
        rimuovi_da_storico(self.id)

        ifd = InformazioniFatturazioneDocumento().select(id_fattura=self.id, batchSize=None)
        if ifd:
            for f in ifd:
                params['session'].delete(f)
            params['session'].commit()
        self.testataDocumentoScadenzaDel(dao=self)
        if posso("SM"):
            for r in self.righe:
                mp = MisuraPezzo().select(idRiga=r.id, batchSize=None)
                if mp:
                    for m in mp:
                        params['session'].delete(m)
                    params["session"].commit()
        for r in self.righe:
            nn = NumeroLottoTemp().select(idRigaMovimentoVenditaTemp=r.id, batchSize=None)
            if nn:
                for n in nn:
                    params["session"].delete(n)
                params["session"].commit()

            rmfa = RigaMovimentoFornitura().select(idRigaMovimentoAcquisto = r.id, batchSize=None)
            if rmfa:
                for f in rmfa:
                    if f.id_riga_movimento_vendita:
                        from promogest.lib.utils import messageError
                        messageError(msg="HAI RIMOSSO UN DOCUMENTO DI ACQUISTO DI CUI\n PARTE DEGLI ARTICOLI ERANO GIÀ STATI VENDUTI,\n I LOTTI NON SARANNO PIÙ NUMERICAMENTE CORRETTI")
                    params['session'].delete(f)
                params["session"].commit()

            precedentiRighe = RigaMovimentoFornitura().select(idRigaMovimentoVendita=r.id, batchSize=None)
            if precedentiRighe:
                for p in precedentiRighe:
                    p.id_riga_movimento_vendita = None
                    params["session"].add(p)
                params['session'].commit()
        params['session'].delete(self)
        params['session'].commit()

    def filter_values(self,k,v):
        contabili = ["Fattura vendita", "Fattura acquisto","Nota di credito a cliente",
            "Nota di credito da fornitore","Fattura accompagnatoria",
             "Vendita dettaglio","Fattura differita vendita", "Fattura differita acquisto"]
        if k == 'daNumero':
            dic = {k:t_testata_documento.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:t_testata_documento.c.numero <= v}
        elif k == 'numero':
            dic = {k:t_testata_documento.c.numero == v}
        elif k == 'parte':
            dic = {k:t_testata_documento.c.parte == v}
        elif k == 'daParte':
            dic = {k:t_testata_documento.c.parte >= v}
        elif k == 'aParte':
            dic = {k:t_testata_documento.c.parte <= v}
        elif k == 'daData':
            dic = {k:t_testata_documento.c.data_documento >= v}
        elif k== 'aData':
            dic = {k:t_testata_documento.c.data_documento <= v}
        elif k =='protocollo':
            dic = {k:t_testata_documento.c.protocollo.ilike("%"+v+"%")}
        elif k == 'idOperazione':
            dic = {k: t_testata_documento.c.operazione == v}
        elif k == 'idPagamento':
            dic = {k: t_testata_documento.c.id_pagamento == v}
        elif k == 'soloContabili':
            dic = {k: t_testata_documento.c.operazione.in_(contabili)}
        elif k == 'idCliente':
            dic = {k: t_testata_documento.c.id_cliente == v}
        elif k == 'idBanca':
            dic = {k: t_testata_documento.c.id_banca == v}
        elif k == 'idPrimoRiferimento':
            dic = {k: t_testata_documento.c.id_primo_riferimento == v}
        elif k == 'idClienteList':
            dic = {k: t_testata_documento.c.id_cliente.in_(v)}
        elif k == 'idFornitore':
            dic = {k:t_testata_documento.c.id_fornitore == v}
        elif k == 'idAgente':
            dic = {k:t_testata_documento.c.id_agente == v}
        elif k == 'statoDocumento':
            dic = {k:t_testata_documento.c.documento_saldato == v}
        elif k =="extra":
            if v == "tutti_vendita":
                dic = {k:t_testata_documento.c.operazione.in_(Environment.solo_vendita)}
            elif v == "tutti_acquisto":
                dic = {k:t_testata_documento.c.operazione.in_(Environment.solo_acquisto)}
            elif v == "tutti_acquisto_con_ddt":
                dic = {k:t_testata_documento.c.operazione.ilike("%acquisto%")}
        elif k == 'descrizioneRiga':
            dic = {k: and_(Riga.descrizione.ilike("%"+v+"%"),
                    Riga.id==RigaDocumento.id,
                    RigaDocumento.id_testata_documento == TestataDocumento.id)}

        elif k == 'idArticoloMov' or k == "idArticolo":
            dic = {k: and_(v ==Riga.id_articolo,
                    t_riga.c.id==RigaMovimento.id,
                    RigaMovimento.id_testata_movimento == TestataMovimento.id,
                    TestataMovimento.id_testata_documento == t_testata_documento.c.id)}
        elif k == 'idArticoloDoc':
            dic = {k: and_(v==Riga.id_articolo,
                    Riga.id==RigaDocumento.id,
                    RigaDocumento.id_testata_documento == TestataDocumento.id)}
        elif k == 'idMagazzino':
            dic = {k:and_(v == Riga.id_magazzino,
                    t_riga.c.id==RigaMovimento.id,
                    RigaMovimento.id_testata_movimento == TestataMovimento.id,
                    TestataMovimento.id_testata_documento == t_testata_documento.c.id)}

        elif k == 'daDataPagamento':
            dic = {k:and_(t_testata_documento.c.id == TestataDocumentoScadenza.id_testata_documento,
                            TestataDocumentoScadenza.data_pagamento >= v)}
        elif k== 'aDataPagamento':
            dic = {k:and_(t_testata_documento.c.id == TestataDocumentoScadenza.id_testata_documento,
                            TestataDocumentoScadenza.data_pagamento <= v)}

        elif (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in Environment.modulesList):
            if k == 'daDataInizioNoleggio':
                dic = {k:and_(t_testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_inizio_noleggio >= v)}
            elif k== 'aDataInizioNoleggio':
                dic = {k:and_(t_testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_inizio_noleggio <= v)}
            if k == 'daDataFineNoleggio':
                dic = {k:and_(t_testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_fine_noleggio >= v)}
            elif k== 'aDataFineNoleggio':
                dic = {k:and_(t_testata_documento.c.id == TestataGestioneNoleggio.id_testata_documento,
                            TestataGestioneNoleggio.data_fine_noleggio <= v)}
        return  dic[k]


if 'esclusione_spese' not in [c.name for c in t_testata_documento.columns]:
    try:
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        op.add_column('testata_documento', Column('esclusione_spese', Boolean, default=True),schema=params['schema'])
    except:
        delete_pickle()

if "codice_cup" not in [c.name for c in t_testata_documento.columns]:
    try:
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        op.add_column('testata_documento', Column('codice_cup', String(15), nullable=True), schema=params["schema"])
    except:
        delete_pickle()

if "codice_cig" not in [c.name for c in t_testata_documento.columns]:
    try:
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        op.add_column('testata_documento', Column('codice_cig', String(15), nullable=True), schema=params["schema"])
    except:
        delete_pickle()
        restart_program()


std_mapper = mapper(TestataDocumento, t_testata_documento,
    properties={
        "rigadoc": relation(RigaDocumento,
            cascade="all, delete",
            backref="testata_documento",
            ),
        "testata_documento_scadenza": relation(TestataDocumentoScadenza,
            cascade="all, delete",
            backref="testata_documento"),
        "PG": relation(Pagamento,
            primaryjoin=t_testata_documento.c.id_pagamento==t_pagamento.c.id),
        "BN": relation(Banca,
            primaryjoin=(t_testata_documento.c.id_banca==t_banca.c.id)),
        "AL": relation(AliquotaIva,
            primaryjoin=(t_testata_documento.c.id_aliquota_iva_esenzione==AliquotaIva.id)),
        "PV": relation(Vettore,
            primaryjoin=(t_testata_documento.c.id_vettore==t_vettore.c.id)),
        "DM": relation(DestinazioneMerce,
            primaryjoin=(t_testata_documento.c.id_destinazione_merce==DestinazioneMerce.id)),
        "TM": relation(TestataMovimento,
            primaryjoin=(t_testata_documento.c.id==t_testata_movimento.c.id_testata_documento),
            cascade="all, delete",
            backref='TD',lazy='joined'),
        "CLI": relation(Cliente,
            primaryjoin=(t_testata_documento.c.id_cliente==t_cliente.c.id), backref="TD"),
        "FORN": relation(Fornitore,
            primaryjoin=(t_testata_documento.c.id_fornitore==t_fornitore.c.id), backref="TD"),
        "AGE": relation(Agente,
            primaryjoin=(t_testata_documento.c.id_agente==t_agente.c.id)),
        "IFDDDT": relation(InformazioniFatturazioneDocumento,
            primaryjoin=(t_testata_documento.c.id==t_informazioni_fatturazione_documento.c.id_ddt)),
        "IFDFAT": relation(InformazioniFatturazioneDocumento,
            primaryjoin=(t_testata_documento.c.id==t_informazioni_fatturazione_documento.c.id_fattura)),
        "OP": relation(Operazione,
            primaryjoin=(t_testata_documento.c.operazione==Operazione.denominazione),
            backref="TD"),
        "STD": relation(ScontoTestataDocumento,
            primaryjoin=(t_testata_documento.c.id==ScontoTestataDocumento.id_testata_documento),
            cascade="all, delete",
            backref="TD"),
    },
    order_by=t_testata_documento.c.data_inserimento.desc())

if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in Environment.modulesList):
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
    std_mapper.add_property("TGN", relation(TestataGestioneNoleggio,
        primaryjoin=(t_testata_documento.c.id==TestataGestioneNoleggio.id_testata_documento),
        cascade="all, delete",
        backref=backref("TD"),
        uselist=False))

if tipodb=="sqlite":
    a = session.query(Banca.id).all()
    b = session.query(TestataDocumento.id_banca).all()
    fixit =  list(set(b)-set(a))
    print "fixt-td-banca", fixit
    for f in fixit:
        if f[0] != "None" and f[0] != None:
            aa = TestataDocumento().select(idBanca=f[0], batchSize=None)
            for a in aa:
                a.id_banca = None
                session.add(a)
    c = session.query(Pagamento.id).all()
    d = session.query(TestataDocumento.id_pagamento).all()
    fixit2 =  list(set(d)-set(c))
    print "fixt-td-pag", fixit2
    for f in fixit2:
        if f[0] != "None" and f[0] != None:
            aa = TestataDocumento().select(idPagamento=f[0], batchSize=None)
            for a in aa:
                a.id_pagamento = None
                session.add(a)
    session.commit()
    e = session.query(TestataDocumento.id).all()
    f = session.query(TestataDocumento.id_primo_riferimento).all()
    fixit3 =  list(set(f)-set(e))
    print "fixt-td-primo_pag", fixit3
    for f in fixit3:
        if f[0] != "None" and f[0] != None:
            aa = TestataDocumento().select(idPrimoRiferimento=f[0], batchSize=None)
            for a in aa:
                a.id_primo_riferimento = None
                session.add(a)
    session.commit()

#-*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
"""


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from RigaMovimento import RigaMovimento
from promogest.ui.utils import numeroRegistroGet
from Fornitore import Fornitore
from Cliente import Cliente
from Fornitura import Fornitura

class TestataNoleggio(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def _getRigheNoleggio(self):
        #if self.__dbRigheMovimento is None:
        self.__dbRigheNoleggio = params['session']\
                                        .query(RigaNoleggio)\
                                        .with_parent(self)\
                                        .filter_by(id_testata_noleggio=self.id)\
                                        .all()
        #if self.__righeMovimento is None:
        self.__righeNoleggio = self.__dbRigheNoleggio[:]
        return self.__righeNoleggio

    def _setRigheNoleggio(self, value):
        self.__righeNoleggio = value

    righe = property(_getRigheNoleggio, _setRigheNoleggio)

    def _ragioneSocialeFornitore(self):
        """ propery ragione sociale fornitore"""
        a = params['session'].query(Fornitore).with_parent(self).filter_by(id=self.id_fornitore).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale
    ragione_sociale_fornitore = property(_ragioneSocialeFornitore)

    def _ragioneSocialeCliente(self):
        """ property ragione sociale cliente """
        a = params['session'].query(Cliente).with_parent(self).filter_by(id=self.id_cliente).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale
    ragione_sociale_cliente= property(_ragioneSocialeCliente)

    def filter_values(self,k,v):
        dic= {  'daNumero': self.numero >= v,
                'aNumero':self.numero <= v,
                'daParte':self.parte >= v,
                'aParte' :self.parte <= v,
                'daData':self.data_movimento >= v,
                'aData': self.data_movimento <= v,
                'idOperazione': self.operazione == v,
                'idMagazzino': self.id.in_(select([RigaNoleggio.id_testata_noleggio],RigaNoleggio.id_magazzino== v)),
                'idCliente': self.id_cliente == v,
                'idFornitore': self.id_fornitore == v,
                'dataMovimento': self.data_movimento == v,
                'registroNumerazione': self.registro_numerazione==v,
                #'statoDocumento': testata_mov.c.stato_documento == v,
                #'idArticolo': testata_movimento.c.id_articolo == v  ARRIVANO QUI TRAMITE RIGA - RIGA DOCUMENTO
            }
        return  dic[k]

    def subPersist(self):
        """cancellazione righe associate alla testata
            conn.execStoredProcedure('RigheMovimentoDel',(self.id, ))"""
        def righeNoleggioDel(id=None):
            """Cancella le righe associate ad un movimento"""
            row = RigaNoleggio().select(idTestataNoleggio = id)

            for r in row:
                r.delete()
            return
        righeNoleggioDel(id=self.id)
        if self.__righeNoleggio is not None:
            for riga in self.__righeNoleggio:
                #annullamento id della riga
                riga._resetId()
                #associazione alla riga della testata
                riga.id_testata_noleggio = self.id
                #salvataggio riga
                riga.persist()
                if self.id_fornitore is not None:
                    """aggiornamento forniture
                        cerca la fornitura relativa al fornitore
                        con data <= alla data del movimento"""

                    # ATTENZIONE Direi che le forniture non debbano essere aggiornate
                    #fors = Dao(Fornitura).select(idArticolo=riga.id_articolo,
                                                            #idFornitore=self.id_fornitore,
                                                            #daDataPrezzo=None,
                                                            #aDataPrezzo=self.data_noleggio,
                                                            #orderBy = 'data_prezzo DESC',
                                                            #offset = None,
                                                            #batchSize = None)
                    #daoFornitura = None
                    #if len(fors) > 0:
                        #if fors[0].data_prezzo == self.data_noleggio:
                            ## ha trovato una fornitura con stessa data: aggiorno questa fornitura
                            #daoFornitura = Dao(Fornitura, id=fors[0].id).getRecord()
                        #else:
                            #"""creo una nuova fornitura con data_prezzo pari alla data del movimento
                                #copio alcuni dati dalla fornitura piu' prossima"""
                            #daoFornitura = Dao(Fornitura).getRecord()
                            #daoFornitura.scorta_minima = fors[0].scorta_minima
                            #daoFornitura.id_multiplo = fors[0].id_multiplo
                            #daoFornitura.tempo_arrivo_merce = fors[0].tempo_arrivo_merce
                            #daoFornitura.fornitore_preferenziale = fors[0].fornitore_preferenziale
                    #else:
                        ## nessuna fornitura utilizzabile, ne creo una nuova (alcuni dati mancheranno)
                        #daoFornitura = Dao(Fornitura).getRecord()

                    #daoFornitura.id_fornitore = self.id_fornitore
                    #daoFornitura.id_articolo = riga.id_articolo
                    #if daoFornitura.data_fornitura is not None:
                        #if self.data_movimento > daoFornitura.data_fornitura:
                            #daoFornitura.data_fornitura = self.data_movimento
                    #else:
                        #daoFornitura.data_fornitura = self.data_movimento
                    #daoFornitura.data_prezzo = self.data_movimento
                    #daoFornitura.codice_articolo_fornitore = riga.codiceArticoloFornitore
                    #daoFornitura.prezzo_lordo = riga.valore_unitario_lordo
                    #daoFornitura.prezzo_netto = riga.valore_unitario_netto
                    #daoFornitura.percentuale_iva = riga.percentuale_iva
                    #daoFornitura.applicazione_sconti = riga.applicazione_sconti
                    sconti = []
                    for s in riga.sconti:
                        daoSconto = ScontoFornitura()
                        daoSconto.id_fornitura = daoFornitura.id
                        daoSconto.valore = s.valore
                        daoSconto.tipo_sconto = s.tipo_sconto
                        sconti.append(daoSconto)

                    daoFornitura.sconti = sconti
                    daoFornitura.persist()

testata_nol=Table('testata_noleggio',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)
std_mapper = mapper(TestataNoleggio, testata_nol,properties={
        "rigamov": relation(RigaNoleggio, backref="testata_noleggio"),
        "fornitore": relation(Fornitore, backref="testata_noleggio"),
        "cliente": relation(Cliente, backref="testata_noleggio"),
        }
        )

sel_mapper = std_mapper
total_mapper = std_mapper

#TM.id IN (SELECT id_testata_movimento FROM v_riga_movimento WHERE id_magazzino = \' || _id_magazzino || \') \';




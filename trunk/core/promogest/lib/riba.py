# -*- coding: utf-8 -*-

'''
Copyright (c) 2011, Francesco Marella <francesco.marella@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Created on 09/dic/2011

@author: Francesco Marella <francesco.marella@gmail.com>
'''

__version__ = '0.9'

from struct import Struct
import datetime
    
#===============================================================================
# def validate(obj):
#    for key, val in vars(obj).iteritems():
#        if not val:
#            raise ValueError('Campo %s non valido' % key)
#===============================================================================


class Debitore:
    '''
    '''
    codice_fiscale = ' ' # codice_fiscale: codice fiscale del cliente debitore (CIN obbligatorio)
    CAP = ' '
    indirizzo = ' '
    provincia =  ' '
    comune = ' '
    descrizione = ' ' # descrizione del debitore (30 caratteri * 2)
    abi = ' '
    cab = ' '
    
    def __init__(self, codice_fiscale, abi, cab):
        self.codice_fiscale = codice_fiscale
        self.abi = abi
        self.cab = cab

class Creditore:
    '''
    Informazioni sul creditore.
    '''
    codice_sia = ' '
    descrizione = ' ' # descrizione del creditore (24 caratteri * 4) == data + abiazienda + cabazienda
    codice_fiscale = ' ' # codice fiscale o partita iva
    numero_conto = ' '
    denominazione_breve = ' '
    abi = ' '
    cab = ' '
    
    def __init__(self, codice_fiscale='', abi='', cab='', numero_conto='', denominazione_breve=' '):
        '''
        Costruttore
        
        @param codice_fiscale: codice fiscale del creditore
        @param abi: ABI del creditore
        @param cab: CAB del creditore
        @param numero_conto: numero di conto del creditore
        @param denominazione_breve: breve denominazione del creditore
        '''
        self.abi = abi
        self.cab = cab
        self.codice_fiscale = codice_fiscale
        self.numero_conto = numero_conto
        self.descrizione = '{0} {1} {2}'.format(datetime.datetime.now().strftime('%d%m%y'), abi, cab)
        self.denominazione_breve = denominazione_breve
        

class RiBa:
    '''
    Libreria di generazione delle ricevute Ri.Ba.
    
    L'implementazione non supporta la gestione del bollo virtuale.
    '''
    
    FILLER = ' '
    IBStruct = Struct('c2s5s5s6s20s6s59scc5s2scc5s')
    EFStruct = Struct('c2s5s5s6s20s6s7s15s15s7s24sc6s')
    R14Struct = Struct('c2s7s12s6s5s13sc5s5s12s5s5s12s5sc16sc5sc')
    R20Struct = Struct('c2s7s24s24s24s24s14s')
    R30Struct = Struct('c2s7s30s30s16s34s')
    R40Struct = Struct('c2s7s30s5s25s50s')
    R50Struct = Struct('c2s7s40s40s10s16s4s')
    R51Struct = Struct('c2s7s10s20s15s10s6s49s')
    R70Struct = Struct('c2s7s78s12sccc17s')
    
    
    def __init__(self, creditore):
        '''
        Inizializza il tracciato Ri.Ba.
        '''
        self._buffer = ''
        self._numero_record = 0
        self.creditore = creditore
        self.debitore = None
        self.data_flusso = datetime.datetime.now().strftime('%d%m%y')
        # numero disposizioni (ricevute ri.ba contenute nel flusso)
        self.totale_disposizioni = 0
        self.nome_supporto = 'INVIO DEL %s' % datetime.datetime.now().strftime('%d%m%y')
            
    def analizza(self, data_inizio=None):
        raise NotImplementedError()

    def write(self, filename):
        '''
        Scrive il tracciato Ri.Ba. su file di testo
        
        @param filename: file contenente il tracciato Ri.Ba.
        '''
        with open(filename, 'w') as f:
            f.write(self._buffer)
            
    def recordIB(self):
        '''
        Genera il testo del record IB
        
        @return: il testo del record IB
        '''
        return self.IBStruct.pack(self.FILLER,
                             'IB',
                             self.creditore.codice_sia,
                             self.creditore.abi,
                             self.data_flusso,
                             self.nome_supporto,
                             ' ', # campo a disposizione
                             self.FILLER,
                             # qualificatore flusso
                             ' ', # tipo flusso
                             '$', # qualificatore flusso
                             ' ',  # soggetto veicolatore    
                             self.FILLER,
                             'E',
                             self.FILLER,
                             ' ').replace('\0', self.FILLER)

   
    def recordEF(self, disposizioni, totale_importi):
        '''
        Genera il testo del record EF
        
        @param disposizioni: numero di disposizioni
        @param totale_importi: totale importi negativi
        @param record: numero dei record che compongono il flusso
        @return: il testo del record EF
        '''
        return self.EFStruct.pack(self.FILLER,
                                  'EF',
                                  self.creditore.codice_sia,
                                  self.creditore.abi,
                                  self.data_flusso,
                                  self.nome_supporto,
                                  ' ', # campo a disposizione
                                  str(disposizioni),
                                  str(totale_importi),
                                  '0'*15, # totale importi positivi
                                  str(disposizioni + 2),
                                  self.FILLER,
                                  'E', # codice divisa
                                  self.FILLER).replace('\0', self.FILLER)
        
    def record14(self, progressivo, data_pagamento, importo, debitore):
        '''
        Genera il testo del record 14
        
        @param progressivo: numero progressivo
        @param data_pagamento: data di pagamento
        @param importo: importo della ricevuta in cent
        @param debitore: informazioni sul debitore
        @return: il testo del record 14
        '''
        return self.R14Struct.pack(self.FILLER,
                                   '14',
                                   str(progressivo),
                                   self.FILLER,
                                   str(data_pagamento.strftime('%d%m%y')),
                                   '30000', # causale
                                   str(importo),
                                   '-', # segno
                                   str(self.creditore.abi),
                                   str(self.creditore.cab),
                                   str(self.creditore.numero_conto),
                                   str(debitore.abi),
                                   str(debitore.cab),
                                   self.FILLER,
                                   ' ', # codice azienda
                                   '4',
                                   ' ', # codice cliente debitore
                                   ' ', # flag tipo debitore ('B' per banca)
                                   self.FILLER,
                                   'E').replace('\0', self.FILLER)
    
    def record20(self, progressivo):
        '''
        Genera il testo del record 20
        
        @param progressivo: numero progressivo
        @return: il testo del record 20
        '''
        descr = list([self.creditore.descrizione[0:24],
                      self.creditore.descrizione[24:24*2],
                      self.creditore.descrizione[24*2:24*3],
                      self.creditore.descrizione[24*3:24*4]])
        return self.R20Struct.pack(self.FILLER,
                                    '20',
                                    str(progressivo),
                                    # descrizione del creditore
                                    descr[0] or ' ',
                                    descr[1] or ' ',
                                    descr[2] or ' ',
                                    descr[3] or ' ',
                                    self.FILLER).replace('\0', self.FILLER)
    
    def record30(self, progressivo, debitore):
        '''
        Genera il testo del record 30
        
        @param progressivo: numero progressivo
        @param debitore: informazioni sul debitore
        @return: il testo del record 30
        '''
        descr = list([debitore.descrizione[0:30], debitore.descrizione[30:60]])
        return self.R30Struct.pack(self.FILLER,
                                     '30',
                                     str(progressivo),
                                     # descrizione del debitore (30 caratteri ognuno)
                                     descr[0] or ' ',
                                     descr[1] or ' ',
                                     str(debitore.codice_fiscale),
                                     self.FILLER).replace('\0', self.FILLER)
    
    def record40(self, progressivo, debitore):
        '''
        Genera il testo del record 40
        
        @param progressivo: numero progressivo
        @param debitore: informazioni sul debitore
        @return: il testo del record 40
        '''
        return self.R40Struct.pack(self.FILLER,
                                   '40',
                                   str(progressivo),
                                   # indirizzo del debitore
                                   str(debitore.indirizzo),
                                   str(debitore.CAP),
                                   '{0} {1}'.format(debitore.comune, debitore.provincia),
                                   ' ').replace('\0', self.FILLER) # eventuale denominazione in chiaro della banca/sportello domiciliataria/o

    def record50(self, progressivo, debitore, riferimenti_debito):
        '''
        Genera il testo del record 50
        
        @param progressivo: numero progressivo
        @param debitore: informazioni sul debitore
        @param riferimenti_debito: riferimenti al debito
        @return: il testo del record 50
        '''
        rif_debito = list([riferimenti_debito[0:40], riferimenti_debito[40:80]])
        return self.R50Struct.pack(self.FILLER,
                                   '50',
                                   str(progressivo),
                                   # riferimenti al debito
                                   rif_debito[0] or ' ',
                                   rif_debito[1] or ' ',
                                   self.FILLER,
                                   str(self.creditore.codice_fiscale),
                                   self.FILLER).replace('\0', self.FILLER)
    
    def record51(self, progressivo, ricevuta):
        '''
        Genera il testo del record 51
        
        @param progressivo: numero progressivo
        @param ricevuta: numero ricevuta attribuito dal creditore
        @return: il testo del record 51
        '''
        return self.R51Struct.pack(self.FILLER,
                                   '51',
                                   str(progressivo),
                                   str(ricevuta),
                                   str(self.creditore.denominazione_breve),
                                   # bollo virtuale
                                   ' ', # provincia
                                   ' ', # numero autorizzazione
                                   ' ', # data autorizzazione
                                   self.FILLER).replace('\0', self.FILLER)
    
    def record70(self, progressivo):
        '''
        Genera il testo del record 70
        
        @param progressivo: numero progressivo
        @return: il testo del record 70
        '''
        return self.R70Struct.pack(self.FILLER,
                                   '70',
                                   str(progressivo),
                                   self.FILLER,
                                   ' ', # indicatori di circuito
                                   # indicatore richiesta incasso
                                   '0', # tipo doc per debitore 
                                        # 1=ricevuta bancaria
                                        # 2=conferma d'ordine di bonifico
                                        # 0 o blank = accordi bilaterali predefiniti con la banca
                                   '0', # flag richiesta esito
                                        # 1= richiesta notifica del pagato
                                        # 2= non è richiesta la notifica del pagato
                                        # 0 o blank = accordi bilaterali predefiniti con la banca
                                   '0', # flag stampa avviso
                                        # 4=avvisi da predisporre e da inviare a cura della banca domiciliaria
                                        # 0 o blank = accordi bilaterali predefiniti con la banca
                                   self.FILLER).replace('\0', self.FILLER)

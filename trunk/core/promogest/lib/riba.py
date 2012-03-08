# -*- coding: utf-8 -*-

'''
Copyright (c) 2011-2012 Francesco Marella <francesco.marella@gmail.com>

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

__version__ = '1.0'

from struct import Struct
import datetime
import unicodedata

#===============================================================================
# def validate(obj):
#    for key, val in vars(obj).iteritems():
#        if not val:
#            raise ValueError('Campo %s non valido' % key)
#===============================================================================

def as_string(arg, lenght):
    try:
        arg = unicode(arg, 'UTF-8')
    except TypeError:
        pass
    arg = unicodedata.normalize('NFKD', arg).encode('ASCII', 'ignore')
    return str(arg).ljust(lenght, ' ')

def as_number(arg, lenght):
    return str(arg).rjust(lenght, '0')

def as_currency(arg, lenght, decimal=2):
    args = str(arg).split('.')
    if len(args) == 1:
        return str(args[0][:int(lenght)].rjust(int(lenght), '0'))
    else:
        return str(args[0][:int(lenght-decimal)].rjust(int(lenght-decimal), '0') + args[1][:decimal].rjust(decimal, '0'))


class Debitore(object):
    '''
    '''
    codice_fiscale = ' ' # codice_fiscale: codice fiscale del cliente debitore (CIN obbligatorio)
    CAP = ' '
    indirizzo = ' '
    provincia =  ' '
    comune = ' '
    descrizione = ['','']
    abi = ' '
    cab = ' '

    def __init__(self, codice_fiscale, abi, cab):
        self.codice_fiscale = codice_fiscale
        self.abi = abi
        self.cab = cab

class Creditore(object):
    '''
    Informazioni sul creditore.
    '''
    codice_sia = ' '
    descrizione = ' ' # descrizione del creditore (24 caratteri * 4) == data + abiazienda + cabazienda
    codice_fiscale = ' ' # codice fiscale o partita iva
    numero_conto = ' '
    denominazione_breve = ' '
    descrizione = ['','','','']
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
        self.descrizione[3] = codice_fiscale
        self.denominazione_breve = denominazione_breve # nome dell azienda
        


class RiBa(object):
    '''
    Libreria di generazione delle ricevute Ri.Ba.

    L'implementazione non supporta la gestione del bollo virtuale.
    '''

    FILLER = ' '
    EOL = '\n'
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

        @param creditore: informazioni sul creditore
        '''
        self._buffer = ''
        self.creditore = creditore
        self.data_flusso = datetime.datetime.now().strftime('%d%m%y')
        self.nome_supporto = 'CBIRIB%s' % datetime.datetime.now().strftime('%d%m%y%H%M')

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
                             as_string(self.creditore.codice_sia, 5),
                             as_number(self.creditore.abi, 5),
                             self.data_flusso,
                             as_string(self.nome_supporto, 20),
                             as_string(' ', 6), # campo a disposizione
                             as_string(' ', 59),
                             # qualificatore flusso
                             '1', # tipo flusso 1
                             '$', # qualificatore flusso $
                             as_string(self.creditore.abi, 5),  # soggetto veicolatore
                             as_number('0', 2),
                             'E',
                             self.FILLER,
                             as_number('0', 2)).replace('\0', self.FILLER) + self.EOL


    def recordEF(self, disposizioni, totale_importi):
        '''
        Genera il testo del record EF

        @param disposizioni: numero di disposizioni
        @param totale_importi: totale importi negativi
        @return: il testo del record EF
        '''
        return self.EFStruct.pack(self.FILLER,
                                  'EF',
                                  as_string(self.creditore.codice_sia, 5),
                                  as_number(self.creditore.abi, 5),
                                  self.data_flusso,
                                  as_string(self.nome_supporto, 20),
                                  as_string(' ', 6), # campo a disposizione
                                  as_number(disposizioni, 7),
                                  as_currency(totale_importi, 15),
                                  as_number('0', 15), # totale importi positivi
                                  as_number(disposizioni * 7 + 2, 7),
                                  as_string(self.FILLER, 24),
                                  'E', # codice divisa
                                  as_string(self.FILLER, 6)).replace('\0', self.FILLER)

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
                                   as_number(str(progressivo), 7),
                                   as_string(self.FILLER, 12),
                                   str(data_pagamento.strftime('%d%m%y')),
                                   '30000', # causale
                                   as_currency(importo, 13),
                                   '-', # segno
                                   as_number(self.creditore.abi, 5),
                                   as_number(self.creditore.cab, 5),
                                   as_number(self.creditore.numero_conto, 12),
                                   as_number(debitore.abi, 5),
                                   as_number(debitore.cab, 5),
                                   as_string(self.FILLER, 12),
                                   as_string(self.creditore.codice_sia, 5),
                                   '4',
                                   as_string(' ', 16), # codice cliente debitore
                                   ' ', # flag tipo debitore ('B' per banca)
                                   as_string(self.FILLER, 5),
                                   'E').replace('\0', self.FILLER) + self.EOL

    def record20(self, progressivo):
        '''
        Genera il testo del record 20

        @param progressivo: numero progressivo
        @return: il testo del record 20
        '''
        return self.R20Struct.pack(self.FILLER,
                                    '20',
                                    as_number(str(progressivo), 7),
                                    # descrizione del creditore
                                    as_string(self.creditore.descrizione[0], 24), #nome azienda
                                    as_string(self.creditore.descrizione[1], 24), # indirizzo
                                    as_string(self.creditore.descrizione[2], 24), # località
                                    as_string(self.creditore.descrizione[3], 24), # codice fiscale
                                    as_string(self.FILLER, 14)).replace('\0', self.FILLER) + self.EOL

    def record30(self, progressivo, debitore):
        '''
        Genera il testo del record 30

        @param progressivo: numero progressivo
        @param debitore: informazioni sul debitore
        @return: il testo del record 30
        '''
        return self.R30Struct.pack(self.FILLER,
                                     '30',
                                     as_number(str(progressivo), 7),
                                     # descrizione del debitore (30 caratteri ognuno)
                                     as_string(debitore.descrizione[0], 30),
                                     as_string(debitore.descrizione[1], 30),
                                     as_string(debitore.codice_fiscale, 16),
                                     as_string(self.FILLER, 34)).replace('\0', self.FILLER) + self.EOL

    def record40(self, progressivo, debitore):
        '''
        Genera il testo del record 40

        @param progressivo: numero progressivo
        @param debitore: informazioni sul debitore
        @return: il testo del record 40
        '''
        return self.R40Struct.pack(self.FILLER,
                                   '40',
                                   as_number(str(progressivo), 7),
                                   # indirizzo del debitore
                                   as_string(debitore.indirizzo, 30),
                                   as_number(debitore.CAP, 5),
                                   as_string('{0} {1}'.format(debitore.comune, debitore.provincia), 25),
                                   as_string(' ', 50)).replace('\0', self.FILLER) + self.EOL # eventuale denominazione in chiaro della banca/sportello domiciliataria/o

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
                                   as_number(str(progressivo), 7),
                                   # riferimenti al debito
                                   as_string(rif_debito[0], 40),
                                   as_string(rif_debito[1], 40),
                                   as_string(self.FILLER, 10),
                                   as_string(self.creditore.codice_fiscale, 16),
                                   as_string(self.FILLER, 4)).replace('\0', self.FILLER) + self.EOL

    def record51(self, progressivo, ricevuta):
        '''
        Genera il testo del record 51

        @param progressivo: numero progressivo
        @param ricevuta: numero ricevuta attribuito dal creditore
        @return: il testo del record 51
        '''
        return self.R51Struct.pack(self.FILLER,
                                   '51',
                                   as_number(str(progressivo), 7),
                                   as_number(ricevuta, 10),
                                   as_string(self.creditore.denominazione_breve, 20),
                                   # bollo virtuale
                                   as_string(' ', 15), # provincia
                                   as_number('0', 10), # numero autorizzazione
                                   as_number('0', 6), # data autorizzazione
                                   as_string(' ', 49)).replace('\0', self.FILLER) + self.EOL

    def record70(self, progressivo):
        '''
        Genera il testo del record 70

        @param progressivo: numero progressivo
        @return: il testo del record 70
        '''
        return self.R70Struct.pack(self.FILLER,
                                   '70',
                                   as_number(str(progressivo), 7),
                                   as_string(self.FILLER, 78),
                                   as_string(' ', 12), # indicatori di circuito
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
                                   as_string(self.FILLER, 17)).replace('\0', self.FILLER) + self.EOL

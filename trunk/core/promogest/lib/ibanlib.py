# -*- coding: utf-8 -*-

#    Copyright (C) 2011-2012 Francesco Marella <francesco.marella@anche.no>

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

from struct import Struct

CARATTERI = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-. "
CIFRE = "0123456789"
DIVISORE = 26
PARI = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
DISPARI = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23, 27, 28, 26]

IT_IBAN_Struct = Struct('2s2sc5s5s12s')
(COUNTRY, CS, CIN, ABI, CAB, NCONTO) = range(6)

def dividi_iban(iban):
    '''Ritorna una lista con i codici che compongono il codice iban
    '''
    try:
        return IT_IBAN_Struct.unpack(iban.upper())
    except:
        raise Exception('Il codice IBAN non è valido.')

def calcolo_cin(abi, cab, numero_conto):
    stringa = ''

    # controlli su abi, cab, numero di conto
    if len(abi) != 5 or len(cab) != 5 or len(numero_conto) > 12 or len(numero_conto) < 1:
        raise Exception('Lunghezza di ABI o CAB o Numero di conto errata.')

    if len(numero_conto) == 12:
        stringa = str(abi + cab + numero_conto)
    else:
        stringa = str(abi + cab) + str(numero_conto).rjust(12, '0')
    stringa = stringa.upper()

    totale = 0

    for i in range(22):
        curr_char = stringa[i]
        posizione = CIFRE.index(curr_char)
        if posizione < 0:
            posizione = CARATTERI.index(curr_char)
            if posizione < 0:
                raise Exception('Carattere non valido trovato in posizione {0}.'.format(i))
        if i % 2 == 0:
            totale += DISPARI[posizione]
        else:
            totale += PARI[posizione]
    x = int(totale % DIVISORE)
    return CARATTERI[x]

def mod97(digit):
    return long(digit) % 97

def calcolo_bban(abi, cab, numero_conto):
    return calcolo_cin(abi, cab, numero_conto) + str(abi) + str(cab) + str(numero_conto).rjust(12, '0')

def calcolo_iban(nazione, abi, cab, numero_conto):
    digits = ''
    bban = calcolo_bban(abi, cab, numero_conto)
    for ch in bban.upper():
        if ch.isdigit():
            digits += ch
        else:
            digits += str(ord(ch) - ord("A") + 10)
    for ch in nazione:
        digits += str(ord(ch) - ord("A") + 10)
    checksum = 98 - mod97(digits)
    return str(nazione) + str(checksum).rjust(2, '0') + str(bban)

if __name__ == "__main__":
    assert calcolo_cin('01000', '16600', '000000123456') == 'K'
    assert calcolo_cin('12345', '54321', '000000001234') == 'O'
    assert calcolo_bban('12345', '54321', '000000001234') == 'O1234554321000000001234'
    assert calcolo_iban('IT', '12345', '12345', '123456789012') == 'IT98Z1234512345123456789012'
    assert dividi_iban('IT98Z3214512345123456789012')[ABI] == '32145' 

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011-2012 Francesco Marella <francesco.marella@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Created on 20/01/2011
# Author: Francesco Marella <francesco.marella@gmail.com>

__version__ = '1.0'

"""
Parser

records: Contiene informazioni sui record come la lunghezza complessiva

record: contiene informazioni sul singolo record; deve avere un nome
 |
 |-- nome = str
 |-- repeat = 0 se il record deve essere ripetuto, 1 altrimenti.
field:
 |
 |-- align: allineamento a sinistra, destra o centrato (risp. left, right, center)
 |          Default:
 |           - stringa: a sinistra
 |           - intero o decimale: a destra
 |           - data: non applicato
 |
 |-- type: Tipo di dato (int, str, float, datetime)
 |
 |-- format: per il tipo datetime (data) specificare il formato riconosciuto dal
 |           modulo datetime di python, default=gg/mm/AAAA
 |
 |-- test: valore di test per il campo (per il tipo datetime usare now)
 |
 |-- sep: Il separatore da applicare al tipo float; default='.'
 |
 |-- sign: Segno e posizione del segno:
           - start : mette il segno nella prima posizione allineato a sinistra
           - yes   : conserva il segno, default
           - no    : non inserisce mai il segno
          

TODO:

- possibilità di processare file dati da importare

- inserendo il tipo e formato data ma non viene passato nessun dato
  oppure viene passato un oggetto non datetime:

Traceback (most recent call last):
  File "./parser.py", line 221, in <module>
    myparse(args.infile, dati, args.outfile)
  File "./parser.py", line 198, in myparse
    tmp = __process(field, el, dati)
  File "./parser.py", line 111, in __process
    _value_str = _value.strftime(_format)
AttributeError: 'str' object has no attribute 'strftime'

- implementare eventuali controlli sulla lunghezza della riga

- migliorare la gestione delle eccezioni

"""

from xml.dom.minidom import parse
from datetime import datetime


class ProcessError(Exception): pass
class ParserError(Exception): pass

def myparse(metadata_xml, dati, out, test=None, verbose=None):
    """

    @param metadata_xml: file metadati
    @param dati: dati da processare
    @param out: file di output
    @param test: utilizzare i tag test
    @param verbose: debug del tracciato
    """

    def __log(message):
        if verbose:
            print(message)

    def __process(field, el, dati):

        _name = str(field.getAttribute('name')) or None
        if _name is None:
            raise ProcessError("Il campo non possiede l'attributo nome.")

        _value = None

        if test:
            _value = field.getAttribute('test') or field.getAttribute('value')
        else:
            _value = field.getAttribute('value') or None
            if _value is None:
                try:
                    _value = dati[_name]
                except:
                    _value = ''

        if field.getAttribute('required') == '1' and not _value:
            raise ProcessError("Attenzione: il campo obbligatorio \'%s\' di \'%s\' non è stato inserito." % (_name, el))

        _value_str = str(_value)

        _type = str(field.getAttribute('type'))
        if _type == '':
            raise ProcessError("Attenzione: il tipo per il campo \'%s\' di \'%s\' non è stato inserito." % (_name, el))

        _len = 0
        try:
            _len = int(field.getAttribute('len'))
        except:
            raise ProcessError("L'attributo len di \'%s\' di \'%s\' è mancante o non è un numero." % (_name, el))

        _align = str(field.getAttribute('align'))
#        if _align == '':
#            _align = ''

        _format = str(field.getAttribute('format'))
        if _format == '':
            _format = "%d/%m/%Y"

        _fill = str(field.getAttribute('fill'))
        if _fill == '':
            _fill = ' '

        _sep = str(field.getAttribute('sep'))

        _sign = str(field.getAttribute('sign'))
        if _sign == '':
            _sign = 'yes'

        _fn = None

        if _type:
            if _type == 'datetime':
                if _value is 'now':
                    _value_str = datetime.now().strftime(_format)
                elif _value is '':
                    _value_str = ''
                    _fill = '0'
                    _align = 'right'
                else:
                    _value_str = _value.strftime(_format)
            elif _type == 'float':
                if _align is '':
                    _align = 'right'
                if len(_value_str) > 0 and '.' in _value_str:
                    _decimal = int(field.getAttribute('decimal'))
                    try:
                        _value_array = str(_value).split('.')
                        if len(str(_value_array[0])) > int(_len-_decimal):
                            __log("Attenzione: la parte intera eccede la lunghezza consentita!")
                        if len(str(_value_array[1])) > int(_decimal):
                            __log("Attenzione: la parte decimale eccede la lunghezza consentita! Verranno troncate le cifre meno significative.")
                            _value_array[1] = str(_value_array[1])[:_decimal]
                        _value_str = _value_array[0].rjust(int(_len-_decimal), _fill) + _sep +  _value_array[1].rjust(_decimal, _fill)
                    except Exception as e:
                        print(str(e))
                        _value_str = ''
                else:
                    print("Attenzione: nessun valore per il campo float.")
            elif _type == 'int':
                if _align is '':
                    _align = 'right'
            elif _type == 'str':
                if _align is '':
                    _align = 'left'
                # Tronca la stringa alla lunghezza specificata
                _value_str = _value_str[:_len]
            else:
                print('Attenzione: Tipo \'%s\' non supportato.' % _type)

        # Traduci align in funzione
        if _align:
            if _align == 'left':
                _fn = 'ljust'
            elif _align == 'right':
                _fn = 'rjust'
            elif _align == 'center':
                _fn = 'center'
            else:
                print('Attenzione: Valore di allineamento \'%s\' non supportato.' % _align)

        # Applica eventuali funzioni
        if _len:
            if _fn == 'center':
                _value_str = getattr(_value_str, str(fn))(_len)
            elif _fn in ['rjust', 'ljust']:
                _value_str = getattr(_value_str, str(_fn))(_len, _fill)
            else:
                pass

        return str(_value_str)

    # end __process

    if not test and dati == dict():
        raise ParserError("Nessun dato passato al parser.\n\nIn alternativa potresti usare l'attributo test di ciascun campo!")
    
    try:
        dom1 = parse(metadata_xml)
    except:
        raise ParserError("File metadata non valido.")
    finally:
        metadata_xml.close()

    __log("Parsing XML metadata and data.")

    records = dom1.getElementsByTagName("records")[0]

    len_riga = None
    try:
        len_riga = int(records.getAttribute('len'))
    except:
        pass

    _fineriga = records.getAttribute('eol') or '\n'
    
    __log("\tLunghezza della singola linea del tracciato: %s" % len_riga)

    for record in records.getElementsByTagName("record"):
        el = str(record.getAttribute('name'))   
        _repeat = str(record.getAttribute('repeat')) or '0'

        __log("\tProcessiamo il record: %s" % el)

        if _repeat == '1':
            #TODO: implementare dei controlli sul tipo, dati[el] deve esseere una lista

            for baz in dati[el]:
                for field in record.getElementsByTagName('field'):
                    __log("\t\tProcessiamo il campo: %s" % field.getAttribute('name'))

                    try:
                        tmp = __process(field, el, baz)
                    except ProcessError as err:
                        print(str(err))

                    out.write(tmp)
                if _fineriga == 'nl':
                    out.write('\n')
                if _fineriga == 'nlcr':
                    out.write('\n\r')
        else:
            for field in record.getElementsByTagName('field'):
                __log("\t\tProcessiamo il campo: %s" % field.getAttribute('name'))
                try:
                    tmp = __process(field, el, dati[el])
                except ProcessError as err:
                    print(str(err))

                out.write(tmp)
            if _fineriga == 'nl':
                out.write('\n')
            if _fineriga == 'nlcr':
                out.write('\n\r')

    __log("Processo terminato.")
    out.close()

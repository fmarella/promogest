# -*- coding: utf-8 -*-
#! /usr/bin/env python

#    Copyright (C) 2011-2012 Francesco Marella <francesco.marella@gmail.com>

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


__version__ = '15122011'

from struct import Struct

class IBANError(Exception):
    pass

IT_IBAN_Struct = Struct('2s2sc5s5s12s')

def check_iban(iban):
    iban = iban.upper()
    try:
        return IT_IBAN_Struct.unpack(iban)
    except:
        raise IBANError('Il codice IBAN non è corretto.')

__iban_data = {
             'AD': ['Andorra'],
             'IT': ['Italy'],
             'IS': ['Iceland']
             }

def country_data(code):
    """Search the country code in the iban_data list."""
    if code in __iban_data.keys():
        return __iban_data[code][0]
    else:
        return None

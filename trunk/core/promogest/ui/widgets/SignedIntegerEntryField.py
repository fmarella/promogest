# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from UnsignedIntegerEntryField import UnsignedIntegerEntryField

class SignedIntegerEntryField(UnsignedIntegerEntryField):
# Effettua la validazione per interi con segno
    __gtype_name__ = 'SignedIntegerEntryField'
    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        UnsignedIntegerEntryField.__init__(self, str1, str2, int1, int2)

        self.acceptedKeys += self.signKeys

#gobject.type_register(SignedIntegerEntryField)

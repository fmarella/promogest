# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
import gobject
import pygtk
import locale
from UnsignedIntegerEntryField import UnsignedIntegerEntryField

class SignedIntegerEntryField(UnsignedIntegerEntryField):
# Effettua la validazione per interi con segno

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        UnsignedIntegerEntryField.__init__(self, str1, str2, int1, int2)

        self.acceptedKeys += self.signKeys

#gobject.type_register(SignedIntegerEntryField)

# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
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

import hashlib
from promogest.ui.utils import orda
from promogest import Environment
from promogest.dao.Setconf import SetConf
from promogest.dao.SectionUser import SectionUser
from GladeWidget import GladeWidget
import datetime

class SetConfUI(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main):
        pass


codice=  SetConf().select(key="install_code",section="Master")
if codice:
    if codice[0].value =="ad2a57ed2bd4d4df494e174b576cf8e822a18be2e1b074871c69b31f":
        codice[0].value = "8f0eff136d1fb1d2b76fde5de7c83eb60d558c4f155ee687dcac5504"
        codice[0].persist()

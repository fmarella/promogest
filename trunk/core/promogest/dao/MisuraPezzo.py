# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: francesco Meloni <francesco@promotux.it>

from Dao import Dao
from promogest import Environment

class MisuraPezzo(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)




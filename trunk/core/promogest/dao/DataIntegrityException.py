# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
#




class DataIntegrityException(Exception):
    __value = None

    def __init__(self, value):
        Exception.__init__(self, value)
        self.__value = value

    def __str__(self):
        return repr(self.__value)

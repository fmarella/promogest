#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import pysvn

client = pysvn.Client()
client.exception_style = 0
client.update('.')

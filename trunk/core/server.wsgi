#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
sys.stdout = sys.stderr
path = '/home/promo/janas-promoSites/'
if path not in sys.path:
    sys.path.append(path)
from janas import app
application =app

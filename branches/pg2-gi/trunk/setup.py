#!/usr/bin/env python

#Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Maccis <amaccis@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import glob
from distutils.core import setup

setup(name='PromoGest2',
      version='2.0.0-rev341',
      license="GNU GENERAL PUBLIC LICENSE (see LICENSE for details), Copyright (c) 2005, Promotux Informatica",
      description='PROMOGEST Gestionale Open Source',
      author='PromoTux Informatica',
      author_email='info@promotux.it',
      url='http://promogest.promotux.it/',
      package_dir = {'':'core'},                #stabilisce /core come dir dei packages
      packages = [
                'promogest',
                'promogest.dao',
                'promogest.lib',
                'promogest.ui',
                'promogest.modules',
                'promogest.ui.widgets',
                ],
      scripts = ['core/promogest.py'],          #include gli scripts eseguibili
      py_modules = [                              #include i moduli fuori da un package
                    'config',
                   ],
      package_data = [                              #include tutti i files non .py fuori dai packages
                   ('.',[
                        'INSTALL',
                        'reinstalla.sh',
                        'installa.sh',
                        'aggiornamentoPromoGest2.sh',
                        'disinstalla.sh',
                        ]
                    ),
                   ('core',[
                                'core/configure.dist',
                                'core/LICENSE',
                             ]
                   ),
                   ('core/data',glob.glob('core/data/*')),
                   ('core/desktop',glob.glob('core/desktop/promoGest')),
                   ('core/desktop/gnome/',glob.glob('core/desktop/gnome/promogest.desktop')),
                   ('core/desktop/kde/',glob.glob('core/desktop/kde/promogest.desktop')),
                   ('core/gui',glob.glob('core/gui/*.*')),
                   ('core/gui/icon',glob.glob('core/gui/icon/*')),
                   ('core/report-templates',glob.glob('core/report-templates/*')),
                   ('core/templates',glob.glob('core/templates/*')),
                   ],
    )

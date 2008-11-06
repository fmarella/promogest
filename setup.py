#Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Maccis <amaccis@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import glob
from distutils.core import setup

setup(name='promogest',
      version='1.9.9.9',
      license="GNU GENERAL PUBLIC LICENSE (see LICENSE for details), Copyright (c) 2005, Promotux Informatica",
      description='PROMOGEST Gestionale Open Source',
      author='Promotux Informatica',
      author_email='info@promotux.it',
      url='http://promogest.promotux.it/',
      package_dir = {'':'core'},                #stabilisce /python come dir dei packages
      packages = [
                'promogest',
                'promogest.dao',
                'promogest.db',
                'promogest.lib',
                'promogest.ui',
                'promogest.modules',
                'promogest.modules.Pagamenti',
                'promogest.modules.Vetreria',
                'promogest.ui.plus',
                'promogest.ui.widgets',
                ],
      scripts = ['core/promogest.py'],          #include gli scripts eseguibili
      py_modules = [                              #include i moduli fuori da un package
                    'config',
                   ],
      data_files = [                              #include tutti i files non .py fuori dai packages
                   ('.',['INSTALL']),
                   #('data/app',glob.glob('data/app/*')),
                   #('data/bin',glob.glob('data/bin/*')),
                   #('data/reg/sp',glob.glob('data/reg/sp/*')),
                   #('data/reg/tab/promogest',glob.glob('data/reg/tab/*.sql')),
                   #('data/reg/tab/promogest',glob.glob('data/reg/tab/promogest/*')),
                   #('data/reg/view',glob.glob('data/reg/view/*')),
                   #('data/sys',glob.glob('data/sys/*.sql')),
                   #('data/sys',glob.glob('data/sys/*.sh')),
                   #('data/sys/sp',glob.glob('data/sys/sp/*')),
                   ('doc',glob.glob('doc/*')),
                   #('install_db',glob.glob('install_db/*')),
                   ('core',[
                                'core/configure.dist',
                                'core/LICENSE',
                             ]
                   ),
                   ('core/desktop',glob.glob('core/desktop/promoGest')),
                   ('core/desktop/gnome/',glob.glob('core/desktop/gnome/promogest.desktop')),
                   ('core/desktop/kde/',glob.glob('core/desktop/kde/promogest.desktop')),
                   ('core/gui',glob.glob('core/gui/*.*')),
                   ('core/gui/icon',glob.glob('core/gui/icon/*')),
                   ('core/report-templates',glob.glob('core/report-templates/*')),
                   ('core/templates',glob.glob('core/templates/*')),
                   ],
    )

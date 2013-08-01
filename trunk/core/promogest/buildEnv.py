# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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


import os
import sys
import shutil
import glob
from promogest.lib.config import Config
from promogest.EnvUtils import getConfigureDir
from promogest import Environment

#""" Sets configuration value """
def set_configuration(company=None, year = None, pg_path=None):
    #global conf,connection, exceptionHandler, promogestDir, feed,  emailcompose,\
                #emailmittente, smtpServer, \
                #multilinelimit, mltext,\
                #imagesDir, labelTemplatesDir, templatesDir, documentsDir, reportTemplatesDir,\
                #bordoDestro, bordoSinistro, magazzini, listini, tempDir, tracciatiDir
    dire = getConfigureDir(company)
    promogestDir = None
    if pg_path:
        promogestDir = os.path.join(pg_path, dire) + os.sep
    else:
        promogestDir = os.path.join(os.path.expanduser('~'), dire) + os.sep
    Environment.promogestDir = promogestDir
    if not (os.path.exists(promogestDir)):
        os.mkdir(promogestDir)
    cartelle = ["documenti", "tracciati", "temp", "templates", "label-templates", "images"]
    for c in cartelle:
        pa = promogestDir + c + os.sep
        if not (os.path.exists(pa)):
            os.mkdir(pa)
        if c == "documenti":
            Environment.documentsDir = pa
        elif c == "tracciati":
            Environment.tracciatiDir = pa
        elif c == "temp":
            Environment.tempDir = pa
        elif c == "images":
            Environment.imagesDir = pa
        elif c == "templates":
            Environment.templatesDir = pa
            slas = glob.glob(os.path.join(c, '*.sla'))
            for s in slas:
                try:
                   with open(pa+s.split(os.sep)[1]) as f: pass
                except IOError as e:
                   shutil.copy(s, pa)
        elif c == "label-templates":
            Environment.labelTemplatesDir = pa
            slas = glob.glob(os.path.join(c, '*.sla'))
            for s in slas:
                try:
                   with open(pa+s.split(os.sep)[1]) as f: pass
                except IOError as e:
                   shutil.copy(s, pa)

    try:
        configFile = promogestDir + 'configure'
        conf = Config(configFile)
    except IOError:
        configFile = promogestDir + 'configure'
        c = open('configure.dist','r')
        cont = c.readlines()
        fileConfig = open(configFile,'w')
        for row in cont[11:]:
            fileConfig.write(str(row))
        c.close()
        fileConfig.close()
        Environment.__sendmail(msg=str(promogestDir))
    conf = Config(configFile)
    conf.save()

    # Parametri localizzazione formati
    conf.windowsrc = promogestDir + 'windowsrc.xml'
    conf.guiDir = '.' + os.sep + 'gui' + os.sep

    #Anno di lavoro
    workingYear = None

    #[Composer]
    if hasattr(conf,'Composer'):
        conf.emailcompose = str(getattr(conf.Composer, 'emailcompose'))
        try:
            conf.subject = conf.Composer.subject
        except:
            conf.subject = "[ Invio Doc: %s ]"
        conf.signature = """Invio elettronico di  %s   effettuato tramite software gestionale PromoGest """
        conf.body = conf.signature
    else:
        emailcompose = None

    #[Label]
    if hasattr(conf,'Label'):
        mod_enable = getattr(conf.Label,'mod_enable')
        if mod_enable:
            conf.hasLabel = True
            sistemaColonnaFrontaline = float(getattr(conf.Label, 'sistemacolonnafrontaline'))
            sistemaRigaFrontaline = float(getattr(conf.Label, 'sistemarigafrontaline'))
            #bordoDestro = float(getattr(conf.Label, 'bordodestro'))
            #bordoSinistro = float(getattr(conf.Label, 'bordosinistro'))
        else:
            conf.hasLabel = False
            sistemaColonnaFrontaline = 0
            sistemaRigaFrontaline = 0
            bordoDestro = None
            bordoSinistro = None
    else:
        conf.hasLabel = False
    importDebug = True
    return conf

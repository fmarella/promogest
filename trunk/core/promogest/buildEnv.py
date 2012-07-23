# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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


import os
import sys
import shutil
import glob
from config import Config
from promogest.EnvUtils import getConfigureDir
from promogest import Environment

#""" Sets configuration value """
def set_configuration(company=None, year = None, pg_path=None):
    #global conf,connection, exceptionHandler, promogestDir, feed,  emailcompose,\
                #emailmittente, smtpServer, \
                #multilinelimit, mltext,\
                #imagesDir, labelTemplatesDir, templatesDir, documentsDir, reportTemplatesDir,\
                #bordoDestro, bordoSinistro, magazzini, listini, tempDir, tracciatiDir

    if company:
        Environment.azienda = company
    dire = getConfigureDir(company)
    promogestDir = None
    if pg_path:
        promogestDir = os.path.join(pg_path, dire) + os.sep
    else:
        promogestDir = os.path.join(os.path.expanduser('~'), dire) + os.sep
    Environment.promogestDir = promogestDir
    if not (os.path.exists(promogestDir)):
        os.mkdir(promogestDir)

    documentsDir = promogestDir + 'documenti' + os.sep
    Environment.documentsDir = documentsDir
    if not (os.path.exists(documentsDir)):
        os.mkdir(documentsDir)

    tracciatiDir = promogestDir + 'tracciati' + os.sep
    Environment.tracciatiDir = tracciatiDir
    if not (os.path.exists(tracciatiDir)):
        os.mkdir(tracciatiDir)

    tempDir = promogestDir + 'temp' + os.sep
    Environment.tempDir = tempDir
    if not (os.path.exists(tempDir)):
        os.mkdir(tempDir)

    templatesDir = promogestDir + 'templates' + os.sep
    Environment.templatesDir = templatesDir
    if not (os.path.exists(templatesDir)):
        os.mkdir(templatesDir)
        slas = glob.glob(os.path.join('.', 'templates', '*.sla'))
        for s in slas:
            shutil.copy(s, templatesDir)

    reportTemplatesDir = promogestDir + 'report-templates' + os.sep
    Environment.reportTemplatesDir = reportTemplatesDir
    if not (os.path.exists(reportTemplatesDir)):
        os.mkdir(reportTemplatesDir)
        slas = glob.glob(os.path.join('.', 'report-templates', '*.sla'))
        for s in slas:
            shutil.copy(s, reportTemplatesDir)

    labelTemplatesDir = promogestDir + 'label-templates' + os.sep
    Environment.labelTemplatesDir = labelTemplatesDir
    if not (os.path.exists(labelTemplatesDir)):
        os.mkdir(labelTemplatesDir)
        slas = glob.glob(os.path.join('.', 'label-templates', '*.sla'))
        for s in slas:
            shutil.copy(s, labelTemplatesDir)

    imagesDir = promogestDir + 'images' + os.sep
    Environment.imagesDir = imagesDir
    if not (os.path.exists(imagesDir)):
        os.mkdir(imagesDir)
    try:
        configFile = promogestDir + 'configure'
        conf = Config(configFile)
    except IOError:
        #b= open(promogestStartDir+'configure')
        #db_cont = b.readlines()
        configFile = promogestDir + 'configure'
        c = open('configure.dist','r')
        cont = c.readlines()
        fileConfig = open(configFile,'w')
        #for row in db_cont[0:10]:
            #fileConfig.write(str(cont))
        for row in cont[11:]:
            fileConfig.write(str(row))
        #b.close()
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

    mltext = ""

    #[Pagamenti]
    if hasattr(conf, 'Pagamenti'):
        mod_enable = getattr(
                conf.Pagamenti,'mod_enable','no')
        if mod_enable == 'yes':
            conf.hasPagamenti = True
        else:
            conf.hasPagamenti = False
    else:
        conf.hasPagamenti = False

    #[Magazzini]
    magazzini = False
    if hasattr(conf, 'Magazzini'):
        mod_enable = getattr( conf.Magazzini,'mod_enable','no')
        if mod_enable == 'yes':
            magazzini = True


    #[Listini] necessario per il multilistini su sqlite
    listini = False
    if hasattr(conf, 'Listini'):
        mod_enable = getattr( conf.Listini,'mod_enable','no')
        if mod_enable == 'yes':
            listini = True


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

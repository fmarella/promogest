# -*- coding: utf-8 -*-

"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 license: GPL see LICENSE file
"""
import locale
from config import Config
import gtk
#import pickle
import os
import shutil
import glob
import getopt, sys
from sqlalchemy import *
from sqlalchemy.orm import *

from sqlalchemy.interfaces import ConnectionProxy
import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)

class TimerProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        now = time.time()
        try:
            return execute(cursor, statement, parameters, context)
        finally:
            total = time.time() - now
            if "UPDATE" in statement or "INSERT" in statement or "DELETE" in statement:
                #print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", statement
                logger.info("Query: %s" % statement)
                teeeeeees = logger.info("Query: %s" % statement)
                logger.info("Total Time: %f" % total)

debugDao = True
debugSQL = False
reportTemplatesDir = None
imagesDir = None
labelTemplatesDir = None
templatesDir = None
documentsDir = None
conf = None
promogestDir = None
exceptionHandler = None
connection = None
feed = None
emailcompose = None
loc = None
subject= None
body = None
rivenditoreUrl = None
smtpServer = None
emailmittente = None
cliente_predefinito = None
tipo_documento_predefinito = None
multilinelimit = None
mltext = None
sistemaColonnaFrontaline = None
sistemaRigaFrontaline = None
bordoDestro = None
bordoSinistro = None
feedCache = ""
feedAll = ""
scontisave = {}
tagliacoloretempdata = (False,None)
lastCode = None
righeDocumentoDict = {}
totaliDict = {}
percentualeIvaRiga = None
aliquotaIvaRiga = None

def getConfigureDir(company='__default__'):
    """ Tests if another configuration folder was indicated """
    default='promogest2'
    if company != '__default__' and company is not None:
        default = os.path.join('promogest2',company)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:", ["config-dir="])
        for opt, arg in opts:
            if opt in ("-c", "--config-dir"):
                return arg
        else:
            return default
    except getopt.GetoptError:
        return default

try:
    startDir = getConfigureDir()
    promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
    if not (os.path.exists(promogestStartDir)):
        os.mkdir(promogestStartDir)
    configFile = promogestStartDir + 'configure'
    conf = Config(configFile)
    conf.guiDir = '.' + os.sep + 'gui' + os.sep

except IOError:
    c = open('configure.dist','r')
    content = c.readlines()
    fileConfig = open(configFile,'w')
    for row in content[0:10]:
        fileConfig.write(row)
    c.close()
    fileConfig.close()
    conf = Config(configFile)
    conf.guiDir = '.' + os.sep + 'gui' + os.sep





""" Sets configuration value """
def set_configuration(company=None, year = None):

    global conf,connection, exceptionHandler, promogestDir, feed,  emailcompose,\
                emailmittente, smtpServer, cliente_predefinito, tipo_documento_predefinito,\
                multilinelimit, mltext, sistemaColonnaFrontaline, sistemaRigaFrontaline,\
                imagesDir, labelTemplatesDir, templatesDir, documentsDir, reportTemplatesDir,\
                bordoDestro, bordoSinistro
            
    try:
        dir = getConfigureDir(company)
        promogestDir = os.path.expanduser('~') + os.sep + dir + os.sep
        if not (os.path.exists(promogestDir)):
            os.mkdir(promogestDir)

        try:
            documentsDir = promogestDir + 'documenti' + os.sep
            if not (os.path.exists(documentsDir)):
                os.mkdir(documentsDir)

            tempDir = promogestDir + 'temp' + os.sep
            if not (os.path.exists(tempDir)):
                os.mkdir(tempDir)

            templatesDir = promogestDir + 'templates' + os.sep
            if not (os.path.exists(templatesDir)):
                os.mkdir(templatesDir)
                slas = glob.glob(os.path.join('.', 'templates', '*.sla'))
                for s in slas:
                    shutil.copy(s, templatesDir)

            reportTemplatesDir = promogestDir + 'report-templates' + os.sep
            if not (os.path.exists(reportTemplatesDir)):
                os.mkdir(reportTemplatesDir)
                slas = glob.glob(os.path.join('.', 'report-templates', '*.sla'))
                for s in slas:
                    shutil.copy(s, reportTemplatesDir)

            labelTemplatesDir = promogestDir + 'label-templates' + os.sep
            if not (os.path.exists(labelTemplatesDir)):
                os.mkdir(labelTemplatesDir)
                slas = glob.glob(os.path.join('.', 'label-templates', '*.sla'))
                for s in slas:
                    shutil.copy(s, labelTemplatesDir)

            imagesDir = promogestDir + 'images' + os.sep
            if not (os.path.exists(imagesDir)):
                os.mkdir(imagesDir)
        except:
            print "Qualcosa e' fallito nell'env"
            raise

        configFile = promogestDir + 'configure'
        conf = Config(configFile)
    except IOError:
        msg = ('Il file configure non e\' stato trovato !\n\n' +
               'Il file verra creato in questo momento con valori di default\n' +
               'e una connessione al database demo di Promotux.\n\n' +
               'Ti invitiamo a riconfigurare il setup secondo le tue esigenze.')
        overDialog = gtk.MessageDialog(None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO,
                                       gtk.BUTTONS_OK, msg)
        response = overDialog.run()
        if response == gtk.RESPONSE_OK:
            b= open(promogestStartDir+'configure')
            db_cont = b.readlines()

            c = open('configure.dist','r')
            cont = c.readlines()
            fileConfig = open(configFile,'w')
            for row in db_cont[0:10]:
                fileConfig.write(str(cont))
            for row in cont[11:]:
                fileConfig.write(str(row))
            b.close()
            c.close()
            fileConfig.close()
            conf = Config(configFile)
        overDialog.destroy()

    # Impostazioni di default
        conf.Documenti.cartella_predefinita = documentsDir
        conf.Documenti.ricerca_per = 'descrizione'
        conf.save()


    # Imposto variabili di formattazione numeri
    conf.number_format = '%-14.' + str(getattr(conf.Numbers, 'decimals', 4)) + 'f'
    conf.decimals = str(getattr(conf.Numbers, 'decimals', 4))
    conf.batch_size = int(getattr(conf.Numbers, "batch_size",15))


    # Parametri localizzazione formati
    loc = locale.setlocale(locale.LC_ALL, '')
    conf.windowsrc = promogestDir + 'windowsrc.xml'
    conf.guiDir = '.' + os.sep + 'gui' + os.sep

    #Anno di lavoro
    conf.workingYear = None
    workingYear = None
    # stampa il debug del Dao
    debugDao = True


    # Promowear
    #if hasattr(conf,'PromoWear'):
        #mod_enable = getattr(
            #conf.PromoWear,'mod_enable','yes')
        #taglie_enable = getattr(
        #conf.PromoWear,'taglie_colori','yes')
        #if mod_enable == 'yes':
            #conf.PromoWear = True
        #else:
            #conf.PromoWear = False
        #if taglie_enable == 'yes':
            #conf.taglia_colore = True
            ###try:
                ###from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori, SelezioneTaglieColori
            ###except ImportError:
                ###print "Errore import di GestioneTaglieColori in Environment.py"
                ###pass
        #else:
            #conf.taglia_colore = False
    #else:
        #conf.PromoWear = False


    #[Feed]
    try:
        feed = str(getattr(conf.Feed, 'feed'))
    except:
        feed = True


    #[Composer]
    if hasattr(conf,'Composer'):
        conf.emailcompose = str(getattr(conf.Composer, 'emailcompose'))
        conf.subject = "[ Invio Doc: %s ]"
        conf.body = ",body="+"""Invio elettronico di  %s   effettuato tramite software gestionale PromoGest """
    else:
        emailcompose = None

    #[Rivenditore]
    if hasattr(conf,'Rivenditore'):
        rivenditoreUrl = str(getattr(conf.Composer, 'rivenditoreurl'))
    else:
        rivenditoreUrl = "http://promogest.promotux.it/contatti.php"

    if hasattr(conf,'Numbers'):
        conf.combo_columns = int(getattr(conf.Numbers,'combo_column',5))
    else:
        print "ATTENZIONE: OPZIONE combo_column = 5  MANCANTE NEL CONFIGURE SEZIONE [Numbers]"
        conf.combo_columns = 3
    #[SMTP]
    smtpServer = str(getattr(conf.SMTP, 'smtpserver'))
    emailmittente = str(getattr(conf.SMTP, 'emailmittente'))

    #[Documenti]
    cliente_predefinito = str(getattr(conf.Documenti, 'cliente_predefinito'))
    tipo_documento_predefinito = str(getattr(conf.Documenti, 'tipo_documento_predefinito'))


    #[Multilinea]
    try :
        multilinelimit = int(getattr(conf.Multilinea, 'multilinealimite'))
    except:
        multilinelimit = 60
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

mainSchema = "promogest2"

#try :
azienda=conf.Database.azienda
#except:
    #azienda = "azienda_prova"
database = conf.Database.database
port = conf.Database.port
user = conf.Database.user
password = conf.Database.password
host = conf.Database.host
userdata = ["","","",user]


engine = create_engine('postgres:'+'//'+conf.Database.user+':'
                    + conf.Database.password+ '@'
                    + conf.Database.host + ':'
                    + conf.Database.port + '/'
                    + conf.Database.database,
                    encoding='utf-8',
                    convert_unicode=True )

engine.echo = debugSQL
meta = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
params = {'db_pg': engine ,
        'mainSchema': mainSchema,
        'schema': azienda,
        'metadata': meta,
        'session' : session,
        'rowsFamily' : [],
        'defaultLimit': 5,
        'widthThumbnail' : 64,
        'heightThumbnail' : 64,
        'widthdetail' : 110,
        'heightdetail': 110 ,
        'usernameLoggedList':userdata}


 # Parametri localizzazione formati
loc = locale.setlocale(locale.LC_ALL, '')
conf.windowsrc = os.path.expanduser('~') + os.sep + 'promogest/windowsrc.xml'
conf.guiDir = '.' + os.sep + 'gui' + os.sep
#conf.windowsrc = promogestDir + 'windowsrc.xml'
#conf.guiDir = '.' + os.sep + 'gui' + os.sep

# -*- coding: utf-8 -*-

"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 license: GPL see LICENSE file
"""
import locale
from config import Config
import gtk
import os
import shutil
import glob
import getopt, sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
import logging
import logging.handlers


PRODOTTO = "PromoTux - Virtual Company"
VERSIONE = "PromoGest2"
debugFilter = False
debugDao = False
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
modulesList = []
listinoFissato = None
new_print_enjine=True
shop = False
rev_locale = None
rev_remota = None
magazzino_pos = None
view = "month"
mm = {'3996679c06ebc369feefc92063644d83':'e4da3b7fbbce2345d7772b0674a318d5', #Contatto = 5
        'cfe6753e5e82f522119e09df7b726e4a':'eccbc87e4b5ce2fe28308fd9f2a7baf3'} #Promemoria = 3


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

def startdir():
    startDir = getConfigureDir()
    promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
    return promogestStartDir


try:

    promogestStartDir = startdir()
    if not (os.path.exists(promogestStartDir)):
        os.mkdir(promogestStartDir)
    configFile = promogestStartDir + 'configure'
    conf = Config(configFile)
    conf.guiDir = '.' + os.sep + 'gui' + os.sep

except IOError:
    c = open('configure.dist','r')
    content = c.readlines()
    fileConfig = open(configFile,'w')
    for row in content[0:13]:
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
                bordoDestro, bordoSinistro, magazzini, listini

    try:
        dire = getConfigureDir(company)
        promogestDir = os.path.expanduser('~') + os.sep + dire + os.sep
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


    # Parametri localizzazione formati
    loc = locale.setlocale(locale.LC_ALL, '')
    conf.windowsrc = promogestDir + 'windowsrc.xml'
    conf.guiDir = '.' + os.sep + 'gui' + os.sep

    #Anno di lavoro
    conf.workingYear = None
    workingYear = None
    # stampa il debug del Dao


    #[Composer]
    if hasattr(conf,'Composer'):
        conf.emailcompose = str(getattr(conf.Composer, 'emailcompose'))
        try:
            conf.subject = conf.Composer.subject
        except:
            conf.subject = "[ Invio Doc: %s ]"
        try:
            conf.signature = conf.Composer.signature
        except:
            conf.signature = """Invio elettronico di  %s   effettuato tramite software gestionale PromoGest """
        try :
            conf.bodytemplate = conf.Composer.bodytemplate
        except:
            conf.bodytemplate = ""
        conf.body = conf.bodytemplate + conf.signature
    else:
        emailcompose = None

    #[Rivenditore]
    if hasattr(conf,'Rivenditore'):
        rivenditoreUrl = str(getattr(conf.Composer, 'rivenditoreurl'))
    else:
        rivenditoreUrl = "http://promogest.promotux.it/contatti.php"

    #[Documenti]
    cliente_predefinito = str(getattr(conf.Documenti, 'cliente_predefinito'))
    tipo_documento_predefinito = str(getattr(conf.Documenti, 'tipo_documento_predefinito'))

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


    #[Listini]
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

azienda=conf.Database.azienda

try:
    tipodb = conf.Database.tipodb
except:
    tipodb = "postgresql"
try:
    pw = conf.Database.pw
except:
    pw = "No"
if tipodb == "sqlite" and not (os.path.exists(startdir()+"db")):
    if os.path.exists("data/db"):
        shutil.copy("data/db",startdir()+"db")
        os.remove("data/db")
    elif os.path.exists("data/db_pw.dist")\
                        and pw.upper()=="YES":
        shutil.copy("data/db_pw.dist",startdir()+"db" )
    elif os.path.exists("data/db.dist"):
        shutil.copy("data/db.dist",startdir()+"db" )
    else:
        print("ERRORE NON RIESCO A CREARE IL DB")

database = conf.Database.database
port = conf.Database.port
user = conf.Database.user
password = conf.Database.password
host = conf.Database.host
userdata = ["","","",user]



class SetTextFactory(PoolListener):
     def connect(self, dbapi_con, con_record):
         dbapi_con.text_factory = str


if tipodb == "sqlite":
    azienda = None
    mainSchema = None
    print "startdir()", startdir()
    engine =create_engine("sqlite:///"+startdir()+"db",listeners=[SetTextFactory()])
else:
    mainSchema = "promogest2"
    #azienda=conf.Database.azienda
    try:
        engine = create_engine('postgresql+pg8000:'+'//'
                    +user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',
                    convert_unicode=True )
        print "PG8000"
    except:
        engine = create_engine('postgres:'+'//'
                        +user+':'
                        + password+ '@'
                        + host + ':'
                        + port + '/'
                        + database,
                        encoding='utf-8',
                        convert_unicode=True )
        print "PSYCOPG2"
tipo_eng = engine.name
engine.echo = False
meta = MetaData(engine)
#Session = sessionmaker(bind=engine)
Session = scoped_session(sessionmaker(bind=engine, autoflush=True))

#meta = None
#Session = scoped_session(sessionmaker(bind=engine))
session = Session()
params = {'engine': engine ,
        'mainSchema': mainSchema,
        'schema': azienda,
        'metadata': meta,
        'session' : session,
        "tipo_db":tipodb,
        'rowsFamily' : [],
        'defaultLimit': 5,
        'widthThumbnail' : 64,
        'heightThumbnail' : 64,
        'widthdetail' : 110,
        'heightdetail': 110 ,
        'usernameLoggedList':userdata}


 # Parametri localizzazione formati
loc = locale.setlocale(locale.LC_ALL, '')
conf.windowsrc = os.path.expanduser('~') + os.sep + 'promogest2/windowsrc.xml'
conf.guiDir = '.' + os.sep + 'gui' + os.sep
#conf.windowsrc = promogestDir + 'windowsrc.xml'
#conf.guiDir = '.' + os.sep + 'gui' + os.sep

LOG_FILENAME = startdir()+'pg2.log'

# Set up a specific logger with our desired output level
pg2log = logging.getLogger('PromoGest2')
pg2log.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=400000, backupCount=3)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(funcName)s - %(lineno)d")
# add formatter to ch
handler.setFormatter(formatter)
pg2log.addHandler(handler)
pg2log.debug("\n\n<<<<<<<<<<<  AVVIO PROMOGEST >>>>>>>>>>")


def hook(et, ev, eb):
    import traceback
    pg2log.debug("\n  ".join (["Error occurred: traceback follows"]+list(traceback.format_exception(et, ev, eb))))
    print "UN ERRORE È STATO INTERCETTATO E LOGGATO, SI CONSIGLIA DI RIAVVIARE E DI CONTATTARE L'ASSISTENZA \n\nPREMERE CTRL+C PER CHIUDERE"
sys.excepthook = hook

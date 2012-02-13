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


from promogest import pg3_check
pg3 = pg3_check.pg3_cla
aziendaforce = pg3_check.aziendaforce
tipodbforce = pg3_check.tipodbforce
hostdbforce = pg3_check.hostdbforce
web = pg3_check.web

from config import Config
if not web:
    if pg3:
        from gi.repository import Gtk as gtk
        GTK_DIALOG_MODAL = gtk.DialogFlags.MODAL
        GTK_DIALOG_DESTROY_WITH_PARENT = gtk.DialogFlags.DESTROY_WITH_PARENT
        GTK_BUTTON_OK = gtk.ButtonsType.OK
        GTK_DIALOG_MESSAGE_INFO = gtk.MessageType.INFO
        GTK_RESPONSE_OK = gtk.ResponseType.OK
        settings = gtk.Settings.get_default()
        gtk.Settings.set_long_property(settings, "gtk-button-images", 1, "main")
    else:
        import gtk
        GTK_DIALOG_MODAL = gtk.DIALOG_MODAL
        GTK_DIALOG_DESTROY_WITH_PARENT = gtk.DIALOG_DESTROY_WITH_PARENT
        GTK_BUTTON_OK = gtk.BUTTONS_OK
        GTK_DIALOG_MESSAGE_INFO = gtk.MESSAGE_INFO
        GTK_RESPONSE_OK = gtk.RESPONSE_OK
        settings = gtk.settings_get_default()
        gtk.Settings.set_long_property(settings, "gtk-button-images", 1, "main")

import os
import sys
import shutil
import glob
import getopt
try:
    from werkzeug import Local, LocalManager #, cached_property
except:
    pass

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.interfaces import ConnectionProxy
from sqlalchemy.exc import *
import logging
import logging.handlers
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime

PRODOTTO = "PromoTux"
VERSIONE = "PromoGest 2.9.0"
if pg3:
    VERSIONE = "PromoGest 2.9.90"
debugFilter = False
debugDao = False
debugSQL = False
reportTemplatesDir = None
imagesDir = None
labelTemplatesDir = None
templatesDir = None
documentsDir = None
tracciatiDir = None
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
bordoDestro = None
bordoSinistro = None
feedCache = ""
feedAll = ""
scontisave = {}
tagliacoloretempdata = (False,None)
lastCode = None
modules_folders = []
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
windowGroup = []
view = "month"
puntoA = None
puntoB = None
puntoP = None
eta = 0
tipo_pg = None
workingYear = 2011
cartella_moduli = 'promogest/modules'
totale_pn_con_riporto = 0
aaa = 648
da_data_inizio_primanota = None
a_data_inizio_primanota = None
azienda_in_conf = None


CONFIGPATH = os.path.split(os.path.dirname(__file__))[0]
webconfigFile = os.path.join(CONFIGPATH, 'pgweb.conf')
webconf = Config(webconfigFile)
if hasattr(webconf,"SottoDominio"):
    if os.path.exists(CONFIGPATH+'/templates/'+webconf.SottoDominio.schema):
        SUB = webconf.SottoDominio.schema
    else:
        SUB = ""
else:
    SUB = ""
cadenza = ["MENSILE", "BIMESTRALE", "TRIMESTRALE", "SEMESTRALE", "ANNUALE"]
ALLOWED_SCHEMES = frozenset(['http', 'https', 'ftp', 'ftps'])
templates_dir= os.path.join(CONFIGPATH, 'templates')
STATIC_PATH = templates_dir
STATIC_PATH_FEED = os.path.join(CONFIGPATH, 'feed')
IMAGEPATH = os.path.join(STATIC_PATH, 'images/')
LANGPATH = os.path.join(CONFIGPATH, 'lang')
session_dir = os.path.join(CONFIGPATH, 'session')
modules_dir = os.path.join(CONFIGPATH, 'core/plugins')
domains = os.path.join(CONFIGPATH, 'templates')
CACHE = os.path.join(CONFIGPATH, 'cache')
URL_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'
modulesList = ["Contatti"]
sladir = "sladir/"
artImagPath = ""
importDebug = False
languages = ""
COOKIENAME = "promogest_web"
hapag = ["Fattura accompagnatoria","Fattura acquisto","Fattura differita acquisto",
"Fattura differita vendita","Fattura vendita","Ricevuta Fiscale","Vendita dettaglio",
"Nota di credito a cliente","Nota di credito da fornitore"]

try:
    local = Local()
    local_manager = LocalManager([local])
    application = local('application')
    feedTrac = None
    feedPromo = None
    orario = 0
except:
    pass

fromHtmlLits = ["Promemoria", "TestataPrimaNota","Articolo", "Cliente",
                "Contatto", "Fornitore", "Fornitura", "Contatto", "Vettore",
                "AliquotaIva", "TestataCommessa","Stoccaggio"]

package = ["ONE BASIC", "ONE FULL", "ONE STANDARD", "PRO BASIC", "PRO STANDARD",
            "PRO FULL","ONE PROMOWEAR", "ONE PROMOSHOP", "PRO PROMOWEAR", "PRO PROMOSHOP"]


mm = {'3996679c06ebc369feefc92063644d83':'e4da3b7fbbce2345d7772b0674a318d5', #Contatto = 5
        'cfe6753e5e82f522119e09df7b726e4a':'eccbc87e4b5ce2fe28308fd9f2a7baf3'} #Promemoria = 3

confList=[]

configDir= None

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


def messageInfoEnv(msg="Messaggio generico", transient=None):
    """generic msg dialog """
    if not web:
        dialoggg = gtk.MessageDialog(transient,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        GTK_DIALOG_MESSAGE_INFO,
                        GTK_BUTTON_OK,
                        msg)
        try:
            pg2log.info(msg)
        except:
            pass
        dialoggg.run()
        dialoggg.destroy()

class MyProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        try:
            return execute(cursor, statement, parameters, context)
        except OperationalError as e:
            messageInfoEnv(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+e.message)
        except IntegrityError as e:
            messageInfoEnv(msg="IntegrityError UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+e.message)
            session.rollback()
        except ProgrammingError as e:
            messageInfoEnv(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+e.message)
            session.rollback()
        except InvalidRequestError as e:
            messageInfoEnv(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+e.message)
            session.rollback()
        except AssertionError as e:
            messageInfoEnv(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO\n Possibile tentativo di cancellazione di un dato\n collegato ad altri dati fondamentali: "+e.message)
            session.rollback()
        except ValueError as e:
            messageInfoEnv(msg="Risulta inserito un Valore non corretto. Ricontrolla: "+e.message)
            session.rollback()


def _pg8000():
    try:
        engine = create_engine('postgresql+pg8000:'+'//'
                    +user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',pool_size=30,
                    convert_unicode=True,proxy=MyProxy() )
        return engine
    except:
        return None

def _py_postgresql():
    try:
        engine = create_engine('postgresql+pypostgresql:'+'//'
                    +user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',pool_size=30,
                    convert_unicode=True,proxy=MyProxy())
        return engine
    except:
        return None

def connect():
    import psycopg2
    a=None
    try:
        a = psycopg2.connect(user=user, host=host, port=port,
                            password=password, database=database)
    except Exception, e:
        a = "CONNESSIONE AL DATABASE PRO NON RIUSCITA.\n DETTAGLIO ERRORE: [%s]" % str(e)
        messageInfoEnv(msg=a)
        sys.exit()
    if a:
        return a

def _psycopg2new():
    try:
        engine = create_engine('postgresql://', creator=connect,
                convert_unicode=True,
                encoding='utf-8',
                proxy=MyProxy())
#        engine = create_engine('postgresql:'+'//'
#                    +user+':'
#                    + password+ '@'
#                    + host + ':'
#                    + port + '/'
#                    + database,
#                    encoding='utf-8',pool_size=30,
#                    convert_unicode=True,proxy=MyProxy() )
        return engine
    except:
        return None

def _psycopg2old():
    try:
        engine = create_engine('postgres:'+'//'
                    +user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',pool_size=30,
                    convert_unicode=True,proxy=MyProxy())
        return engine
    except:
        return None

if not web:
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
                emailmittente, smtpServer, \
                multilinelimit, mltext,\
                imagesDir, labelTemplatesDir, templatesDir, documentsDir, reportTemplatesDir,\
                bordoDestro, bordoSinistro, magazzini, listini, tempDir, tracciatiDir

    try:
        dire = getConfigureDir(company)
        promogestDir = os.path.expanduser('~') + os.sep + dire + os.sep
        if not (os.path.exists(promogestDir)):
            os.mkdir(promogestDir)
        try:
            documentsDir = promogestDir + 'documenti' + os.sep
            if not (os.path.exists(documentsDir)):
                os.mkdir(documentsDir)

            tracciatiDir = promogestDir + 'tracciati' + os.sep
            if not (os.path.exists(tracciatiDir)):
                os.mkdir(tracciatiDir)

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
        msg = """Questa è la prima volta che viene lanciato il PromoGest.
Il file di configurazione per questa installazione non è ancora presente!
Ne verrà creato uno con i valori di base e poi il programma partirà
La cartella di lavoro sarà: %s
Grazie per aver scelto il PromoGest""" %str(promogestDir)

        overDialog = gtk.MessageDialog(None,
                                       GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                       GTK_DIALOG_MESSAGE_INFO,
                                       GTK_BUTTON_OK, msg)
        response = overDialog.run()
        if response == GTK_RESPONSE_OK:
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
        sendmail(msg=str(promogestDir))
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
#        try:
#            conf.signature = conf.Composer.signature
#        except:
        conf.signature = """Invio elettronico di  %s   effettuato tramite software gestionale PromoGest """
#        try :
#            conf.bodytemplate = conf.Composer.bodytemplate
#        except:
#            conf.bodytemplate = ""
        conf.body = conf.signature
    else:
        emailcompose = None

    #[Rivenditore]
    if hasattr(conf,'Rivenditore'):
        rivenditoreUrl = str(getattr(conf.Composer, 'rivenditoreurl'))
    else:
        rivenditoreUrl = "http://promogest.promotux.it/contatti.php"

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

if web:
    conf = webconf

if aziendaforce:
    azienda = aziendaforce
else:
    azienda = conf.Database.azienda

if tipodbforce:
    tipodb = tipodbforce

else:
    try:
        tipodb = conf.Database.tipodb
    except:
        tipodb = "postgresql"

if hostdbforce:
    host = hostdbforce
else:
    try:
        host = conf.Database.host
    except:
        host = "localhost"



try:
    pw = conf.Database.pw
except:
    pw = "No"
if tipodb == "sqlite" and not (os.path.exists(startdir()+"db")) and not tipodbforce:
    if os.path.exists("data/db"):
        shutil.copy("data/db",startdir()+"db")
        os.remove("data/db")
    elif os.path.exists("data/db.dist"):
        shutil.copy("data/db.dist",startdir()+"db" )
    else:
        print("ERRORE NON RIESCO A CREARE IL DB")

database = conf.Database.database
port = conf.Database.port
user = conf.Database.user
password = conf.Database.password

userdata = ["","","",user]

class SetTextFactory(PoolListener):
     def connect(self, dbapi_con, con_record):
         dbapi_con.text_factory = str

def my_on_connect(dbapi_con, con_record):
    dbapi_con.text_factory = str

if tipodb == "sqlite":
    azienda = None
    mainSchema = None
    if sqlalchemy.__version__ >= "0.7":
        from sqlalchemy.event import listen
        if hostdbforce and tipodbforce:
            engine =create_engine("sqlite:///"+hostdbforce+"/db",encoding='utf-8',proxy=MyProxy())
        else:
            engine =create_engine("sqlite:///"+startdir()+"db",encoding='utf-8',proxy=MyProxy())
        listen(engine, 'connect', my_on_connect)
    else:
        engine =create_engine("sqlite:///"+startdir()+"db",listeners=[SetTextFactory()],proxy=MyProxy())
else:
    mainSchema = "promogest2"
    engine = _pg8000()
    if not engine:
        engine = _py_postgresql()
    if not engine:
        engine = _psycopg2new()
    if not engine:
        engine = _psycopg2old()
if not engine:
    raise RuntimeError("Non è stato trovato un backend per il database.")
tipo_eng = engine.name
engine.echo = False
#engine.autocommit= True
#insp = reflection.Inspector.from_engine(engine)

#Session = sessionmaker(bind=engine)
#Session = scoped_session(sessionmaker(bind=engine, autoflush=True))
#Session = scoped_session(sessionmaker(bind=engine))
if web:
    print "SESSIONE DI TIPO SCOPED PER IL WEB"
    Session = scoped_session(lambda: create_session(engine, autocommit=False))
else:
    Session = sessionmaker(bind=engine)

schema_azienda = azienda
meta = MetaData(engine)
session = Session()
#meta = None
schema_azienda = azienda

params = {'engine': engine ,
        'mainSchema': mainSchema,
        'schema': azienda,
        'metadata': meta,
        'session' : session,
        "tipo_db":tipodb,
        'rowsFamily' : [],
        'defaultLimit': 5,
        'bccaddr' : ["assistenza@promotux.it"],
        'objects' : ["Informazioni Tecniche", "Informazioni Commerciali" , "Varie"],
        'widthThumbnail' : 64,
        'heightThumbnail' : 64,
        'widthdetail' : 110,
        'heightdetail': 110 ,
        'usernameLoggedList':userdata}



 # Parametri localizzazione formati
conf.windowsrc = os.path.expanduser('~') + os.sep + 'promogest2/windowsrc.xml'
conf.guiDir = '.' + os.sep + 'gui' + os.sep

if not web:
    LOG_FILENAME = startdir() + 'pg2.log'

    # Set up a specific logger with our desired output level
    pg2log = logging.getLogger('PromoGest2')
    pg2log.setLevel(logging.INFO)

    # Add the log message handler to the logger
    try:
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=10000, backupCount=6)
    except:
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME+"bis", maxBytes=10000, backupCount=6)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(funcName)s - %(lineno)d")
    # add formatter to ch
    handler.setFormatter(formatter)
    pg2log.addHandler(handler)
    pg2log.info("\n\n<<<<<<<<<<<  AVVIO PROMOGEST >>>>>>>>>>")
else:
    pg2log = logging.getLogger('PromoGest2')
    #pg2log=None


def sendmail(msg="PG"):
    msg = str(promogestDir) +"  "+str(rev_locale) +"  "+str(rev_remota)
    return _msgDef(text=msg)

def _msgDef(text="", html="",img="", subject=""):
    msgg = MIMEMultipart()
    msgg['Subject'] = azienda+"  "+str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))
    msgg['From'] = "promogestlogs@gmail.com"
    msgg['To'] = "promogestlogs@gmail.com"
    msgg.attach(MIMEText(text))
#        fp = open(self.stname, 'rb')
#    part = MIMEBase('application','octet-stream')
    part = MIMEText('text/plain')
    fp =open(LOG_FILENAME, 'rb')
    part.set_payload(fp.read())
    fp.close()
#    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment', filename="pg2.log")
    msgg.attach(part)

    _send(fromaddr="promogestlogs@gmail.com", total_addrs="promogestlogs@gmail.com", msg=msgg)

def _send(fromaddr=None, total_addrs=None, msg=None):
    try:
        server = smtplib.SMTP("smtp.gmail.com")
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("promogestlogs@gmail.com", "pr0m0t0x")
        return server.sendmail("promogestlogs@gmail.com", "promogestlogs@gmail.com" , msg.as_string())
    except Exception as e:
        print "ERRORE NELLA SPEDIZIONE EMAIL", e.message

def hook(et, ev, eb):
    import traceback
    if "Operation aborted" in str(ev):
        return
    if "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????" in ev:
        return
    if "[Errno 9] Bad file descriptor" in ev:
        return
    if "Handler" in str(ev):
        print "ATTENZIONE!!! MANCA L'HANDLER", ev
        return
    pg2log.info("\n  ".join (["Error occurred: traceback follows"]+list(traceback.format_exception(et, ev, eb))))
    print "UN ERRORE È STATO INTERCETTATO E LOGGATO, SI CONSIGLIA DI RIAVVIARE E DI CONTATTARE L'ASSISTENZA \n\nPREMERE CTRL+C PER CHIUDERE  \n"+"\n  ".join(list(traceback.format_exception(et, ev, eb)))
    sendmail()
sys.excepthook = hook

# DA SPOSTARE ASSOLUTAMENTE QUANTO PRIMA

# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2014 by Promotux
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


from promogest import preEnv
# leggiamo da preEnv che è anche un file di configurazioni pre-environment

# XXX: Su piattaforma Windows, forziamo PyGI se disponibile
#try:
    #import gi
    #pygi_available = True
#except ImportError:
    #pygi_available = False

pg3 = preEnv.pg3_cla
# bypassiamo il paramentro iniziale o passato da linea di comando se siamo su win32
import os
#if os.name == 'nt' and pygi_available:
    #pg3 = True
    #preEnv.pg3_cla = True

aziendaforce = preEnv.aziendaforce
tipodbforce = preEnv.tipodbforce
hostdbforce = preEnv.hostdbforce
dbforce = preEnv.dbforce
web = preEnv.web
echosa = preEnv.echo
debugFilter = preEnv.debugFilter
debugDao = preEnv.debugDao
shop = preEnv.shop
sublo = preEnv.sublo

if web:
    main_conf = preEnv.main_conf_force
    preEnv.conf = main_conf

from promogest.lib.config import Config
if not web:
    print " USIAMO LA VERSIONE CON PYGI"
    from gi.repository import Gtk as gtk
    GTK_DIALOG_MODAL = gtk.DialogFlags.MODAL
    GTK_DIALOG_DESTROY_WITH_PARENT = gtk.DialogFlags.DESTROY_WITH_PARENT
    GTK_BUTTON_OK = gtk.ButtonsType.OK
    GTK_RESPONSE_CANCEL = gtk.ResponseType.CANCEL
    GTK_DIALOG_MESSAGE_INFO = gtk.MessageType.INFO
    GTK_DIALOG_MESSAGE_ERROR = gtk.MessageType.ERROR
    GTK_RESPONSE_OK = gtk.ResponseType.OK
    settings = gtk.Settings.get_default()
    gtk.Settings.set_long_property(settings, "gtk-button-images", 1, "main")

import os
import sys
import shutil
import decimal
try:
    import psycopg2
    psycopg2.extensions.register_adapter(decimal.Decimal,
                                                psycopg2._psycopg.Decimal)
except:
    pass
import sqlalchemy
if "0.7.4" > sqlalchemy.__version__:
    dialoggg = gtk.MessageDialog(None,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        GTK_DIALOG_MESSAGE_ERROR,
                        GTK_RESPONSE_CANCEL)
    dialoggg.set_markup("E' necessaria una versione di sqlalchemy superiore alla 0.7.3, tu hai la "+str(sqlalchemy.__version__))
    response = dialoggg.run()
    dialoggg.destroy()
    sys.exit()

try:
    import jinja2
    if preEnv.pg3_cla:
            from gi.repository.WebKit import WebView
            from gi.repository.WebKit import WebSettings
    else:
        from webkit import WebView
        from webkit import WebSettings
    import reportlab
except Exception as e:
    if not preEnv.web:
        dialoggg = gtk.MessageDialog(None,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        GTK_DIALOG_MESSAGE_ERROR,
                        GTK_RESPONSE_CANCEL)
        msg = """ Manca la libreria python indicata qui in basso,
Su linux installarla singolarmente usando il software manager o yum o apt-get
Su windows provare a disinstallare e reinstallare il PromoGest
disattivando l'antivirus per qualche minuto

{0}""".format(str(e))
        dialoggg.set_markup(msg)
        response = dialoggg.run()
        dialoggg.destroy()
        sys.exit()
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.interfaces import PoolListener
from sqlalchemy.exc import *
#from sqlalchemy.ext.declarative import DeferredReflection
from promogest.lib.alembic.migration import MigrationContext
from promogest.lib.alembic.operations import Operations
from promogest.lib.alembic import op
from promogest.EnvUtils import *

PRODOTTO = "PromoTux"
VERSIONE = "PromoGest 2.9.2"
if pg3:
    VERSIONE = "PromoGest 2.9.92"
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
subject = None
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
idACT = []
scontisave = {}
tagliacoloretempdata = (False, None)
lastCode = None
modules_folders = []
righeDocumentoDict = {}
totaliDict = {}
percentualeIvaRiga = None
aliquotaIvaRiga = None
listinoFissato = None
new_print_enjine = True
rev_locale = None
rev_remota = None
magazzino_pos = None
windowGroup = []
view = "month"
news = []
req = None
puntoA = None
puntoB = None
puntoP = None
eta = 0
tipo_pg = None
workingYear = 2014
cartella_moduli = 'promogest/modules'
totale_pn_con_riporto = 0
aaa = 648
da_data_inizio_primanota = None
a_data_inizio_primanota = None
azienda_in_conf = None
idACT = []
confDict = {}
famiglie_articolo = []
categorie_articolo = []
stati_articolo = []
cache_obj = None
avvii = 1
generic_counter= 0
SRC_PATH = os.path.split(os.path.dirname(__file__))[0]
guiDir = '.' + os.sep + 'gui' + os.sep
subloguiDir = '.' + os.sep + 'gui_sublo' + os.sep
schemi_presenti = []
confList = []
configDir = None

modulesList = []

sladir = "sladir/"
artImagPath = ""
languages = ""

def putMainconf():
    if not preEnv.web:
        #controlliamo che ci sia la cartella promogest2
        promogestStartDir = startdir()
        if not (os.path.exists(promogestStartDir)):
            os.mkdir(promogestStartDir)
        configFile = promogestStartDir + 'main_conf.cf'
        if not os.path.exists(promogestStartDir + "main_conf.cf"):
            if os.path.exists(promogestStartDir + "configure"):
                shutil.copy(promogestStartDir + "configure", configFile)
            else:
                c = open('configure.dist', 'r')
                content = c.readlines()
                fileConfig = open(configFile, 'w')
                for row in content[0:13]:
                    fileConfig.write(row)
                c.close()
                fileConfig.close()
        main_conf = Config(configFile)
        return main_conf


if preEnv.conf is None:
    main_conf = putMainconf()
else:
    main_conf = preEnv.conf

windowsrc = startdir() + 'windowsrc.xml'


if preEnv.aziendaforce:
    azienda = preEnv.aziendaforce
else:
    try:
        azienda = main_conf.Database.azienda
    except:
        azienda = None

if preEnv.tipodbforce:
    tipodb = preEnv.tipodbforce
else:
    tipodb = main_conf.Database.tipodb

if preEnv.hostdbforce:
    host = preEnv.hostdbforce
else:
    host = main_conf.Database.host

try:
    nobrand = bool(main_conf.Database.nobrand)
except:
    nobrand = False
try:
    partner = main_conf.Database.partner
except:
    partner = "070 8649705 -- www.promogest.me -- assistenza@promotux.it"

if tipodb == "sqlite" and not (os.path.exists(startdir() + "db")) and not tipodbforce and not preEnv.web:
    if os.path.exists("data/db"):
        shutil.copy("data/db", startdir() + "db")
        os.remove("data/db")
    elif os.path.exists("data/db.dist"):
        shutil.copy("data/db.dist", startdir() + "db")
    else:
        print("ERRORE NON RIESCO A CREARE IL DB")


if preEnv.dbforce:
    database = preEnv.dbforce
else:
    database = main_conf.Database.database

if preEnv.portforce:
    port = preEnv.portforce
else:
    port = main_conf.Database.port

if preEnv.userforce:
    user = preEnv.userforce
else:
    user = main_conf.Database.user

if preEnv.pwdforce:
    password = preEnv.pwdforce
else:
    password = main_conf.Database.password

preEnv.port = port
preEnv.user = user
preEnv.password = password
preEnv.database = database
preEnv.host = host
preEnv.tipodb = tipodb
SUB = ""
userdata = ["", "", "", user]

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    print " STO RIAVVIANDO IL PROGRAMMA CON QUESTO ESEGUIBILE PYTHON", python
    os.execl(python, python, * sys.argv)
print " AZIENDAAAA", azienda

def handleEngine(schema= None):
    engine = None
    print "TIPO DB",tipodb
    if tipodb == "sqlite":
        azienda = None
        mainSchema = None
        if sqlalchemy.__version__ >= "0.7":
            from sqlalchemy.event import listen
            if hostdbforce and tipodbforce:
                engine = create_engine("sqlite:///" + hostdbforce + "/db", encoding='utf-8', proxy=MyProxy())
            else:
                if preEnv.web:
                    engine = create_engine("sqlite:///" + "/home/vete/www.promotux.it/" + main_conf.Database.sqlitedb, encoding='utf-8', proxy=MyProxy())
                else:
                    engine = create_engine("sqlite:///" + startdir() + "db", encoding='utf-8', proxy=MyProxy())
            listen(engine, 'connect', my_on_connect)
        else:
            engine = create_engine("sqlite:///" + startdir() + "db", listeners=[SetTextFactory()], proxy=MyProxy())
    elif tipodb =="postgresql":
        from promogest.EnvUtils import *
        mainSchema = "promogest2"
        engine = pg8000()
        if not engine:
            engine = py_postgresql()
        if not engine:
            engine = psycopg2new()
        if not engine:
            engine = psycopg2old()

    elif tipodb =="mysql":
        from sqlalchemy.pool import NullPool
        if preEnv.buildSchema:
            database = preEnv.buildSchema
            main_conf.Database.database = database
            main_conf.Database.azienda = database
            main_conf.save()
            print "RICORDATI DI CREARE UN  DB CHE SI CHIAMI", preEnv.buildSchema
        try:
            engine = create_engine("mysql+mysqlconnector://" + user + ":" + \
                                    password + "@" + host + ":" + preEnv.port +\
                                    "/" + preEnv.database + "?charset=utf8",
                                    poolclass=NullPool)
        except Exception as e:
            print "NON SONO RIUSCITO A CREARE L'ENGINE, NOME DEL DB NON PRESENTE? ERRORE:", e


    if not engine:
        raise RuntimeError("Non è stato trovato possibile creare un ENGINE per il DB")
    #if not preEnv.web:
    engine.echo = echosa
    #engine.echo = True
    return engine


if tipodb=="sqlite":
    azienda = None

engine = handleEngine()
tipo_eng = engine.name

def createSession():
    print " QUANTE VOLTE PASSI QUI" , azienda
    if not web:
        Session = sessionmaker(bind=engine)
        session = Session()
    else:
        print " USI QUESTA SESSIONE SCOPED"
        session = scoped_session(lambda: create_session(engine, autocommit=False))
        #session.execute("SET search_path TO {0}".format(azienda))
    return session

# Determiniamo il nome del file pickle in base all'azienda e alla ver python.

if azienda:
    meta_pickle = azienda + "-meta.pickle"+sys.version[:1]
    promogestDir = os.path.expanduser('~') + os.sep + "promogest2" + os.sep + azienda + os.sep
    meta_pickle_da_conf = main_conf.Database.azienda + "-meta.pickle"+sys.version[:1]
    promogestDir_da_conf = os.path.expanduser('~') + os.sep + "promogest2" + os.sep + main_conf.Database.azienda + os.sep
else:
    meta_pickle = None
    meta_pickle_da_conf = None
    promogestDir_da_conf = None


session = createSession()

from pickle import load as pickle_load
#metatmp = MetaData()

def delete_pickle():
    """ Cancella il file pickle del metadata
    """
    import os
    if meta_pickle:
        if os.path.exists(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip())):
            os.remove(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip()))
        if os.path.exists(str(os.path.join(promogestDir_da_conf.replace("_",""),meta_pickle_da_conf.replace("_","")).strip())):
            os.remove(str(os.path.join(promogestDir_da_conf.replace("_",""),meta_pickle_da_conf.replace("_","")).strip()))
            print "\n\n\n\nHO CANCELLATO IL FILE PICKLE QUASI SICURAMENTE BISOGNA RILANCIARE\n\n\n\n"
            restart_program()

def usePickleToMeta():
    if azienda and os.path.exists(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip())):
        print " CONTROLLO DELL'ESISTENZA DEL FILE PICKLE", str(os.path.join(promogestDir.replace("_","")))
        with open(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip()), 'rb') as f:
            try:
                meta = pickle_load(f)
                meta.bind = engine
            except:
                print "DEVO CANCELLARE IL PICKLE PERCHé NON RIESCO A TROVARLO O LEGGERLO"
                delete_pickle()
            print "USO META PICKLE FAST"
            #meta = MetaData(engine)
    else:
        print "USO META NORMALE"
        meta = MetaData(engine)
    return meta
#meta = usePickleToMeta()


preEnv.azienda = azienda
print " AZIENDAAAAAAAAAAAA 2222222222222222", azienda
#meta = None
meta = MetaData(engine)

mainSchema = None
schema = None

if tipo_eng=="postgresql":
    mainSchema = "promogest2"
    schema = azienda

params = {
        'engine': engine,
        'mainSchema': mainSchema,
        'schema': schema,
        'metadata': meta,
        'session': session,
        "tipo_db": tipodb,
        'usernameLoggedList': userdata
        }

if params['tipo_db'] == 'postgresql':
    if params["schema"]:
        fk_prefix = params['schema'] + '.'
    fk_prefix_main = mainSchema  +'.'
else:
    fk_prefix = ""
    fk_prefix_main = ""


if not preEnv.web:
    pg2log = pg_log()

def __sendmail(msg="PG"):
    msg = str(promogestDir) + " " + str(rev_locale) + "  " + str(rev_remota)
    msg = msg +"\n"
    if not web:
        return msgDef(text=msg, azienda=azienda)

def hook(et, ev, eb):
    import traceback
    if "Operation aborted" in str(ev):
        pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
        print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
        return
    if "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????" in ev:
        return
    if "[Errno 9] Bad file descriptor" in ev:
        return
    if "ProgrammingError" in str(ev):
        pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
        print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
        __sendmail()
        delete_pickle()
        return
    if "OperationalError" in str(ev):
        pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
        print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
        __sendmail()
        delete_pickle()
        return
    if "ArgumentError" in str(ev):
        pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
        print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
        __sendmail()
        delete_pickle()
        return
    if "AttributeError: 'MetaData' object has no attribute 'naming_convention'" in str(ev):
        delete_pickle()
    if "Handler" in str(ev):
        print str(ev)
        return
    if "InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush" in str(ev):
        from promogest.lib.utils import messageError
        messageError(msg="Si consiglia di riavviare il software, l'errore è stato segnalato")
    if "is already defined for this MetaData instance" in str(ev):
        delete_pickle()

    try:
        pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
    except:
        pass
    print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
    __sendmail()

sys.excepthook = hook

# DA SPOSTARE ASSOLUTAMENTE QUANTO PRIMA
print "SQLALCHEMY VERSION", sqlalchemy.__version__

if not preEnv.web:
    pg2log.info("SQLALCHEMY:" + str(sqlalchemy.__version__))



cadenza = ["MENSILE", "BIMESTRALE", "TRIMESTRALE",
            "SEMESTRALE", "ANNUALE"]

hapag = ["Fattura accompagnatoria",
        "Fattura acquisto",
        "Fattura differita acquisto",
        "Fattura differita vendita",
        "Fattura vendita",
        "Ricevuta Fiscale",
        "Vendita dettaglio",
        "Nota di credito a cliente",
        "Nota di credito da fornitore"]

solo_vendita = ["Fattura accompagnatoria",
        "Fattura differita vendita",
        "Fattura vendita",
        "Vendita dettaglio",
        ]
solo_acquisto = ["Fattura acquisto",
        "Fattura differita acquisto",
        ]
solo_acquisto_con_DDT = ["Fattura acquisto",
        "Fattura differita acquisto",
        "DDT acquisto"
        ]

solo_vendita_completo = ["Fattura accompagnatoria",
        "Fattura differita vendita", "Fattura servizio",
        "Fattura vendita",
        "Vendita dettaglio","Scarico venduto da cassa",
        "DDT vendita"
        ]

fromHtmlLits = ["Promemoria", "TestataPrimaNota",
                "Articolo", "Cliente",
                "Contatto", "Fornitore",
                "Fornitura", "Contatto",
                "Vettore", "AliquotaIva",
                "TestataCommessa", "Stoccaggio",
                "Agente"]

package = ["ONE BASIC", "ONE FULL", "ONE STANDARD",
            "PRO BASIC", "PRO STANDARD",
            "PRO FULL", "ONE PROMOWEAR", "ONE PROMOSHOP",
            "PRO PROMOWEAR", "PRO PROMOSHOP"]

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


from promogest import preEnv
# leggiamo da preEnv che è anche un file di configurazioni pre-environment
pg3 = preEnv.pg3_cla
aziendaforce = preEnv.aziendaforce
tipodbforce = preEnv.tipodbforce
hostdbforce = preEnv.hostdbforce
dbforce = preEnv.dbforce
web = preEnv.web
echosa = preEnv.echo
debugFilter = preEnv.debugFilter
debugDao = preEnv.debugDao
shop = preEnv.shop
if web:
    main_conf = preEnv.main_conf_force

from promogest.lib.config import Config
if not web:
    if pg3:
        print " USIAMO LA VERSIONE CON PYGI"
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

import decimal

try:
    import psycopg2
    psycopg2.extensions.register_adapter(decimal.Decimal,
                                                psycopg2._psycopg.Decimal)
except:
    pass
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.interfaces import PoolListener
from sqlalchemy.exc import *

from promogest.EnvUtils import *

PRODOTTO = "PromoTux"
VERSIONE = "PromoGest 2.9.0"
if pg3:
    VERSIONE = "PromoGest 2.9.90"
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
puntoA = None
puntoB = None
puntoP = None
eta = 0
tipo_pg = None
workingYear = 2013
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
SRC_PATH = os.path.split(os.path.dirname(__file__))[0]

STATIC_PATH = os.path.join(SRC_PATH, 'templates')
STATIC_PATH_FEED = os.path.join(SRC_PATH, 'feed')
IMAGE_PATH = os.path.join(STATIC_PATH, 'images/')
guiDir = '.' + os.sep + 'gui' + os.sep

SESSION_DIR = os.path.join("./", 'session')
CACHE_DIR = os.path.join("./", 'cache')
URL_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'
COOKIENAME = "promogest_web"
ALLOWED_SCHEMES = frozenset(['http', 'https', 'ftp', 'ftps'])
#mainSchema = "promogest2"

modulesList = []

sladir = "sladir/"
artImagPath = ""
languages = ""


confList = []
configDir = None

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
#if preEnv.main_conf_force:
    #main_conf = preEnv.main_conf_force


#preEnv.main_conf = main_conf
windowsrc = startdir() + 'windowsrc.xml'

if aziendaforce:
    azienda = aziendaforce
else:
    azienda = main_conf.Database.azienda

if tipodbforce:
    tipodb = tipodbforce
else:
    tipodb = main_conf.Database.tipodb

if hostdbforce:
    host = hostdbforce
else:
    host = main_conf.Database.host
try:
    nobrand = bool(main_conf.Database.nobrand)
except:
    nobrand = False
try:
    partner = main_conf.Database.partner
except:
    partner = "070 8649702 -- www.promogest.me -- assistenza@promotux.it"
#pw = main_conf.Database.pw

if tipodb == "sqlite" and not (os.path.exists(startdir() + "db")) and not tipodbforce and not preEnv.web:
    if os.path.exists("data/db"):
        shutil.copy("data/db", startdir() + "db")
        os.remove("data/db")
    elif os.path.exists("data/db.dist"):
        shutil.copy("data/db.dist", startdir() + "db")
    else:
        print("ERRORE NON RIESCO A CREARE IL DB")

if dbforce:
    database = dbforce
else:
    database = main_conf.Database.database


port = main_conf.Database.port
user = main_conf.Database.user
password = main_conf.Database.password


preEnv.port = port
preEnv.user = user
preEnv.password = password
preEnv.database = database
preEnv.host = host
preEnv.tipodb = tipodb
SUB = ""
userdata = ["", "", "", user]
engine = None
if tipodb == "sqlite":
    azienda = None
    mainSchema = None
    if sqlalchemy.__version__ >= "0.7":
        from sqlalchemy.event import listen
        if hostdbforce and tipodbforce:
            engine = create_engine("sqlite:///" + hostdbforce + "/db", encoding='utf-8', proxy=MyProxy())
        else:
            if preEnv.web:
                #engine = create_engine("sqlite:///"+"/home/vete/www.promotux.it/"+main_conf.Database.sqlitedb,encoding='utf-8')
                engine = create_engine("sqlite:///" + "/home/vete/www.promotux.it/" + main_conf.Database.sqlitedb, encoding='utf-8', proxy=MyProxy())
            else:
                engine = create_engine("sqlite:///" + startdir() + "db", encoding='utf-8', proxy=MyProxy())

        listen(engine, 'connect', my_on_connect)
    else:
        engine = create_engine("sqlite:///" + startdir() + "db", listeners=[SetTextFactory()], proxy=MyProxy())
else:
    from promogest.EnvUtils import *
    engine = pg8000()
    if not engine:
        engine = py_postgresql()
    if not engine:
        engine = psycopg2new()

    if not engine:
        engine = psycopg2old()
if not engine:
    raise RuntimeError("Non è stato trovato un backend per il database.")

#if not preEnv.web:
tipo_eng = engine.name
#engine.echo = echosa
engine.echo = True
Session = sessionmaker(bind=engine)
session = Session()
#else:
    #session = scoped_session(lambda: create_session(engine, autocommit=False))

schema_azienda = azienda
# Determiniamo il nome del file pickle in base all'azienda e alla ver python.
if azienda:
    meta_pickle = azienda + "-meta.pickle"+sys.version[:1]
    promogestDir = os.path.expanduser('~') + os.sep + "promogest2" + os.sep + azienda + os.sep
else:
    meta_pickle = "AziendaPromo-meta.pickle"+sys.version[:1]
    promogestDir = os.path.expanduser('~') + os.sep + "promogest2" + os.sep + "AziendaPromo" + os.sep

from pickle import load as pickle_load
#meta = MetaData(engine)
metatmp = MetaData()

def delete_pickle():
    """ Cancella il file pickle del metadata
    """
    import os
    if os.path.exists(os.path.join(SRC_PATH, meta_pickle)):
        os.remove(os.path.join(SRC_PATH, meta_pickle))

print "OK", os.path.exists(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip())), str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")))

if os.path.exists(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip())):
    with open(str(os.path.join(promogestDir.replace("_",""),meta_pickle.replace("_","")).strip()), 'rb') as f:
        try:
            meta = pickle_load(f)
            meta.bind = engine
        except:
            delete_pickle()
        print "USO META PICKLE FAST"
        #meta = MetaData(engine)
else:
    print "USO META NORMALE"
    meta = MetaData(engine)

#meta = MetaData(engine)
schema_azienda = azienda
preEnv.azienda = azienda
print " ENGINE", engine,preEnv.conSchemaPromogest2
if preEnv.conSchemaPromogest2 == False:
    mainSchema = preEnv.buildSchema
else:
    mainSchema = "promogest2"
params = {'engine': engine,
        'mainSchema': mainSchema,
        'schema': azienda,
        'metadata': meta,
        'session': session,
        "tipo_db": tipodb,
        'defaultLimit': 5,
        'bccaddr': ["assistenza@promotux.it"],
        'objects': ["Informazioni Tecniche",
                    "Informazioni Commerciali",
                    "Varie"],
        'usernameLoggedList': userdata}

fk_prefix = params['schema'] + '.' if params['tipo_db'] == 'postgresql' else ''
fk_prefix_main = mainSchema  +'.' if params['tipo_db'] == 'postgresql' else ''


if not preEnv.web:
    pg2log = pg_log()


def __sendmail(msg="PG"):
    msg = str(promogestDir) + " " + str(rev_locale) + "  " + str(rev_remota)
    if not web:
        return msgDef(text=msg, azienda=azienda)


def hook(et, ev, eb):
    import traceback
    if "Operation aborted" in str(ev):
        delete_pickle()
        return
    if "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????" in ev:
        return
    if "[Errno 9] Bad file descriptor" in ev:
        return
    if "Handler" in str(ev):
        print "ATTENZIONE!!! MANCA L'HANDLER", ev
        delete_pickle()
        return
    if "ProgrammingError" in str(ev):
        delete_pickle()
        return
    if "OperationalError" in str(ev):
        delete_pickle()
        return
    pg2log.info("\n  ".join(["Error occurred: traceback follows"] + list(traceback.format_exception(et, ev, eb))))
    print "\n  ".join(list(traceback.format_exception(et, ev, eb)))
    __sendmail()
#if not preEnv.web:
sys.excepthook = hook

# DA SPOSTARE ASSOLUTAMENTE QUANTO PRIMA
print "SQLALCHEMY VERSION", sqlalchemy.__version__


if os.name=="nt" and sqlalchemy.__version__ < "0.7":
    delete_pickle()
    from setuptools.command import easy_install
    easy_install.main( ["-U","sqlalchemy==0.7.8"] )
    sys.exit()

#try:
    #import keyring
#except:
    #if os.name == 'nt':
        #from setuptools.command import easy_install
        #easy_install.main(['-U', 'keyring'])
    #else:
        #pass

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

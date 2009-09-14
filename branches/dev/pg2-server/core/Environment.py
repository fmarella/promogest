#-*- coding: utf-8 -*-

# Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import os
import sys
import glob
import locale
import gettext
from config import Config
import logging
import logging.handlers
#from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug import Local, LocalManager, cached_property
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import pool
print "PG2_SERVER START"
CONFIGPATH = os.path.split(os.path.dirname(__file__))[0]
ALLOWED_SCHEMES = frozenset(['http', 'https', 'ftp', 'ftps'])
templates_dir= os.path.join(CONFIGPATH, 'templates')
#templates_dir = "/home/promo/elinuxCMS/templates"
STATIC_PATH = templates_dir
STATIC_PATH_FEED = os.path.join(CONFIGPATH, 'feed')
IMAGEPATH = os.path.join(STATIC_PATH, 'images/')
LANGPATH = os.path.join(CONFIGPATH, 'lang')
session_dir = os.path.join(CONFIGPATH, 'session')
URL_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'
COOKIENAME = "janascookie"
modules_dir = os.path.join(CONFIGPATH, 'core/plugins')
domains = os.path.join(CONFIGPATH, 'templates')
subdomains = [f for f in os.listdir(domains) if os.path.isdir(os.path.join(domains, f)) and f not in ["include","common","img"]]
sladir = "sladir/"
artImagPath = ""
importDebug = False
languages = ""
userdata = ["","","",""]
debugFilter=False
local = Local()
local_manager = LocalManager([local])
application = local('application')
feedTrac = None
feedPromo = None
orario = 0

tipo_db="sqlite"
configFile = os.path.join(CONFIGPATH, 'main.conf')
conf = Config(configFile)

azienda=conf.Database.azienda

try:
    tipodb = conf.Database.tipodb
except:
    tipodb = "postgresql"

database = conf.Database.database
port = conf.Database.port
user = conf.Database.user
password = conf.Database.password
host = conf.Database.host
userdata = ["","","",user]

if tipodb == "sqlite":
    azienda = None
    mainSchema = None
    engine =create_engine('sqlite:///data/db')
else:
    mainSchema = "promogest2"
    #azienda=conf.Database.azienda
    engine = create_engine('postgres:'+'//'
                    +user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',
                    convert_unicode=True )
tipo_eng = engine.name
engine.echo = True
meta = MetaData(engine)


#engine =create_engine("sqlite:////"+CONFIGPATH+"/db_janas.sqlite", convert_unicode=True)
engine.echo = False
#mainSchema = None
schema ="testing"
session = scoped_session(lambda: create_session(engine, autocommit=False))
meta = MetaData(engine)
#Session = sessionmaker(bind=engine)
#session = Session()
#scoped_session(new_db_session, local_manager.get_ident)
params = {  'db': engine ,
            'tipo_db' :tipo_db,
            'mainSchema': mainSchema,
            'schema': schema,
            'metadata': meta,
            'session' : session,
            'defaultLimit': 20,
            'fromaddr' : "info@e-linux.it",
            'usernameLoggedList':userdata,
            'bccaddr' : ["francesco@promotux.it"],
            'objects' : ["Informazioni Tecniche", "Informazioni Commerciali" , "Varie"],
            'widthThumbnail' : 64,
            'heightThumbnail' : 64,
            'widthdetail' : 110,
            'heightdetail': 110
            }

activeUserBody =  """
        Il suo account e' stato attivato.
        Da adesso puo' inserire i software o l'azienda.

        lo staff

        E-linux.it
        """

#def startdir():
    #startDir = getConfigureDir()
    #promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
    #return promogestStartDir

#LOG_FILENAME = startdir()+'pg2.log'
#LOG_FILENAME = "pg2_server.log"

## Set up a specific logger with our desired output level
#pg2log = logging.getLogger('PromoGest2')
#pg2log.setLevel(logging.DEBUG)

## Add the log message handler to the logger
#handler = logging.handlers.RotatingFileHandler(
              #LOG_FILENAME, maxBytes=400000, backupCount=3)

#formatter = logging.Formatter(
    #"%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(funcName)s - %(lineno)d")
## add formatter to ch
#handler.setFormatter(formatter)
#pg2log.addHandler(handler)
#pg2log.debug("\n\n<<<<<<<<<<<  AVVIO PROMOGEST >>>>>>>>>>")


#def hook(et, ev, eb):
    #import traceback
    #pg2log.debug("\n  ".join (["Error occurred: traceback follows"]+list(traceback.format_exception(et, ev, eb))))
    #print "UN ERRORE È STATO INTERCETTATO E LOGGATO, SI CONSIGLIA DI RIAVVIARE E DI CONTATTARE L'ASSISTENZA \n\nPREMERE CTRL+C PER CHIUDERE"
#sys.excepthook = hook
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
import logging
import logging.handlers
import smtplib
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.exc import *
from sqlalchemy.interfaces import ConnectionProxy
#from promogest.preEnv import *

class MyProxy(ConnectionProxy):

    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        from promogest.lib.utils import messageInfo
        from promogest.preEnv import session
        try:
            return execute(cursor, statement, parameters, context)
        except OperationalError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+ str(e) )
        except IntegrityError as e:
            messageInfo(msg="IntegrityError UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+ str(e))
            session.rollback()
        except ProgrammingError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+str(e))
            session.rollback()
            delete_pickle()
        except InvalidRequestError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+str(e))
            session.rollback()
        except AssertionError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO\n Possibile tentativo di cancellazione di un dato\n collegato ad altri dati fondamentali: "+str(e))
            session.rollback()
        except ValueError as e:
            messageInfo(msg="Risulta inserito un Valore non corretto. Ricontrolla: "+str(e))
            session.rollback()

def connect():
    import psycopg2
    from promogest.lib.utils import messageInfo
    a=None
    try:
        from promogest.preEnv import *
        a = psycopg2.connect(user=user, host=host, port=port,
                            password=password, database=database)
        cursor = a.cursor()
        cursor.execute("SELECT * FROM pg_stat_activity")
        records = cursor.fetchall()
        st = "CI SONO  ----- {0} ------- CONNESSIONI ATTIVE AL MOMENTO".format(len(records))
        print st
        print "RECORDSSSSSSSSSSSSSSSSSSSSSSSSSS", records
    except Exception, e:
        a = "CONNESSIONE AL DATABASE PRO NON RIUSCITA.\n DETTAGLIO ERRORE: [%s]" % str(e)
        messageInfo(msg=a)
        sys.exit()
    if a:
        return a

def psycopg2new():
    try:
        engine = create_engine('postgresql://', creator=connect,
                convert_unicode=True,
                encoding='utf-8',
                proxy=MyProxy())
        return engine
    except:
        return None

def psycopg2old():
    try:
        from promogest.preEnv import *
        engine = create_engine('postgres:' + '//'
                    + user + ':'
                    + password + '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',
                    pool_size=30,
                    convert_unicode=True,
                    proxy=MyProxy())
        return engine
    except:
        return None

def pg8000():
    try:
        from promogest.preEnv import *
        engine = create_engine('postgresql+pg8000:' + '//'
                    + user + ':'
                    + password + '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',
                    pool_size=30,
                    convert_unicode=True,
                    proxy=MyProxy() )
        return engine
    except:
        return None

def py_postgresql():
    try:
        from promogest.preEnv import *
        engine = create_engine('postgresql+pypostgresql:' + '//'
                    + user + ':'
                    + password + '@'
                    + host + ':'
                    + port + '/'
                    + database,
                    encoding='utf-8',
                    pool_size=30,
                    convert_unicode=True,
                    proxy=MyProxy())
        return engine
    except:
        return None

def getConfigureDir(company='__default__'):
    """ Tests if another configuration folder was indicated """
    default='promogest2'
    if company != '__default__' and company is not None:
        default = os.path.join('promogest2', company)
    return default

def startdir():
    startDir = getConfigureDir()
    promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
    return promogestStartDir

class SetTextFactory(PoolListener):
     def connect(self, dbapi_con, con_record):
         dbapi_con.text_factory = str

def my_on_connect(dbapi_con, con_record):
    dbapi_con.text_factory = str

LOG_FILENAME = startdir() + 'pg2.log'


def msgDef(text="", html="", img="", subject="", azienda="ND"):

    msgg = MIMEMultipart()
    msgg['Subject'] = azienda\
                 + "  "\
                 + str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))
    msgg['From'] = "promogestlogs@gmail.com"
    msgg['To'] = "promogestlogs@gmail.com"
    msgg.attach(MIMEText(text))
#        fp = open(self.stname, 'rb')
#    part = MIMEBase('application','octet-stream')
    part = MIMEText('text/plain')
    fp = open(LOG_FILENAME, 'rb')
    part.set_payload(fp.read())
    fp.close()
#    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="pg2.log")
    msgg.attach(part)
    _send(fromaddr="promogestlogs@gmail.com",
                total_addrs="promogestlogs@gmail.com",
                msg=msgg)


def _send(fromaddr=None, total_addrs=None, msg=None):
    try:
        server = smtplib.SMTP("smtp.gmail.com")
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("promogestlogs@gmail.com", "pr0m0t0x")
        return server.sendmail("promogestlogs@gmail.com",
                        "promogestlogs@gmail.com",
                            msg.as_string())
    except Exception as e:
        print "ERRORE NELLA SPEDIZIONE EMAIL", str(e)

def pg_log():

    # Set up a specific logger with our desired output level
    pg2log = logging.getLogger('PromoGest2')
    pg2log.setLevel(logging.INFO)

    # Add the log message handler to the logger
    try:
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=10000, backupCount=6)
    except:
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME + "bis", maxBytes=10000, backupCount=6)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(funcName)s - %(lineno)d")
    # add formatter to ch
    handler.setFormatter(formatter)
    pg2log.addHandler(handler)
    pg2log.info("\n\n<<<<<<<<<<<  AVVIO PROMOGEST >>>>>>>>>>")
    return pg2log

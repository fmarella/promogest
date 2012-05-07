# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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
from promogest import Environment
from promogest.dao.Setconf import SetConf
COOKIENAME = SetConf().select(key="cookie_name")[0].value
import ConfigParser

class Session(object):
    """
    Gestisce le sessioni utente, attraverso il controllo dei cookies di sessione
    """

    def __init__(self, req):
        self.session_dir = Environment.session_dir
        self.req = req
        self.path = req.environ['PATH_INFO'].split('/')


    def start(self, id_user):
        """ Inizializzazione sessione """
        if not os.path.exists(self.session_dir):
            os.mkdir(self.session_dir, 02770)
        cookiename =  COOKIENAME
        #cookiename = self.path[1]+'id'
        sid = self.req.cookies[cookiename]
        session_file = self.session_dir + "/" + sid
        #s_file = open(session_file, 'w')
        #s_file.write(str(id_user)+"\n")
        #s_file.close()

        config = ConfigParser.RawConfigParser()
        config.add_section('Main')
        config.set('Main', 'id_user', id_user)
        #s_file = open(session_file, 'a')
        #s_file.write(str("id_attivita="+ attivita))
        #s_file.close()
        with open(session_file, 'wb') as configfile:
            config.write(configfile)


    def destroy(self):
        """ Distruzione sessione """
        #cookiename =  self.req.environ["SERVER_NAME"] +id
        cookiename =  COOKIENAME
        #cookiename = self.path[1]+'id'
        sid = self.req.cookies[cookiename]
        session_file = self.session_dir + "/" + sid
        if os.path.exists(session_file):
            os.remove(session_file)


    def control(self):
        """
        Controllo sessione
        """
        #cookiename =  self.req.environ["SERVER_NAME"] +id
        cookiename =  COOKIENAME
        #cookiename = self.path[1]+'id'
        if not self.req.cookies.has_key(cookiename):
#            print '>>>>>           NON CI SONO COOKIE           <<<<<'
            return False
        else:
            file = self.req.cookies[cookiename]
            sess_dir = os.listdir(self.session_dir)
            if file in sess_dir:
#                print '>>>>>          AUTENTICATO           <<<<<'
                return True
            else:
#                print ">>>>>>      NON AUTENTICATO               <<<<<<"
                return False


    def getUserId(self):
        """
        Legge l'userid dal file di sessione e lo restituisce
        """
        #cookiename = self.req.environ["SERVER_NAME"]+'id'
        cookiename =  COOKIENAME
        if self.req.cookies.has_key(cookiename):
            file = self.req.cookies[cookiename]
            session_file = self.session_dir + "/" + file
            if os.path.exists(session_file):
                config = ConfigParser.RawConfigParser()
                config.read(session_file)
                #s_file = open(session_file, 'r')
                id_user = config.getint('Main', 'id_user')
                #id_user = s_file.readlines()[0]
                #s_file.close()
                return int(id_user)
            return 0
        else:
            return 0
        #print "questo è l'id dell'utente", id_user

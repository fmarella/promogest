# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Enrico Pintus <enrico@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import Dao
from promogest import Environment



class Promemoria(Dao.Dao):

    def __init__(self, connection, idPromemoria = None):
        Dao.Dao.__init__(self, connection,
                         'PromemoriaGet', 'PromemoriaSet', 'PromemoriaDel',
                         ('id', ), (idPromemoria, ))

def getScadenze():
    """
    Ritorna una lista di id di oggetti Promemoria in scadenza (e quindi da notificare)
    """
    alarms = select(Environment.connection, in_scadenza=True, offset=None, batchSize=None, immediate=True)
    returnList = []
    for alarm in alarms:
        returnList.append(alarm.id)
    return returnList

def select(connection, da_data_inserimento = None, a_data_inserimento = None,
           da_data_scadenza = None, a_data_scadenza = None, oggetto = None,
           incaricato = None, autore = None, descrizione = None, annotazione = None,
           riferimento = None, giorni_preavviso = None,
           in_scadenza = None, scaduto = None, completato = None,
           orderBy = 'data_scadenza', offset=0, batchSize=5, immediate=False):
    """ Seleziona le righe del promemoria """
    cursor = connection.execStoredProcedure('PromemoriaSel',
                                            (orderBy, da_data_inserimento, a_data_inserimento,
                                             da_data_scadenza, a_data_scadenza,
                                             oggetto, incaricato, autore,
                                             descrizione, annotazione, riferimento,
                                             giorni_preavviso,
                                             in_scadenza, scaduto, completato,
                                             offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return Dao.select(cursor=cursor, daoClass=Promemoria)
    else:
        return (cursor, Promemoria)


def count(connection, da_data_inserimento = None, a_data_inserimento = None,
          da_data_scadenza = None, a_data_scadenza = None, oggetto = None,
          incaricato = None, autore = None, descrizione = None, annotazione = None,
          riferimento = None, giorni_preavviso = None,
          in_scadenza = None, scaduto = None, completato = None):
    """ Conta i promemoria """
    return connection.execStoredProcedure('PromemoriaSel',
                                          (None, da_data_inserimento, a_data_inserimento,
                                           da_data_scadenza, a_data_scadenza, oggetto,
                                           incaricato, autore, descrizione,
                                           annotazione, riferimento, giorni_preavviso,
                                           in_scadenza, scaduto, completato,
                                           None, None),
                                          countResults = True)


def updateScadenze():
    """ Segna quali promemoria entrano nel periodo in scadenza, quali scadono, e quali sono completati """
    Environment.connection.execStoredProcedure('ScadenzePromemoriaUpd',())

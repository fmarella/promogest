# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
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

import gtk

import Dao
from promogest import Environment



class Inventario(Dao.Dao):

    def __init__(self, connection, idInventario = None):
        Dao.Dao.__init__(self, connection,
                         'InventarioGet', 'InventarioSet', 'InventarioDel',
                         ('id', ), (idInventario, ))



def control(window):
    """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio """
    res = count(connection=Environment.connection, anno=Environment.conf.workingYear)

    if res == 0:
        # richiesta di generazione dell'inventario
        msg = ("Non e' presente nessun caricamento di inventario nell'anno di lavoro:\n\n" +
               "si desidera generarne uno ?")
        dialog = gtk.MessageDialog(window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            # genera l'inventario per l'anno in corso sulla base delle giacenze finali 
            # dell'anno precedente, per ogni magazzino e per ogni articolo
            Environment.connection.execStoredProcedure('InventarioFill', (int(Environment.conf.workingYear),))

            msg = ("Generazione completata.\n\nEffettuare le dovute modifiche dall'apposita maschera\n" +
                   "di caricamento inventario dopo aver fatto i rilevamenti\n" +
                   "delle merci nei magazzini.\n")
            dialog = gtk.MessageDialog(window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()


def select(connection, orderBy=None, anno=None, idMagazzino=None, idArticolo=None,
           daDataAggiornamento=None, aDataAggiornamento=None,
           offset=0, batchSize=5, immediate=False):
    """ Seleziona gli inventari relativi agli articoli """
    cursor = connection.execStoredProcedure('InventarioSel',
                                            (orderBy, anno, idMagazzino, idArticolo,
                                             daDataAggiornamento, aDataAggiornamento, 
                                             offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return Dao.select(cursor=cursor, daoClass=Inventario)
    else:
        return (cursor, Inventario)


def count(connection, anno=None, idMagazzino=None, idArticolo=None,
          daDataAggiornamento=None, aDataAggiornamento=None):
    """ Conta gli inventari relativi agli articoli """
    return connection.execStoredProcedure('InventarioSel',
                                          (None, anno, idMagazzino, idArticolo,
                                           daDataAggiornamento, aDataAggiornamento, 
                                           None, None),
                                          countResults = True)

# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


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

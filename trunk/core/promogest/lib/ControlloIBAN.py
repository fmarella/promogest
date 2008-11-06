# -*- coding: iso-8859-15 -*-

# This file is part of Promogest - Copyright (C) 2007 by Promotux Informatica
# Copyright (C) 2007 by JJDaNiMoTh
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

#!/usr/local/bin/python

from string import join

# L'International Bank Account Number, piè noto nella forma abbreviata IBAN
# e' uno standard internazionale utilizzato per identificare un'utenza bancaria.
# Fu originariamente ideato dal Comitato Europeo per gli Standard Bancari
# (European Committee for Banking Standards) e successivamente fu adottato
# dall'ISO come standard ISO 13616:1997.

# L'IBAN è composto da 2 lettere che rappresentano la nazione della banca
# secondo lo standard ISO 3166, da 2 cifre di controllo e dal BBAN
# (Basic Bank Account Number) che è un codice di non meno di 13 cifre che
# identifica la banca e il conto corrente:

#      ITPP CAAA AABB BBBN NNNN NNNN NNN
#      IT73 J061 5513 0000 0000 0012 345 (esempio)

#      IT            Codice paese (IT)
#      PP            Cifra di controllo (73)
#      C             CIN (J)
#      AAAAA         ABI (06155)
#      BBBBB         CAB (13000)
#      NNNNNNNNNNNN  CONTO (12345)


class IBAN():
    def __init__(self, iban):
        if type(iban) == str:
            self.iban = join(iban.split(),"")
            self.iban = self.iban.upper()
        else:
            self.abi = ""
            self.cab = ""
            self.cin = ""
            self.account = ""
            self.iban = -1
            return

        if self.verifyIBAN(self.iban):
            self.abi = self.getABI(self.iban)
            self.cab = self.getCAB(self.iban)
            self.cin = self.getCIN(self.iban)
            self.account = self.getAccount(self.iban)
        else:
            self.abi = ""
            self.cab = ""
            self.cin = ""
            self.account = ""
            self.iban = -1

    def msg(self, msg):

#        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
#            gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
#        dialog.run()
#        dialog.destroy()
        print msg

    def getABI(self, iban):
        """
        Restituisce una stringa con il codice ABI
        """

        abi = iban[5:10]
        return abi

    def getCAB(self, iban):
        """
        Restituisce una stringa con il codice CAB
        """

        cab = iban[10:15]
        return cab

    def getCIN(self, iban):
        """
        Restituisce il codice CIN
        """

        return iban[4]

    def getAccount(self, iban):
        """
        Restituisce una stringa con il conto corrente
        """

        cc = iban[15:27]
        return cc

    def verifyIBAN(self, iban):
        """
        Verifica formalmente la correttezza del codice IBAN.
        """

        def checkABI(iban):
            """
            Controlla l'abi
            """
            for i in range(1,5):
                if iban[4+i].isalpha():
                    self.msg('Attenzione ti preghiamo di verificare la sezione ABI')
                    return False

            return True

        def checkCAB(iban):
            """
            Controlla il CAB
            """

            for i in range(1,5):
                if iban[i+9].isalpha():
                    self.msg('Attenzione ti preghiamo di verificare la sezione CAB')
                    return False

            return True

        def checkAccount(iban):
            """
            Controlla il numero di conto
            """

            for i in range(1,10):
                if iban[i+14].isalpha():
                    self.msg('Attenzione ti preghiamo di verificare la sezione C/C')
                    return False
            return True

        def checkCIN(iban):
            """
            Controlla il CIN
            """

            if iban[4].isdigit():
                self.msg('Attenzione ti preghiamo di verificare il CIN. Deve essere una lettera')
                return False

            return True

        def checkLenght(iban, lenght):
            """
            Controlla la lunghezza del codice IBAN
            """

            if len(iban) != lenght:
                self.msg('Attenzione ti preghiamo di controllare la lunghezza del codice IBAN')
                return False
            else:
                return True

        def checkNation(iban):
            """
            Controlla la nazione dell'IBAN. Qui calcoliamo solo quelle italiane
            e quelle di San Marino.
            """

            if (iban.count('IT',0,2) != 1) and (iban.count('SM',0,2) != 1):
                self.msg('Lo strumento di verifica controlla solo i codici IBAN per Italia e San Marino.')
                return False

            cab_SM = ""
            for i in range(1, 5):
                cab_SM = cab_SM + iban[9+i]

            if iban.count('SM',0,2) == 1 and ((int(cab_SM)<9800) or (int(cab_SM)>9810) or (cab_SM.isalpha())):
                self.msg('Attenzione ti preghiamo di verificare i dati perche` non coerenti')
                return False

            return True

        if not (checkLenght(iban, 27)) or not (checkNation(iban)) or not (checkCIN(iban)) or not (
        checkABI(iban)) or not (checkCAB(iban)) or not (checkAccount(iban)):
            return False

        return True


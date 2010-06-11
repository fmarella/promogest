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
#      IT73J0615513000000000012345 (esempio)

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

#
# IBAN_Check.py
# Utility to check the integrity of an <strong class="highlight">IBAN</strong> bank account No.
# <strong class="highlight">Python</strong> 2.5.1

# Sample <strong class="highlight">IBAN</strong> account numbers.
#-----------------------------
# BE31435411161155
# CH5108686001256515001
# GB35MIDL40253432144670


# Dictionaries - Refer to ISO 7064 mod 97-10
letter_dic={"A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "H":17, "I":18, "J":19, "K":20, "L":21, "M":22,
            "N":23, "O":24, "P":25, "Q":26, "R":27, "S":28, "T":29, "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35,
            "0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}

# ISO 3166-1 alpha-2 country code
country_dic={"AL":[28,"Albania"],
             "AD":[24,"Andorra"],
             "AT":[20,"Austria"],
             "BE":[16,"Belgium"],
             "BA":[20,"Bosnia"],
             "BG":[22,"Bulgaria"],
             "HR":[21,"Croatia"],
             "CY":[28,"Cyprus"],
             "CZ":[24,"Czech Republic"],
             "DK":[18,"Denmark"],
             "EE":[20,"Estonia"],
             "FO":[18,"Faroe Islands"],
             "FI":[18,"Finland"],
             "FR":[27,"France"],
             "DE":[22,"Germany"],
             "GI":[23,"Gibraltar"],
             "GR":[27,"Greece"],
             "GL":[18,"Greenland"],
             "HU":[28,"Hungary"],
             "IS":[26,"Iceland"],
             "IE":[22,"Ireland"],
             "IL":[23,"Israel"],
             "IT":[27,"Italy"],
             "LV":[21,"Latvia"],
             "LI":[21,"Liechtenstein"],
             "LT":[20,"Lithuania"],
             "LU":[20,"Luxembourg"],
             "MK":[19,"Macedonia"],
             "MT":[31,"Malta"],
             "MU":[30,"Mauritius"],
             "MC":[27,"Monaco"],
             "ME":[22,"Montenegro"],
             "NL":[18,"Netherlands"],
             "NO":[15,"Northern Ireland"],
             "PO":[28,"Poland"],
             "PT":[25,"Portugal"],
             "RO":[24,"Romania"],
             "SM":[27,"San Marino"],
             "SA":[24,"Saudi Arabia"],
             "RS":[22,"Serbia"],
             "SK":[24,"Slovakia"],
             "SI":[19,"Slovenia"],
             "ES":[24,"Spain"],
             "SE":[24,"Sweden"],
             "CH":[21,"Switzerland"],
             "TR":[26,"Turkey"],
             "TN":[24,"Tunisia"],
             "GB":[22,"United Kingdom"]}

def check(n):
    if int(n)%97 !=1:
        result=0                                                # False
    else:
        result=1                                                # True
    return result

#while True:
#    # <strong class="highlight">IBAN</strong> = (raw_input("Enter account No. : ")).upper()          # Input account No.
#    <strong class="highlight">IBAN</strong> = "GB35MIDL40253432144670"                             # Sample UK <strong class="highlight">IBAN</strong>
#    print "original:",
#    print <strong class="highlight">IBAN</strong>
#    length = len(<strong class="highlight">IBAN</strong>)
#    country = <strong class="highlight">IBAN</strong>[:2]
#    if country_dic.has_key(country):
#        data = country_dic[country]
#        length_c = data[0]
#        name_c = data[1]
#        if length == length_c:
#            print name_c,"/ <strong class="highlight">IBAN</strong> length",length_c,"OK!"
#            header = <strong class="highlight">IBAN</strong>[:4]                                   # Get the first four characters
#            body = <strong class="highlight">IBAN</strong>[4:]                                     # And the remaining characters
#            <strong class="highlight">IBAN</strong> = body+header                                  # Move the first block at the end
#            IBAN_ = list(<strong class="highlight">IBAN</strong>)                                  # Transform string into a list
#            print "C1:", <strong class="highlight">IBAN</strong>
#            string_=""
##            for index in range(len(IBAN_)):                     # Convert letters to integers
##                if letter_dic.has_key(IBAN_[index]):
##                    value = letter_dic[IBAN_[index]]
##                    print IBAN_[index],
##                    IBAN_[index] = value
##                    print value
##            for index in range(len(IBAN_)):                     # Transform list into a string
##                string_ = string_ + str(IBAN_[index])
#            string_="".join(map(lambda x: str(letter_dic[x]), IBAN_))
#            print string_
#            valid = check(string_)                              # Check validity
#            if not valid:
#                print "Not a valid <strong class="highlight">IBAN</strong> account No."
#            else:
#                print "<strong class="highlight">IBAN</strong> account No. accepted."              # Rebuild the original <strong class="highlight">IBAN</strong>
#                trailer = <strong class="highlight">IBAN</strong>[len(<strong class="highlight">IBAN</strong>)-4:]                    # Get the four last characters
#                body = <strong class="highlight">IBAN</strong>[:len(<strong class="highlight">IBAN</strong>)-4]                       # And the remaining characters
#                <strong class="highlight">IBAN</strong> = trailer+body                             # Move the trailer at the begin
#                print "Exit loop ..."
#                break
#        else:
#            print name_c,"/ Wrong <strong class="highlight">IBAN</strong> code length!"
#    else:
#        print "Wrong <strong class="highlight">IBAN</strong> country code!"

#print "<strong class="highlight">IBAN</strong> account No. :",<strong class="highlight">IBAN</strong>
## Display a formated account No. (Thanks to Griboullis)
#split_IBAN = lambda block,string:[string[f:f+block] for f in range(0,len(string),block)]
#BankAccountNo = split_IBAN(4,<strong class="highlight">IBAN</strong>)
#print "Formated bank account No :",
#for block in BankAccountNo:
#    print block,
#print

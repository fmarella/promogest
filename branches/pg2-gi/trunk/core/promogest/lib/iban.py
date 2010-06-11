# -*- coding: utf-8 -*-
#! /usr/bin/env python

"""iban.py 0.3 - Create or check International Bank Account Numbers (IBAN).

Copyright (C) 2002-2003, Thomas Günther (toms-cafe.de)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

Usage as module:
    from iban import *

    code, bank, account = "DE", "12345678", "123456789"
    try:
        iban = create_iban(code, bank, account)
    except IBANError, err:
        print err
    else:
        print "  Correct IBAN: %s << %s ?? %s %s" % (iban, code, bank, account)

    iban = "de58123456780123456789".upper()
    try:
        code, checksum, bank, account = check_iban(iban)
    except IBANError, err:
        print err
    else:
        print "  Correct IBAN: %s >> %s %s %s %s" % (iban, code, checksum,
                                                     bank, account)
"""

__all__ = ["create_iban", "check_iban", "IBANError"]

usage = \
"""Create or check International Bank Account Numbers (IBAN).

Usage: iban <iban>
       iban <country> <bank/branch> <account>
       iban -h | -f | -e | -t

 e.g.: iban DE58123456780123456789
       iban DE 12345678 123456789

       <iban>         is the International Bank Account Number (IBAN)
       <country>      is the Country Code from ISO 3166
       <bank/branch>  is the Bank/Branch Code part of the IBAN from ISO 13616
       <account>      is the Account Number including check digits

       iban -h        prints this message
       iban -f        prints a table with the country specific iban format
       iban -e        prints an example for each country
       iban -t        prints some test data

Information about IBAN are from European Committee for Banking Standards
(www.ecbs.org/iban.htm). IBAN is an ISO standard (ISO 13616: 1997).
"""

class Country:
    """Class for country specific iban data."""

    def __init__(self, name, code, bank_form, acc_form):
        """Constructor for Country objects.

        Arguments:
            name      - Name of the country
            code      - Country Code from ISO 3166
            bank_form - Format of bank/branch code part (e.g. "0 4a 0 ")
            acc_form  - Format of account number part (e.g. "0  11  2n")
        """
        self.code = code
        self.name = name
        self.bank = self._decode_format(bank_form)
        self.acc  = self._decode_format(acc_form)

    def bank_lng(self):
        return reduce(lambda sum, part: sum + part[0], self.bank, 0)

    def acc_lng(self):
        return reduce(lambda sum, part: sum + part[0], self.acc, 0)

    def total_lng(self):
        return 4 + self.bank_lng() + self.acc_lng()

    def _decode_format(self, form):
        form_list = []
        for part in form.split(" "):
            if part:
                a_n = part[-1]
                if a_n in ("a", "n"):
                    part = part[:-1]
                else:
                    a_n = "an"
                lng = int(part)
                form_list.append((lng, a_n))
        return tuple(form_list)

# BBAN data from ISO 13616, Country codes from ISO 3166 (www.iso.org).
iban_data = (Country("Andorra",        "AD", "0  4n 4n", "0  12   0 "),
             Country("Austria",        "AT", "0  5n 0 ", "0  11n  0 "),
             Country("Belgium",        "BE", "0  3n 0 ", "0   7n  2n"),
             Country("Switzerland",    "CH", "0  5n 0 ", "0  12   0 "),
             Country("Czech Republic", "CZ", "0  4n 0 ", "0  16n  0 "),
             Country("Germany",        "DE", "0  8n 0 ", "0  10n  0 "),
             Country("Denmark",        "DK", "0  4n 0 ", "0   9n  1n"),
             Country("Spain",          "ES", "0  4n 4n", "2n 10n  0 "),
             Country("Finland",        "FI", "0  6n 0 ", "0   7n  1n"),
             Country("Faroe Islands",  "FO", "0  4n 0 ", "0   9n  1n"),
             Country("France",         "FR", "0  5n 5n", "0  11   2n"),
             Country("United Kingdom", "GB", "0  4a 6n", "0   8n  0 "),
             Country("Gibraltar",      "GI", "0  4a 0 ", "0  15   0 "),
             Country("Greenland",      "GL", "0  4n 0 ", "0   9n  1n"),
             Country("Greece",         "GR", "0  3n 4n", "0  16   0 "),
             Country("Hungary",        "HU", "0  3n 4n", "1  15   1 "),
             Country("Ireland",        "IE", "0  4a 6n", "0   8n  0 "),
             Country("Iceland",        "IS", "0  4n 0 ", "0  18n  0 "),
             Country("Italy",          "IT", "1a 5n 5n", "0  12   0 "),
             Country("Liechtenstein",  "LI", "0  5n 0 ", "0  12   0 "),
             Country("Luxembourg",     "LU", "0  3n 0 ", "0  13   0 "),
             Country("Latvia",         "LV", "0  4a 0 ", "0  13   0 "),
             Country("Monaco",         "MC", "0  5n 5n", "0  11   2n"),
             Country("Netherlands",    "NL", "0  4a 0 ", "0  10n  0 "),
             Country("Norway",         "NO", "0  4n 0 ", "0   6n  1n"),
             Country("Poland",         "PL", "0  8n 0 ", "0  16   0 "),
             Country("Portugal",       "PT", "0  4n 4n", "0  11n  2n"),
             Country("Sweden",         "SE", "0  3n 0 ", "0  16n  1n"),
             Country("Slovenia",       "SI", "0  5n 0 ", "0   8n  2n"),
             Country("San Marino",     "SM", "1a 5n 5n", "0  12   0 "))

def country_data(code):
    """Search the country code in the iban_data list."""
    for country in iban_data:
        if country.code == code:
            return country
    return None

def mod97(digit_string):
    """Modulo 97 for huge numbers given as digit strings.

    This function is a prototype for a JavaScript implementation.
    In Python this can be done much easier: long(digit_string) % 97.
    """
    m = 0
    for d in digit_string:
        m = (m * 10 + int(d)) % 97
    return m

def fill0(s, l):
    """Fill the string with leading zeros until length is reached."""
    import string
    return string.zfill(s, l)

def checksum_iban(iban):
    """Calculate 2-digit checksum of an IBAN."""
    code     = iban[:2]
    checksum = iban[2:4]
    bban     = iban[4:]

    # Assemble digit string
    digits = ""
    for ch in bban:
        if ch.isdigit():
            digits += ch
        else:
            digits += str(ord(ch) - ord("A") + 10)
    for ch in code:
        digits += str(ord(ch) - ord("A") + 10)
    digits += checksum

    # Calculate checksum
    checksum = 98 - mod97(digits)
    return fill0(str(checksum), 2)

def fill_account(country, account):
    """Fill the account number part of IBAN with leading zeros."""
    return fill0(account, country.acc_lng())

def invalid_part(form_list, iban_part):
    """Check if syntax of the part of IBAN is invalid."""
    for lng, a_n in form_list:
        if lng > len(iban_part):
            lng = len(iban_part)
        for ch in iban_part[:lng]:
            a = ("A" <= ch <= "Z")
            n = ch.isdigit()
            if (not a and not n) or \
               (not a and a_n == "a") or \
               (not n and a_n == "n"):
                return 1
        iban_part = iban_part[lng:]
    return 0

def invalid_bank(country, bank):
    """Check if syntax of the bank/branch code part of IBAN is invalid."""
    return len(bank) != country.bank_lng() or \
           invalid_part(country.bank, bank)

def invalid_account(country, account):
    """Check if syntax of the account number part of IBAN is invalid."""
    return len(account) > country.acc_lng() or \
           invalid_part(country.acc, fill_account(country, account))

def calc_iban(country, bank, account):
    """Calculate the checksum and assemble the IBAN."""
    account = fill_account(country, account)
    checksum = checksum_iban(country.code + "00" + bank + account)
    return country.code + checksum + bank + account

def iban_okay(iban):
    """Check the checksum of an IBAN."""
    return checksum_iban(iban) == "97"

class IBANError(Exception):
    def __init__(self, errmsg):
        Exception.__init__(self, errmsg)

def create_iban(code, bank, account):
    """Check the input, calculate the checksum and assemble the IBAN.

    Return the calculated IBAN.
    Raise an IBANError exception if the input is not correct.
    """
    err = None
    country = country_data(code)
    if not country:
        err = "Unknown Country Code: %s" % code
    elif len(bank) != country.bank_lng():
        err = "Bank/Branch Code length %s is not correct for %s (%s)" % \
              (len(bank), country.name, country.bank_lng())
    elif invalid_bank(country, bank):
        err = "Bank/Branch Code %s is not correct for %s" % \
              (bank, country.name)
    elif len(account) > country.acc_lng():
        err = "Account Number length %s is not correct for %s (%s)" % \
              (len(account), country.name, country.acc_lng())
    elif invalid_account(country, account):
        err = "Account Number %s is not correct for %s" % \
              (account, country.name)
    if err:
        raise IBANError(err)
    return calc_iban(country, bank, account)

def check_iban(iban):
    """Check the syntax and the checksum of an IBAN.

    Return the parts of the IBAN: Country Code, Checksum, Bank/Branch Code and
    Account number.
    Raise an IBANError exception if the input is not correct.
    """
    err = None
    code     = iban[:2]
    checksum = iban[2:4]
    bban     = iban[4:]
    country = country_data(code)
    if not country:
        err = "Codice nazione sconosciuto: %s" % code
    elif len(iban) != country.total_lng():
        err = "Lunghezza IBAN %s non corretta per %s (%s)" % \
              (len(iban), country.name, country.total_lng())
    else:
        bank_lng = country.bank_lng()
        bank     = bban[:bank_lng]
        account  = bban[bank_lng:]
        if invalid_bank(country, bank):
            err = "Bank/Branch Code %s non è corretto per %s" % \
                  (bank, country.name)
        elif invalid_account(country, account):
            err = "Numero conto  %s non è corretto per %s" % \
                  (account, country.name)
        elif not iban_okay(iban):
            err = "IBAN: Non corretto %s >> %s %s %s %s" % \
                  (iban, code, checksum, bank, account)
    if err:
        raise IBANError(err)
    return code, checksum, bank, account

def print_new_iban(code, bank, account):
    """Check the input, calculate the checksum, assemble and print the IBAN."""
    try:
        iban = create_iban(code, bank, account)
    except IBANError, err:
        print err
        return ""
    print "  Correct IBAN: %s << %s ?? %s %s" % (iban, code, bank, account)
    return iban

def print_iban_parts(iban):
    """Check the syntax and the checksum of an IBAN and print the parts."""
    try:
        code, checksum, bank, account = check_iban(iban)
    except IBANError, err:
        print err
        return ()
    print "  Correct IBAN: %s >> %s %s %s %s" % (iban, code, checksum,
                                                 bank, account)
    return code, checksum, bank, account

def print_format():
    """Print a table with the country specific iban format."""
    print "IBAN-Format (a = alphabetic, n = numeric, an = alphanumeric):"
    print "                    | Bank/Branch-Code      | Account Number"
    print " Country       Code | check1  bank  branch  |" + \
          " check2 number check3"
    print "--------------------|-----------------------|" + \
          "---------------------"
    for country in iban_data:
        print country.name.ljust(14), "|", country.code, "|",
        for lng, a_n in country.bank:
            if lng:
                print str(lng).rjust(3), a_n.ljust(2),
            else:
                print "  -   ",
        print " |",
        for lng, a_n in country.acc:
            if lng:
                print str(lng).rjust(3), a_n.ljust(2),
            else:
                print "  -   ",
        print

def print_test_data(*data):
    """Print a table with iban test data."""
    for code, bank, account, checksum in data:
        created_iban = print_new_iban(code, bank, account)
        if created_iban:
            iban = code + checksum + bank + \
                   fill_account(country_data(code), account)
            print_iban_parts(iban)
            if iban != created_iban:
                print "  Changed IBAN"

def print_examples():
    print "IBAN-Examples:"
    print_test_data(("AD", "00012030",    "200359100100",       "12"),
                    ("AT", "19043",       "00234573201",        "61"),
                    ("BE", "539",         "007547034",          "68"),
                    ("CH", "00762",       "011623852957",       "93"),
                    ("CZ", "0800",        "0000192000145399",   "65"),
                    ("DE", "37040044",    "0532013000",         "89"),
                    ("DK", "0040",        "0440116243",         "50"),
                    ("ES", "21000418",    "450200051332",       "91"),
                    ("FI", "123456",      "00000785",           "21"),
                    ("FO", "0040",        "0440116243",         "20"),
                    ("FR", "2004101005",  "0500013M02606",      "14"),
                    ("GB", "NWBK601613",  "31926819",           "29"),
                    ("GI", "NWBK",        "000000007099453",    "75"),
                    ("GL", "0040",        "0440116243",         "20"),
                    ("GR", "0110125",     "0000000012300695",   "16"),
                    ("HU", "1177301",     "61111101800000000",  "42"),
                    ("IE", "AIBK931152",  "12345678",           "29"),
                    ("IS", "0159",        "260076545510730339", "14"),
                    ("IT", "X0542811101", "000000123456",       "60"),
                    ("LI", "00762",       "011623852957",       "09"),
                    ("LU", "001",         "9400644750000",      "28"),
                    ("LV", "BANK",        "0000435195001",      "80"),
                    ("MC", "2004101005",  "0500013M02606",      "93"),
                    ("NL", "ABNA",        "0417164300",         "91"),
                    ("NO", "8601",        "1117947",            "93"),
                    ("PL", "11402004",    "0000300201355387",   "27"),
                    ("PT", "00020123",    "1234567890154",      "50"),
                    ("SE", "500",         "00000054910000003",  "35"),
                    ("SI", "19100",       "0000123438",         "56"),
                    ("SM", "X0542811101", "000000123456",       "88"))

def print_test():
    print "IBAN-Test:"
    print_test_data(("XY", "1",           "2",                  "33"),
                    ("AD", "11112222",    "C3C3C3C3C3C3",       "11"),
                    ("AD", "1111222",     "C3C3C3C3C3C3",       "11"),
                    ("AD", "X1112222",    "C3C3C3C3C3C3",       "11"),
                    ("AD", "111@2222",    "C3C3C3C3C3C3",       "11"),
                    ("AD", "1111X222",    "C3C3C3C3C3C3",       "11"),
                    ("AD", "1111222@",    "C3C3C3C3C3C3",       "11"),
                    ("AD", "11112222",    "@3C3C3C3C3C3",       "11"),
                    ("AD", "11112222",    "C3C3C3C3C3C@",       "11"),
                    ("AT", "11111",       "22222222222",        "17"),
                    ("AT", "1111",        "22222222222",        "17"),
                    ("AT", "X1111",       "22222222222",        "17"),
                    ("AT", "1111@",       "22222222222",        "17"),
                    ("AT", "11111",       "X2222222222",        "17"),
                    ("AT", "11111",       "2222222222@",        "17"),
                    ("BE", "111",         "222222233",          "93"),
                    ("BE", "11",          "222222233",          "93"),
                    ("BE", "X11",         "222222233",          "93"),
                    ("BE", "11@",         "222222233",          "93"),
                    ("BE", "111",         "X22222233",          "93"),
                    ("BE", "111",         "222222@33",          "93"),
                    ("BE", "111",         "2222222X3",          "93"),
                    ("BE", "111",         "22222223@",          "93"),
                    ("CH", "11111",       "B2B2B2B2B2B2",       "60"),
                    ("CH", "1111",        "B2B2B2B2B2B2",       "60"),
                    ("CH", "X1111",       "B2B2B2B2B2B2",       "60"),
                    ("CH", "1111@",       "B2B2B2B2B2B2",       "60"),
                    ("CH", "11111",       "@2B2B2B2B2B2",       "60"),
                    ("CH", "11111",       "B2B2B2B2B2B@",       "60"),
                    ("CZ", "1111",        "2222222222222222",   "68"),
                    ("CZ", "111",         "2222222222222222",   "68"),
                    ("CZ", "X111",        "2222222222222222",   "68"),
                    ("CZ", "111@",        "2222222222222222",   "68"),
                    ("CZ", "1111",        "X222222222222222",   "68"),
                    ("CZ", "1111",        "222222222222222@",   "68"),
                    ("DE", "11111111",    "2222222222",         "16"),
                    ("DE", "1111111",     "2222222222",         "16"),
                    ("DE", "X1111111",    "2222222222",         "16"),
                    ("DE", "1111111@",    "2222222222",         "16"),
                    ("DE", "11111111",    "X222222222",         "16"),
                    ("DE", "11111111",    "222222222@",         "16"),
                    ("DK", "1111",        "2222222223",         "79"),
                    ("DK", "111",         "2222222223",         "79"),
                    ("DK", "X111",        "2222222223",         "79"),
                    ("DK", "111@",        "2222222223",         "79"),
                    ("DK", "1111",        "X222222223",         "79"),
                    ("DK", "1111",        "22222222@3",         "79"),
                    ("DK", "1111",        "222222222X",         "79"),
                    ("ES", "11112222",    "334444444444",       "71"),
                    ("ES", "1111222",     "334444444444",       "71"),
                    ("ES", "X1112222",    "334444444444",       "71"),
                    ("ES", "111@2222",    "334444444444",       "71"),
                    ("ES", "1111X222",    "334444444444",       "71"),
                    ("ES", "1111222@",    "334444444444",       "71"),
                    ("ES", "11112222",    "X34444444444",       "71"),
                    ("ES", "11112222",    "3@4444444444",       "71"),
                    ("ES", "11112222",    "33X444444444",       "71"),
                    ("ES", "11112222",    "33444444444@",       "71"),
                    ("FI", "111111",      "22222223",           "68"),
                    ("FI", "11111",       "22222223",           "68"),
                    ("FI", "X11111",      "22222223",           "68"),
                    ("FI", "11111@",      "22222223",           "68"),
                    ("FI", "111111",      "X2222223",           "68"),
                    ("FI", "111111",      "222222@3",           "68"),
                    ("FI", "111111",      "2222222X",           "68"),
                    ("FO", "1111",        "2222222223",         "49"),
                    ("FO", "111",         "2222222223",         "49"),
                    ("FO", "X111",        "2222222223",         "49"),
                    ("FO", "111@",        "2222222223",         "49"),
                    ("FO", "1111",        "X222222223",         "49"),
                    ("FO", "1111",        "22222222@3",         "49"),
                    ("FO", "1111",        "222222222X",         "49"),
                    ("FR", "1111122222",  "C3C3C3C3C3C44",      "44"),
                    ("FR", "111112222",   "C3C3C3C3C3C44",      "44"),
                    ("FR", "X111122222",  "C3C3C3C3C3C44",      "44"),
                    ("FR", "1111@22222",  "C3C3C3C3C3C44",      "44"),
                    ("FR", "11111X2222",  "C3C3C3C3C3C44",      "44"),
                    ("FR", "111112222@",  "C3C3C3C3C3C44",      "44"),
                    ("FR", "1111122222",  "@3C3C3C3C3C44",      "44"),
                    ("FR", "1111122222",  "C3C3C3C3C3@44",      "44"),
                    ("FR", "1111122222",  "C3C3C3C3C3CX4",      "44"),
                    ("FR", "1111122222",  "C3C3C3C3C3C4@",      "44"),
                    ("GB", "AAAA222222",  "33333333",           "45"),
                    ("GB", "AAAA22222",   "33333333",           "45"),
                    ("GB", "8AAA222222",  "33333333",           "45"),
                    ("GB", "AAA@222222",  "33333333",           "45"),
                    ("GB", "AAAAX22222",  "33333333",           "45"),
                    ("GB", "AAAA22222@",  "33333333",           "45"),
                    ("GB", "AAAA222222",  "X3333333",           "45"),
                    ("GB", "AAAA222222",  "3333333@",           "45"),
                    ("GI", "AAAA",        "B2B2B2B2B2B2B2B",    "72"),
                    ("GI", "AAA",         "B2B2B2B2B2B2B2B",    "72"),
                    ("GI", "8AAA",        "B2B2B2B2B2B2B2B",    "72"),
                    ("GI", "AAA@",        "B2B2B2B2B2B2B2B",    "72"),
                    ("GI", "AAAA",        "@2B2B2B2B2B2B2B",    "72"),
                    ("GI", "AAAA",        "B2B2B2B2B2B2B2@",    "72"),
                    ("GL", "1111",        "2222222223",         "49"),
                    ("GL", "111",         "2222222223",         "49"),
                    ("GL", "X111",        "2222222223",         "49"),
                    ("GL", "111@",        "2222222223",         "49"),
                    ("GL", "1111",        "X222222223",         "49"),
                    ("GL", "1111",        "22222222@3",         "49"),
                    ("GL", "1111",        "222222222X",         "49"),
                    ("GR", "1112222",     "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "111222",      "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "X112222",     "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "11@2222",     "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "111X222",     "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "111222@",     "C3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "1112222",     "@3C3C3C3C3C3C3C3",   "61"),
                    ("GR", "1112222",     "C3C3C3C3C3C3C3C@",   "61"),
                    ("HU", "1112222",     "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "111222",      "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "X112222",     "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "11@2222",     "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "111X222",     "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "111222@",     "CD4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "1112222",     "@D4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "1112222",     "C@4D4D4D4D4D4D4D5",  "36"),
                    ("HU", "1112222",     "CD4D4D4D4D4D4D4@5",  "36"),
                    ("HU", "1112222",     "CD4D4D4D4D4D4D4D@",  "36"),
                    ("IE", "AAAA222222",  "33333333",           "18"),
                    ("IE", "AAAA22222",   "33333333",           "18"),
                    ("IE", "8AAA222222",  "33333333",           "18"),
                    ("IE", "AAA@222222",  "33333333",           "18"),
                    ("IE", "AAAAX22222",  "33333333",           "18"),
                    ("IE", "AAAA22222@",  "33333333",           "18"),
                    ("IE", "AAAA222222",  "X3333333",           "18"),
                    ("IE", "AAAA222222",  "3333333@",           "18"),
                    ("IS", "1111",        "222222222222222222", "98"),
                    ("IS", "111",         "222222222222222222", "98"),
                    ("IS", "X111",        "222222222222222222", "98"),
                    ("IS", "111@",        "222222222222222222", "98"),
                    ("IS", "1111",        "X22222222222222222", "98"),
                    ("IS", "1111",        "22222222222222222@", "98"),
                    ("IT", "A2222233333", "D4D4D4D4D4D4",       "43"),
                    ("IT", "A222223333",  "D4D4D4D4D4D4",       "43"),
                    ("IT", "82222233333", "D4D4D4D4D4D4",       "43"),
                    ("IT", "AX222233333", "D4D4D4D4D4D4",       "43"),
                    ("IT", "A2222@33333", "D4D4D4D4D4D4",       "43"),
                    ("IT", "A22222X3333", "D4D4D4D4D4D4",       "43"),
                    ("IT", "A222223333@", "D4D4D4D4D4D4",       "43"),
                    ("IT", "A2222233333", "@4D4D4D4D4D4",       "43"),
                    ("IT", "A2222233333", "D4D4D4D4D4D@",       "43"),
                    ("LI", "11111",       "B2B2B2B2B2B2",       "73"),
                    ("LI", "1111",        "B2B2B2B2B2B2",       "73"),
                    ("LI", "X1111",       "B2B2B2B2B2B2",       "73"),
                    ("LI", "1111@",       "B2B2B2B2B2B2",       "73"),
                    ("LI", "11111",       "@2B2B2B2B2B2",       "73"),
                    ("LI", "11111",       "B2B2B2B2B2B@",       "73"),
                    ("LU", "111",         "B2B2B2B2B2B2B",      "27"),
                    ("LU", "11",          "B2B2B2B2B2B2B",      "27"),
                    ("LU", "X11",         "B2B2B2B2B2B2B",      "27"),
                    ("LU", "11@",         "B2B2B2B2B2B2B",      "27"),
                    ("LU", "111",         "@2B2B2B2B2B2B",      "27"),
                    ("LU", "111",         "B2B2B2B2B2B2@",      "27"),
                    ("LV", "AAAA",        "B2B2B2B2B2B2B",      "86"),
                    ("LV", "AAA",         "B2B2B2B2B2B2B",      "86"),
                    ("LV", "8AAA",        "B2B2B2B2B2B2B",      "86"),
                    ("LV", "AAA@",        "B2B2B2B2B2B2B",      "86"),
                    ("LV", "AAAA",        "@2B2B2B2B2B2B",      "86"),
                    ("LV", "AAAA",        "B2B2B2B2B2B2@",      "86"),
                    ("MC", "1111122222",  "C3C3C3C3C3C44",      "26"),
                    ("MC", "111112222",   "C3C3C3C3C3C44",      "26"),
                    ("MC", "X111122222",  "C3C3C3C3C3C44",      "26"),
                    ("MC", "1111@22222",  "C3C3C3C3C3C44",      "26"),
                    ("MC", "11111X2222",  "C3C3C3C3C3C44",      "26"),
                    ("MC", "111112222@",  "C3C3C3C3C3C44",      "26"),
                    ("MC", "1111122222",  "@3C3C3C3C3C44",      "26"),
                    ("MC", "1111122222",  "C3C3C3C3C3@44",      "26"),
                    ("MC", "1111122222",  "C3C3C3C3C3CX4",      "26"),
                    ("MC", "1111122222",  "C3C3C3C3C3C4@",      "26"),
                    ("NL", "AAAA",        "2222222222",         "57"),
                    ("NL", "AAA",         "2222222222",         "57"),
                    ("NL", "8AAA",        "2222222222",         "57"),
                    ("NL", "AAA@",        "2222222222",         "57"),
                    ("NL", "AAAA",        "X222222222",         "57"),
                    ("NL", "AAAA",        "222222222@",         "57"),
                    ("NO", "1111",        "2222223",            "40"),
                    ("NO", "111",         "2222223",            "40"),
                    ("NO", "X111",        "2222223",            "40"),
                    ("NO", "111@",        "2222223",            "40"),
                    ("NO", "1111",        "X222223",            "40"),
                    ("NO", "1111",        "22222@3",            "40"),
                    ("NO", "1111",        "222222X",            "40"),
                    ("PL", "11111111",    "B2B2B2B2B2B2B2B2",   "16"),
                    ("PL", "1111111",     "B2B2B2B2B2B2B2B2",   "16"),
                    ("PL", "X1111111",    "B2B2B2B2B2B2B2B2",   "16"),
                    ("PL", "1111111@",    "B2B2B2B2B2B2B2B2",   "16"),
                    ("PL", "11111111",    "@2B2B2B2B2B2B2B2",   "16"),
                    ("PL", "11111111",    "B2B2B2B2B2B2B2B@",   "16"),
                    ("PT", "11112222",    "3333333333344",      "59"),
                    ("PT", "1111222",     "3333333333344",      "59"),
                    ("PT", "X1112222",    "3333333333344",      "59"),
                    ("PT", "111@2222",    "3333333333344",      "59"),
                    ("PT", "1111X222",    "3333333333344",      "59"),
                    ("PT", "1111222@",    "3333333333344",      "59"),
                    ("PT", "11112222",    "X333333333344",      "59"),
                    ("PT", "11112222",    "3333333333@44",      "59"),
                    ("PT", "11112222",    "33333333333X4",      "59"),
                    ("PT", "11112222",    "333333333334@",      "59"),
                    ("SE", "111",         "22222222222222223",  "32"),
                    ("SE", "11",          "22222222222222223",  "32"),
                    ("SE", "X11",         "22222222222222223",  "32"),
                    ("SE", "11@",         "22222222222222223",  "32"),
                    ("SE", "111",         "X2222222222222223",  "32"),
                    ("SE", "111",         "222222222222222@3",  "32"),
                    ("SE", "111",         "2222222222222222X",  "32"),
                    ("SI", "11111",       "2222222233",         "92"),
                    ("SI", "1111",        "2222222233",         "92"),
                    ("SI", "X1111",       "2222222233",         "92"),
                    ("SI", "1111@",       "2222222233",         "92"),
                    ("SI", "11111",       "X222222233",         "92"),
                    ("SI", "11111",       "2222222@33",         "92"),
                    ("SI", "11111",       "22222222X3",         "92"),
                    ("SI", "11111",       "222222223@",         "92"),
                    ("SM", "A2222233333", "D4D4D4D4D4D4",       "71"),
                    ("SM", "A222223333",  "D4D4D4D4D4D4",       "71"),
                    ("SM", "82222233333", "D4D4D4D4D4D4",       "71"),
                    ("SM", "AX222233333", "D4D4D4D4D4D4",       "71"),
                    ("SM", "A2222@33333", "D4D4D4D4D4D4",       "71"),
                    ("SM", "A22222X3333", "D4D4D4D4D4D4",       "71"),
                    ("SM", "A222223333@", "D4D4D4D4D4D4",       "71"),
                    ("SM", "A2222233333", "@4D4D4D4D4D4",       "71"),
                    ("SM", "A2222233333", "D4D4D4D4D4D@",       "71"),
                    ("DE", "12345678",    "5",                  "06"))

# Main program (executed unless imported as module)
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        print_new_iban(sys.argv[1].upper(), sys.argv[2].upper(),
                       sys.argv[3].upper())
    elif len(sys.argv) == 2 and sys.argv[1][0] != "-":
        print_iban_parts(sys.argv[1].upper())
    elif "-f" in sys.argv[1:2]:
        print_format()
    elif "-e" in sys.argv[1:2]:
        print_examples()
    elif "-t" in sys.argv[1:2]:
        print_test()
    else:
        print usage

# -*- coding: utf-8 -*-

# Copyright (C) 2005-2015 by Promotux
# di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
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


# possibleFieldsKeys is a global module list containing all visible fields that is possible to import from a price list
from promogest import Environment
from promogest.lib.utils import posso

possibleFieldsKeys = ['Codice',
                      'Codice a barre',
                      'Codice articolo fornitore',
                      'Descrizione articolo',
                      'Aliquota iva',
                      'Famiglia',
                      'Categoria',
                      'Unita base',
                      'Produttore',
                      'Prezzo vendita ivato',
                      'Prezzo vendita NON ivato',
                      'Prezzo acquisto ivato',
                      'Prezzo acquisto NON ivato',
                      'Sconto Vendita Dettaglio',
                      'Sconto Vendita Ingrosso',
                      'Valore nullo']
if posso("PW"):
    possibleFieldsKeys.append("Gruppo Taglia")
    possibleFieldsKeys.append("Taglia")
    possibleFieldsKeys.append("Colore")
    possibleFieldsKeys.append("Anno")
    possibleFieldsKeys.append("Stagione")
    possibleFieldsKeys.append("Genere")
    possibleFieldsKeys.append("Modello")
    possibleFieldsKeys.append("Codice Padre")

# possibleFieldsValues is a global module list containing all real fields that is possible to import from a price list
possibleFieldsValues = ['codice_articolo',
                        'codice_barre_articolo',
                        'codice_fornitore',
                        'denominazione_articolo',
                        'aliquota_iva',
                        'famiglia_articolo',
                        'categoria_articolo',
                        'unita_base',
                        'produttore',
                        'prezzo_vendita_ivato',
                        'prezzo_vendita_non_ivato',
                        'prezzo_acquisto_ivato',
                        'prezzo_acquisto_non_ivato',
                        'sconto_vendita_dettaglio',
                        'sconto_vendita_ingrosso',
                        'chiave_nulla_']
if posso("PW"):
    possibleFieldsValues.append("gruppo_taglia")
    possibleFieldsValues.append("taglia")
    possibleFieldsValues.append("colore")
    possibleFieldsValues.append("anno")
    possibleFieldsValues.append("stagione")
    possibleFieldsValues.append("genere")
    possibleFieldsValues.append("modello")
    possibleFieldsValues.append("codice_padre")
# possibleFieldsDict is a global module dictionary containing all fields that is possible to import from a price list
possibleFieldsDict = dict(zip(possibleFieldsKeys, possibleFieldsValues))

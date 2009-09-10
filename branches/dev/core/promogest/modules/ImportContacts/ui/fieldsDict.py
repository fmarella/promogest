# -*- coding: UTF-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

# possibleFieldsKeys is a global module list containing all visible fields that is possible to import from a price list
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
# possibleFieldsDict is a global module dictionary containing all fields that is possible to import from a price list
possibleFieldsDict = dict(zip(possibleFieldsKeys, possibleFieldsValues))
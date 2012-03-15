# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#       di Francesco Meloni snc - http://www.promotux.it/

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
from decimal import Decimal
from promogest import Environment
from promogest.ui.utils import messageError, mN, leggiArticolo


def tracciati_disponibili():
    ''' Ritorna una lista con i nomi dei tracciati disponibili '''
    return [tracciato[:-4] for tracciato in os.listdir(Environment.tracciatiDir) if tracciato.endswith('.xml')]

def dati_file_conad_terron(testata):
    pass

def dati_file_conad(testata):
    """
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento
    from promogest.dao.Azienda import Azienda
    if testata:
        #Scriviamo la testata della fattura
        dati_differita = InformazioniFatturazioneDocumento().select(id_fattura=testata.id, batchSize=None)
        azienda = Azienda().getRecord(id=Environment.azienda)
        if not azienda:
            messageError('Inserire le informazioni sull\' azienda in Dati azienda')
            return None

        if azienda.ragione_sociale == '':
            messageError('Inserire la ragione sociale dell\'azienda in Dati azienda')
            return None

        codice_fornitore = ''
        if azienda.matricola_inps:
            codice_fornitore = azienda.matricola_inps
        else:
            messageError("Inserire il codice fornitore nel campo \'matricola_inps\' in Dati azienda")
            return None

        dati2 = []

        if dati_differita:

            for ddtt in dati_differita:
                ddt = TestataDocumento().getRecord(id=ddtt.id_ddt)

                codice = 0
                if ddt.DM is not None:
                    codice = ddt.DM.codice

                dati = {'testata': {
                    'numero_progressivo': str(dati_differita.index(ddtt) + 1),
                    'codice_cliente': str(ddt.ragione_sociale_cliente),
                    'data_bolla':  ddt.data_documento,
                    'numero_bolla': str(ddt.numero),
                    'codice_fornitore': codice_fornitore,
                    'data_fattura': testata.data_documento,
                    'numero_fattura': str(testata.numero),
                    'codice_cooperativa': str(codice),
                    'codice_socio': str(codice),
                },
                'dettaglio': []
                }
                for riga in ddt.righe:
                    if riga.id_articolo:
                        art = leggiArticolo(riga.id_articolo)
                        dati['dettaglio'].append(
                            {
                                'numero_progressivo':str(dati_differita.index(ddtt) + 1),
                                'codice_articolo': str(art["codice"]),
                                'descrizione': str(art["denominazione"].replace("à", "a")),
                                'unita_misura': str(art["unitaBase"]).upper(),
                                'qta_fatturata': str(mN(Decimal(riga.quantita * (riga.moltiplicatore or 1)), 2)),
                                'prezzo_unitario': str(mN(Decimal(riga.valore_unitario_netto), 3)),
                                'importo_totale': str(mN(Decimal(riga.quantita or 0) * Decimal(riga.moltiplicatore or 1) * Decimal(riga.valore_unitario_netto or 0), 3)),
                                'aliquota_iva': str(mN(riga.percentuale_iva,0))
                            })
                dati2.append(dati)
            return dati2

def dati_file_buffetti(testata):
    """
    """
    #from promogest.dao.TestataDocumento import TestataDocumento
    from promogest.dao.Azienda import Azienda
    if testata:
        azienda = Azienda().getRecord(id=Environment.azienda)
        if not azienda:
            messageError('nessuna informazione azienda')
            return None

        if azienda.ragione_sociale == '':
            messageError('nessuna ragione sociale impostata')
            return None

        scadenze = testata.scadenze
        dati_generazione_scadenze = 'S'
        if len(scadenze) == 0:
            dati_generazione_scadenze = 'N'

        if testata.operazione == 'Fattura Accompagnatoria':
            tipo_documento = 'A'
        elif 'Fattura Differita' in testata.operazione:
            tipo_documento = 'D'
        elif 'Fattura' in testata.operazione:
            tipo_documento = 'F'

        tipo_registro = 'F'

        totale_fattura = mN(testata._totaleScontato + testata._totaleSpese, 2)

        if testata.id_fornitore is not None:
            tipo_nominativo = 'F'
            cognome_cli_for = testata.cognome_fornitore or ''
            nome_cli_for = testata.nome_fornitore or ''
            codice_fiscale_cli_for = testata.codice_fiscale_fornitore
            partita_iva_cli_for = testata.partita_iva_fornitore
            indirizzo_cli_for = testata.indirizzo_fornitore
            localita_cli_for = testata.localita_fornitore
            cap_cli_for = testata.cap_fornitore
            provincia_cli_for = testata.provincia_fornitore
            codice_cli_for = testata.codice_fornitore
        elif testata.id_cliente is not None:
            tipo_nominativo = 'C'
            cognome_cli_for = testata.cognome_cliente or ''
            nome_cli_for = testata.nome_cliente or ''
            codice_fiscale_cli_for = testata.codice_fiscale_cliente
            partita_iva_cli_for = testata.partita_iva_cliente
            indirizzo_cli_for = testata.indirizzo_cliente
            localita_cli_for = testata.localita_cliente
            cap_cli_for = testata.cap_cliente
            provincia_cli_for = testata.provincia_cliente
            codice_cli_for = testata.codice_cliente

        dati = [{
            'testata': {
                'ragione_sociale_ditta': azienda.ragione_sociale,
                'cod_fisc_piva_ditta': azienda.codice_fiscale or azienda.partita_iva,
                'dati_generazione_scadenze': dati_generazione_scadenze,
                'tipo_piano': '2',
                'da_data': testata.data_documento,
                'a_data': testata.data_documento,
                'no_data': ''
            },
            'scadenze':{},
            'testata_pagamento': [{
                'codice': '0', #inseire il codice con cui identifichiamo il tipo di pagamento (es. ID RIba 30 gg)
                'numero_rate': str(len(scadenze)),
                'descrizione': testata.pagamento,
                'tipo': '1',
                'determinazione_tipo': '31',
                'numero_rate': '1',
                'giorni_prima': '30' # recuperare il numero di giorni dal pagamento
            }],
            'fine_scadenza': {},
            'record0': [{
                'tipo_nominativo': tipo_nominativo,
                'cognome': cognome_cli_for,
                'nome': nome_cli_for,
                'codice_fiscale': codice_fiscale_cli_for,
                'partita_iva': partita_iva_cli_for,
                'indirizzo': indirizzo_cli_for,
                'localita': localita_cli_for,
                'cap': cap_cli_for,
                'provincia': provincia_cli_for,
                'incluso_elenchi_bl': 'N'
            }],
            'record1': [{
                'tipo_documento': tipo_documento,
                'totale_fattura': str(totale_fattura),
                'cf_piva': codice_fiscale_cli_for or partita_iva_cli_for,
                'codice': codice_cli_for,
                'tipo_registro': tipo_registro,
                'data_doc': testata.data_documento
            }],
            'record2': [{
                'imponibile_iva': str(mN(testata._totaleImponibileScontato)),
                'importo_iva': str(mN(testata._totaleImpostaScontata)),
            }],
            'recordB': [{
                'posizione': 'A' # controllare scadenze.data_pagamento se None mettere A, altrimenti P (pagato)
            }],
        }]

        # for scadenza in testata.scadenze:
            # dati['dettaglio_rate'].append({
                # 'numero_rata': testata.scadenze.index(scadenza) + 1
            # })

        return dati

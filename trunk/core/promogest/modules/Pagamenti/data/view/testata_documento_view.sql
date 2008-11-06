--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Alessandro Scano <alessandro@promotux.it>
--
-- This program is free software; you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation; either version 2
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

Testata Documento  - Vista

*/


DROP VIEW v_testata_documento;

CREATE OR REPLACE VIEW v_testata_documento AS
    SELECT 
         TD.id
        ,TD.numero
        ,TD.parte
        ,TD.registro_numerazione
        ,TD.operazione
        ,TD.data_documento
        ,TD.data_inserimento
        ,TD.protocollo
        ,TD.note_interne
        ,TD.note_pie_pagina
        ,TD.causale_trasporto
        ,TD.aspetto_esteriore_beni
        ,TD.inizio_trasporto
        ,TD.fine_trasporto
        ,TD.incaricato_trasporto
        ,TD.totale_colli
        ,TD.totale_peso
        ,TD.applicazione_sconti
        ,TD.id_cliente
        ,TD.id_fornitore
        ,TD.id_destinazione_merce
        ,TD.id_pagamento
        ,TD.id_banca
        ,TD.id_aliquota_iva_esenzione
        ,TD.id_vettore
        ,TD.id_agente
        ,TD.porto
        ,ICD.documento_saldato
        ,ICD.totale_pagato
        ,ICD.totale_sospeso
        ,ICD.id_primo_riferimento
        ,ICD.id_secondo_riferimento
        ,TD.costo_da_ripartire
        ,TD.ripartire_importo
    FROM testata_documento TD
    LEFT OUTER JOIN informazioni_contabili_documento ICD ON TD.id = ICD.id_documento;


DROP VIEW v_testata_documento_completa;

CREATE OR REPLACE VIEW v_testata_documento_completa AS
    SELECT 
         TD.id
        ,TD.numero
        ,TD.parte
        ,TD.registro_numerazione
        ,TD.operazione
        ,TD.data_documento
        ,TD.data_inserimento
        ,TD.protocollo
        ,TD.note_interne
        ,TD.note_pie_pagina
        ,TD.causale_trasporto
        ,TD.aspetto_esteriore_beni
        ,TD.inizio_trasporto
        ,TD.fine_trasporto
        ,TD.incaricato_trasporto
        ,TD.totale_colli
        ,TD.totale_peso
        ,TD.applicazione_sconti
        ,TD.id_cliente
        ,TD.id_fornitore
        ,TD.id_destinazione_merce
        ,TD.id_pagamento
        ,TD.id_banca
        ,TD.id_aliquota_iva_esenzione
        ,TD.id_vettore
        ,TD.id_agente
        ,TD.porto
        ,ICD.documento_saldato
        ,ICD.totale_pagato
        ,ICD.totale_sospeso
        ,ICD.id_primo_riferimento
        ,ICD.id_secondo_riferimento
        ,TD.costo_da_ripartire
        ,TD.ripartire_importo
        ,PC.ragione_sociale AS ragione_sociale_cliente
        ,PC.cognome AS cognome_cliente
        ,PC.nome AS nome_cliente
        ,PC.sede_legale_indirizzo AS indirizzo_cliente
        ,PC.sede_legale_localita AS localita_cliente
        ,PC.sede_legale_cap AS cap_cliente
        ,PC.sede_legale_provincia AS provincia_cliente
        ,PC.codice_fiscale AS codice_fiscale_cliente
        ,PC.partita_iva AS partita_iva_cliente
        ,PF.ragione_sociale AS ragione_sociale_fornitore
        ,PF.cognome AS cognome_fornitore
        ,PF.nome AS nome_fornitore
        ,PF.sede_legale_indirizzo AS indirizzo_fornitore
        ,PF.sede_legale_localita AS localita_fornitore
        ,PF.sede_legale_cap AS cap_fornitore
        ,PF.sede_legale_provincia AS provincia_fornitore
        ,PF.codice_fiscale AS codice_fiscale_fornitore
        ,PF.partita_iva AS partita_iva_fornitore
        ,DM.denominazione AS destinazione_merce
        ,DM.indirizzo AS indirizzo_destinazione_merce
        ,DM.localita AS localita_destinazione_merce
        ,DM.cap AS cap_destinazione_merce
        ,DM.provincia AS provincia_destinazione_merce
        ,PG.denominazione AS pagamento
        ,BN.denominazione AS banca
        ,BN.agenzia AS agenzia
        ,BN.iban AS iban
        ,AL.denominazione AS aliquota_iva_esenzione
        ,PV.ragione_sociale AS ragione_sociale_vettore
        ,PA.ragione_sociale AS ragione_sociale_agente
    FROM testata_documento TD
    LEFT OUTER JOIN persona_giuridica PC ON TD.id_cliente = PC.id
    LEFT OUTER JOIN persona_giuridica PF ON TD.id_fornitore = PF.id
    LEFT OUTER JOIN destinazione_merce DM ON TD.id_destinazione_merce = DM.id
    LEFT OUTER JOIN pagamento PG ON TD.id_pagamento = PG.id
    LEFT OUTER JOIN banca BN ON TD.id_banca = BN.id
    LEFT OUTER JOIN aliquota_iva  AL ON TD.id_aliquota_iva_esenzione = AL.id
    LEFT OUTER JOIN persona_giuridica PV ON TD.id_vettore = PV.id
    LEFT OUTER JOIN persona_giuridica PA ON TD.id_agente = PA.id
    LEFT OUTER JOIN informazioni_contabili_documento ICD ON TD.id = ICD.id_documento;

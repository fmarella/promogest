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

Informazioni contabili documento - Vista
*/


DROP VIEW v_informazioni_contabili_documento;

CREATE OR REPLACE VIEW v_informazioni_contabili_documento AS
    SELECT 
        MP.id
        ,MP.documento_saldato
        ,MP.id_documento
        ,MP.id_primo_riferimento
        ,MP.id_secondo_riferimento
        ,MP.totale_pagato
        ,MP.totale_sospeso
        FROM informazioni_contabili_documento MP;

DROP VIEW v_informazioni_contabili_documento_completa;

CREATE OR REPLACE VIEW v_informazioni_contabili_documento_completa AS
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

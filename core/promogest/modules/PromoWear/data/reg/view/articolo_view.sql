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

Articolo  - Vista

*/

DROP VIEW v_articolo;

CREATE OR REPLACE VIEW v_articolo AS
    SELECT  
         A.id
        ,A.codice
        ,A.denominazione
        ,A.id_aliquota_iva
        ,A.id_famiglia_articolo
        ,A.id_categoria_articolo
        ,A.id_unita_base
        ,A.produttore
        ,A.unita_dimensioni
        ,A.lunghezza 
        ,A.larghezza
        ,A.altezza 
        ,A.unita_volume
        ,A.volume
        ,A.unita_peso
        ,A.peso_lordo
        ,A.id_imballaggio
        ,A.peso_imballaggio
        ,A.stampa_etichetta
        ,A.codice_etichetta
        ,A.descrizione_etichetta
        ,A.stampa_listino
        ,A.descrizione_listino
        ,A.aggiornamento_listino_auto
        ,A.timestamp_variazione
        ,A.note
        ,A.cancellato
        ,A.sospeso
        ,A.id_stato_articolo
        ,CB.codice AS codice_a_barre
        ,F.codice_articolo_fornitore AS codice_articolo_fornitore
    FROM articolo A
    LEFT OUTER JOIN codice_a_barre_articolo CB ON A.id = CB.id_articolo AND CB.primario
    LEFT OUTER JOIN fornitura F ON A.id = F.id_articolo AND F.fornitore_preferenziale;


DROP VIEW v_articolo_completa;

CREATE OR REPLACE VIEW v_articolo_completa AS
    SELECT  
         A.id
        ,A.codice
        ,A.denominazione
        ,A.id_aliquota_iva
        ,A.id_famiglia_articolo
        ,A.id_categoria_articolo
        ,A.id_unita_base
        ,A.produttore
        ,A.unita_dimensioni
        ,A.lunghezza 
        ,A.larghezza
        ,A.altezza 
        ,A.unita_volume
        ,A.volume
        ,A.unita_peso
        ,A.peso_lordo
        ,A.id_imballaggio
        ,A.peso_imballaggio
        ,A.stampa_etichetta
        ,A.codice_etichetta
        ,A.descrizione_etichetta
        ,A.stampa_listino
        ,A.descrizione_listino
        ,A.aggiornamento_listino_auto
        ,A.timestamp_variazione
        ,A.note
        ,A.cancellato
        ,A.sospeso
        ,A.id_stato_articolo
        ,AI.denominazione_breve AS denominazione_breve_aliquota_iva
        ,AI.denominazione AS denominazione_aliquota_iva
        ,AI.percentuale AS percentuale_aliquota_iva
        ,FA.denominazione_breve AS denominazione_breve_famiglia
        ,FA.denominazione AS denominazione_famiglia
        ,CA.denominazione_breve AS denominazione_breve_categoria
        ,CA.denominazione AS denominazione_categoria
        ,UB.denominazione_breve AS denominazione_breve_unita_base
        ,UB.denominazione AS denominazione_unita_base
        ,I.denominazione AS imballaggio
        ,SA.denominazione  AS stato_articolo
        ,CB.codice AS codice_a_barre
        ,F.codice_articolo_fornitore AS codice_articolo_fornitore
        ,ATC.id_articolo_padre AS id_articolo_padre_taglia_colore
        ,ATC.id_gruppo_taglia
        ,ATC.id_taglia
        ,ATC.id_colore
        ,ATC.id_anno
        ,ATC.id_stagione
        ,ATC.id_genere
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,AAB.denominazione AS anno
        ,SAB.denominazione AS stagione
        ,GAB.denominazione AS genere
    FROM articolo A
    LEFT OUTER JOIN aliquota_iva AI ON A.id_aliquota_iva = AI.id
    LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id
    LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id
    LEFT OUTER JOIN promogest.unita_base UB ON A.id_unita_base = UB.id
    LEFT OUTER JOIN imballaggio I ON A.id_imballaggio = I.id
    LEFT OUTER JOIN promogest.stato_articolo SA ON A.id_stato_articolo = SA.id
    LEFT OUTER JOIN codice_a_barre_articolo CB ON A.id = CB.id_articolo AND CB.primario
    LEFT OUTER JOIN fornitura F ON A.id = F.id_articolo AND F.fornitore_preferenziale
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id 
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id 
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id;

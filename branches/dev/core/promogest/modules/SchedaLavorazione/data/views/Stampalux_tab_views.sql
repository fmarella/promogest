--
-- Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
-- Author: Dr astico (Marco Pinna) <zoccolodignu@gmail.com>
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

Schede ordinazione  - Vista

*/

DROP VIEW v_riga_scheda ;
DROP VIEW v_riga_scheda_completa ;
DROP VIEW v_elemento_associazione_articoli ;
DROP VIEW v_sconto_scheda_ordinazione ;
DROP VIEW v_nodo_associazione_articoli ;
DROP VIEW v_scheda_ordinazione ;
DROP VIEW v_scheda_ordinazione_completa ;
DROP VIEW v_sconto_riga_scheda ;
DROP VIEW v_promemoria_scheda ;


-- View: "v_scheda_ordinazione"

CREATE OR REPLACE VIEW v_scheda_ordinazione AS 
SELECT so.id, 
    so.numero,

    nt.note_text, 
    nt.note_fornitore, 
    nt.note_final, 
    nt.note_spedizione, 
    so.mezzo_ordinazione, 
    so.mezzo_spedizione, 
    so.disp_materiale, 
    so.id_colore_stampa, 
    so.id_carattere_stampa, 
    so.bomba_in_cliche, 
    so.codice_spedizione,
    so.operatore, 
    so.nomi_sposi, 
    so.provenienza, 
    cs.referente AS nome_contatto, 
    cs.prima_email, 
    cs.seconda_email, 
    cs.telefono, 
    cs.cellulare, 
    cs.skype, 
    rs.referente, 
    rs.presso, 
    rs.via_piazza, 
    rs.num_civ, 
    rs.zip, 
    rs.localita, 
    rs.provincia, 
    rs.stato, 
    dt.matrimonio AS data_matrimonio, 
    dt.presa_in_carico AS data_presa_in_carico, 
    dt.ordine_al_fornitore AS data_ordine_al_fornitore, 
    dt.consegna_bozza AS data_consenga_bozza, 
    dt.spedizione AS data_spedizione, 
    dt.consegna AS data_consegna, 
    dt.ricevuta AS data_ricevuta, 
    so.ricevuta_associata, 
    so.applicazione_sconti, 
    so.documento_saldato, 
    so.fattura, 
    so.totale_lordo, 
    so.userid_cliente, 
    so.passwd_cliente,
    so.lui_e_lei,
    so.id_cliente,
    so.id_magazzino,
    co.denominazione AS colore_stampa, 
    ca.denominazione AS carattere_stampa
   FROM schede_ordinazioni so
   LEFT JOIN note_schede nt ON so.id = nt.id_scheda
   LEFT JOIN datari dt ON so.id = dt.id_scheda
   LEFT JOIN contatti_schede cs ON so.id = cs.id_scheda
   LEFT JOIN recapiti_spedizioni rs ON so.id = rs.id_scheda
   LEFT JOIN colori_stampa co ON co.id = so.id_colore_stampa
   LEFT JOIN caratteri_stampa ca ON ca.id = so.id_carattere_stampa;



CREATE OR REPLACE VIEW v_scheda_ordinazione_completa AS 
 SELECT so.id, 
    so.numero,
    nt.note_text, 
    nt.note_fornitore, 
    nt.note_final, 
    nt.note_spedizione, 
    so.mezzo_ordinazione, 
    so.mezzo_spedizione, 
    so.disp_materiale, 
    so.id_colore_stampa, 
    so.id_carattere_stampa, 
    so.bomba_in_cliche, 
    so.codice_spedizione,
    so.operatore, 
    so.nomi_sposi, 
    so.provenienza, 
    cs.referente AS nome_contatto, 
    cs.prima_email, 
    cs.seconda_email, 
    cs.telefono, 
    cs.cellulare, 
    cs.skype, 
    rs.referente, 
    rs.presso, 
    rs.via_piazza, 
    rs.num_civ, 
    rs.zip, 
    rs.localita, 
    rs.provincia, 
    rs.stato, 
    dt.matrimonio AS data_matrimonio, 
    dt.presa_in_carico AS data_presa_in_carico, 
    dt.ordine_al_fornitore AS data_ordine_al_fornitore, 
    dt.consegna_bozza AS data_consenga_bozza, 
    dt.spedizione AS data_spedizione, 
    dt.consegna AS data_consegna, 
    dt.ricevuta AS data_ricevuta, 
    so.ricevuta_associata, 
    so.applicazione_sconti, 
    so.documento_saldato, 
    so.fattura,
    so.totale_lordo,
    so.userid_cliente,
    so.passwd_cliente,
    so.lui_e_lei
    so.id_cliente,
    so.id_magazzino,
    co.denominazione AS colore_stampa, 
    ca.denominazione AS carattere_stampa
   FROM schede_ordinazioni so
   LEFT JOIN note_schede nt ON so.id = nt.id_scheda
   LEFT JOIN datari dt ON so.id = dt.id_scheda
   LEFT JOIN contatti_schede cs ON so.id = cs.id_scheda
   LEFT JOIN recapiti_spedizioni rs ON so.id = rs.id_scheda
   LEFT JOIN colori_stampa co ON co.id = so.id_colore_stampa
   LEFT JOIN caratteri_stampa ca ON ca.id = so.id_carattere_stampa;


CREATE OR REPLACE VIEW v_sconto_scheda_ordinazione AS
    SELECT 
         S.id
        ,S.valore
        ,S.tipo_sconto
        ,SO.id_scheda_ordinazione
    FROM sconto S
    INNER JOIN sconti_schede_ordinazioni SO ON S.id = SO.id;

CREATE OR REPLACE VIEW v_nodo_associazione_articoli AS
    SELECT DISTINCT ON (AA.id_padre)
         AA.id
        ,AA.id_figlio AS id_associato
        ,A.id as id_articolo 
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
    FROM associazioni_articoli AA
    LEFT OUTER JOIN articolo A on AA.id_padre = A.id
    LEFT OUTER JOIN aliquota_iva AI ON A.id_aliquota_iva = AI.id
    LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id
    LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id
    LEFT OUTER JOIN promogest.unita_base UB ON A.id_unita_base = UB.id
    LEFT OUTER JOIN imballaggio I ON A.id_imballaggio = I.id
    LEFT OUTER JOIN promogest.stato_articolo SA ON A.id_stato_articolo = SA.id
    LEFT OUTER JOIN codice_a_barre_articolo CB ON A.id = CB.id_articolo AND CB.primario
    LEFT OUTER JOIN fornitura F ON A.id = F.id_articolo AND F.fornitore_preferenziale;


CREATE OR REPLACE VIEW v_elemento_associazione_articoli AS
    SELECT 
         AA.id
        ,AA.id_padre AS id_associato
        ,AA.posizione
        ,A.id as id_articolo 
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
    FROM associazioni_articoli AA
    LEFT OUTER JOIN articolo A on AA.id_figlio = A.id
    LEFT OUTER JOIN aliquota_iva AI ON A.id_aliquota_iva = AI.id
    LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id
    LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id
    LEFT OUTER JOIN promogest.unita_base UB ON A.id_unita_base = UB.id
    LEFT OUTER JOIN imballaggio I ON A.id_imballaggio = I.id
    LEFT OUTER JOIN promogest.stato_articolo SA ON A.id_stato_articolo = SA.id
    LEFT OUTER JOIN codice_a_barre_articolo CB ON A.id = CB.id_articolo AND CB.primario
    LEFT OUTER JOIN fornitura F ON A.id = F.id_articolo AND F.fornitore_preferenziale;

CREATE OR REPLACE VIEW v_sconto_riga_scheda AS
    SELECT 
         S.id
        ,S.valore
        ,S.tipo_sconto
        ,SD.id_riga_scheda
    FROM sconto S
    INNER JOIN sconti_righe_schede SD ON S.id = SD.id;

CREATE OR REPLACE VIEW v_riga_scheda AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,A.codice AS codice_articolo
        ,RS.id_scheda
        ,CAST('scheda' AS text) AS tipo_riga
    FROM riga R
    INNER JOIN righe_schede_ordinazioni RS ON RS.id = R.id
    LEFT OUTER JOIN articolo A ON R.id_articolo = A.id;

CREATE OR REPLACE VIEW v_riga_scheda_completa AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,RS.id_scheda
        ,L.denominazione AS listino
        ,M.denominazione AS magazzino
        ,MU.denominazione_breve AS multiplo
        ,A.codice AS codice_articolo
        ,U.denominazione_breve AS unita_base
        ,CAST('scheda' AS text) AS tipo_riga
    FROM riga R
    INNER JOIN righe_schede_ordinazioni RS ON RS.id = R.id
    LEFT OUTER JOIN listino L ON R.id_listino = L.id
    LEFT OUTER JOIN magazzino M ON R.id_magazzino = M.id
    LEFT OUTER JOIN multiplo MU ON R.id_multiplo = MU.id
    LEFT OUTER JOIN articolo A ON R.id_articolo = A.id
    LEFT OUTER JOIN promogest.unita_base U ON A.id_unita_base = U.id;


/*

Promemoria schede ordinazioni - vista tabella promemoria_schede

*/
CREATE OR REPLACE VIEW v_promemoria_scheda AS
    SELECT P.*,
        PS.id_scheda
        FROM promemoria P
        LEFT OUTER JOIN promemoria_schede_ordinazioni PS ON P.id = PS.id;


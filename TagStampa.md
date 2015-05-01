# Introduction #
Elenco dei TAG per la stampa:
**TAG SPECIALI**
I tag speciali sono tag che vengono usati quasi sempre in abbinamento con i **TAG NORMALI**  cioè quelli contenenti i dati reali.
I TAG SPECIALI si suddividono in **FORMATO**, **TEMPORALI** , **POSIZIONAMENTO**, **PAGINE** ed andremo adesso a vederli nel dettaglio


# Details #

## TAG FORMATO: ##
  * **trunc:** Il TAG trunc si usa per troncare delle parole o frasi troppo lunghe.
    * Sintassi: _`[[trunc(tagnormale,lunghezzastringa)]]`_
    * Esempio: _`[[trunc(operazione,10)]]`renderà la stringa finale lunga al massimo 10 caratteri_

  * **approx:** Il TAG approx si usa per approssimare dei numeri che hanno molti/troppi decimali dopo la virgola.
    * Sintassi: _`[[tagnormale,approssimazione)]]`_.
    * Esempio: _`[[approx(_totaleScontato,2)]]`_ renderà il numero finale con un massimo di due decimali

  * **itformat:** Il TAG itformat si usa italianizzare una data nel formato gg/mm/aa
    * Sintassi: _`[[iformat(tagnormale)]]`_.
    * Esempio: _`[[itformat(data_documento)]]`_ renderà il dato nel formato 05/06/2011

  * **itformatdataora:** Il TAG itformatdataora si usa italianizzare una data nel formato gg/mm/aa hh:mm:ss
    * Sintassi: _`[[itformatdataora(tagnormale)]]`_.
    * Esempio: _`[[itformatdataora(data_documento)]]`_ renderà il dato nel formato 05/06/2011 11:45:23

  * **itformatdata:** Il TAG itformatdata si usa italianizzare una data nel formato gg/mm/aa quando il dato in origina avrebbe anche l'orario. Tronca quindi la parte dell'orario.
    * Sintassi: _`[[iformatdata(tagnormale)]]`_.
    * Esempio: _`[[itaformatdata(data_documento)]]`_ renderà il dato nel formato 05/06/2011

  * **bcview:** Il TAG bicview si usa per creare l'immagine del codice a barre in una label o in una scheda articolo o anche eventualmente in una riga documento.
    * Sintassi: _`[[bcview(codice_a_barre,altezzaXlarghezza)]]`_.
    * Esempio: _`[[bcview(codice_a_barre,1X2)]]`_  creerà un codice a barre alto un centimetro e largo due

  * **approxit:** Il TAG approxit si comporta come approx ma modifica il formato finale mettendo la virgola per i decimali e il punto come separatore migliaia ed il simbolo di valuta ( €) .
    * Sintassi: _`[[approxit(tagnormale,approssimazione)]]`_.
    * Esempio: _`[[approxit(_totaleScontato,2)]]`_ renderà il numero finale con un massimo di due decimali,  € 1.234,80

## TAG TEMPORALI: ##

  * **date:** Il TAG inserirà nel pdf la data.
    * Sintassi: _`[[date]]`_
    * Esempio: _`[[date]]`_ scriverà 05/06/02011

  * **time:** Il TAG inserirà nel pdf l'ora.
    * Sintassi: _`[[time]]`_
    * Esempio: _`[[time]]`_ scriverà 18:34:55

  * **datetime:** Il TAG inserirà nel pdf data e ora
    * Sintassi: _`[[datetime]]`_
    * Esempio: _`[[datetime]]`_ scriverà 18:34:55 18:45:33

## TAG POSIZIONAMENTO: ##

  * **first:** Il TAG forzerà la visualizzazione del dato nella SOLA PRIMA PAGINA quando il documento è formato da più pagine
    * Sintassi: _`[[first(tagnormale)]]`_
    * Esempio: _`[[first:approxit(_totaleScontato,2)]]`_ inserirà il totale SOLO nella prima pagina

  * **last:** Il TAG forzerà la visualizzazione del dato nella SOLA ULTIMA PAGINA quando il documento è formato da più pagine
    * Sintassi: _`[[last(tagnormale)]]`_
    * Esempio: _`[[last:approxit(_totaleScontato,2)]]`_ inserirà il totale SOLO nell'ultima pagina


## TAG PAGINE: ##
currentPage

  * **currentPage:** Il TAG inserirà il numero di pagina corrente
    * Sintassi: _`[[currentPage]]`_
    * Esempio: _`[[currentPage]]`_  inserirà 1 se è la prima pagina

  * **totalPage:** Il TAG inserirà il numero di pagina totale del documento pdf
    * Sintassi: _`[[totalPage]]`_
    * Esempio: _`[[totalPage]]`_  uso comune è : _`[[currentPage]]` di `[[totalPage]]`inserirà  2/5_

### TAG AZIENDA ###

Questi tag vengono aggiunti per poter gestire le informazioni relative all'azienda nel templates documento.sla o simili

  * **`[[azi_abi]]`**
  * **`[[azi_cab]]`**
  * **`[[azi_cin]]`**
  * **`[[azi_codice_fiscale]]`**
  * **`[[azi_codice_rea]]`**
  * **`[[azi_denominazione]]`**
  * **`[[azi_iban]]`**
  * **`[[azi_iscrizione_cciaa_data]]`**
  * **`[[azi_iscrizione_cciaa_numero]]`**
  * **`[[azi_iscrizione_tribunale_data]]`**
  * **`[[azi_iscrizione_tribunale_numero]]`**
  * **`[[azi_matricola_inps]]`**
  * **`[[azi_numero_conto]]`**
  * **`[[azi_partita_iva]]`**
  * **`[[azi_percorso_immagine]]`**
  * **`[[azi_ragione_sociale]]`**
  * **`[[azi_sede_legale_cap]]`**
  * **`[[azi_sede_legale_indirizzo]]`**
  * **`[[azi_sede_legale_localita]]`**
  * **`[[azi_sede_legale_numero]]`**
  * **`[[azi_sede_legale_provincia]]`**
  * **`[[azi_sede_operativa_cap]]`**
  * **`[[azi_sede_operativa_indirizzo]]`**
  * **`[[azi_sede_operativa_localita]]`**
  * **`[[azi_sede_operativa_numero]]`**
  * **`[[azi_sede_operativa_provincia]]`**

### TAG DOCUMENTO: ###
  * **`[[_totaleImponibile]]`** Restituisce il totale imponibile
  * **`[[_totaleImponibileScontato]]`** Restituisce il totale imponibile scontato
  * **`[[_totaleImposta]]`** Restituisce il totale finale dell'imposta
  * **`[[_totaleImpostaScontata]]`** Restituisce il totale dell'imposta dopo eventuali sconti
  * **`[[_totaleNonBaseImponibile]]`** Restituisce il totale di una eventuale cifra non imponibile
  * **`[[_totaleNonScontato]]`** Restituisce il totale finale documento prima di eventuali sconti
  * **`[[_totaleScontato]]`** Restituisce il totale finale documento
  * **`[[agenzia]]`** Agenzia della banca assegnata in appoggio
  * **`[[aliquota_iva_esenzione]]`** Eventuali aliquota iva in esenzione nel documento
  * **`[[applicazione_sconti]]`** Tipoligia di sconti applicata ( scalare o nonscalare )
  * **`[[aspetto_esteriore_beni]]`** Aspetto esteriore beni
  * **`[[banca]]`** Stringa relativa alla decrizione banca
  * **`[[cap_cliente]]`** Il cap del cliente
  * **`[[cap_cliente_operativa]]`** Il cap del cliente della eventuale sede operativa
  * **`[[codice_cliente]]`**
  * **`[[codice_fornitore]]`**
  * **`[[cap_destinazione_merce]]`**
  * **`[[cap_fornitore]]`**
  * **`[[cap_fornitore_operativa]]`**
  * **`[[causale_trasporto]]`**
  * **`[[codice_fiscale_cliente]]`**
  * **`[[codice_fiscale_fornitore]]`**
  * **`[[cognome_cliente]]`**
  * **`[[cognome_fornitore]]`**
  * **`[[data_documento]]`**
  * **`[[data_inserimento]]`**
  * **`[[destinazione_merce]]`**
  * **`[[documento_saldato]]`**
  * **`[[fine_trasporto]]`**
  * **`[[iban]]`**
  * **`[[abi]]`**
  * **`[[cab]]`**
  * **`[[incaricato_trasporto]]`**
  * **`[[indirizzo_cliente]]`**
  * **`[[indirizzo_cliente_operativa]]`**
  * **`[[indirizzo_destinazione_merce]]`**
  * **`[[indirizzo_fornitore]]`**
  * **`[[indirizzo_fornitore_operativa]]`**
  * **`[[inizio_trasporto]]`**
  * **`[[insegna_cliente]]`**
  * **`[[insegna_fornitore]]`**
  * **`[[intestatario]]`**
  * **`[[localita_cliente]]`**
  * **`[[localita_cliente_operativa]]`**
  * **`[[localita_destinazione_merce]]`**
  * **`[[localita_fornitore]]`**
  * **`[[localita_fornitore_operativa]]`**
  * **`[[nome_cliente]]`**
  * **`[[nome_fornitore]]`**
  * **`[[note_interne]]`**
  * **`[[note_pie_pagina]]`**
  * **`[[numero]]`**
  * **`[[operazione]]`**
  * **`[[pagamento]]`** Rdvf/B.b. 60 gg. F.M.
  * **`[[pagamento_tipo]]`** banca
  * **`[[partita_iva_cliente]]`**
  * **`[[partita_iva_fornitore]]`**
  * **`[[porto]]`**
  * **`[[protocollo]]`**
  * **`[[provincia_cliente]]`**
  * **`[[provincia_cliente_operativa]]`**
  * **`[[provincia_destinazione_merce]]`**
  * **`[[provincia_fornitore]]`**
  * **`[[provincia_fornitore_operativa]]`**
  * **`[[ragione_sociale_agente]]`**
  * **`[[ragione_sociale_cliente]]`**
  * **`[[ragione_sociale_fornitore]]`**
  * **`[[ragione_sociale_vettore]]`**
  * **`[[stringaSconti]]`** Stringa sconti già formattata [.md](.md),<br />
  * **`[[totalConfections]]`** Numero totale di pezzi venduti nel documento
  * **`[[totale_colli]]`** Numero Totale dei colli
  * **`[[totale_pagato]]`** Totale di quanto si è già incassato/pagato di questo documento
  * **`[[totale_peso]]`**
  * **`[[totale_sospeso]]`** Totale residuo a pagare/incassare di questo documento
  * ### righe ###
  * **`[[righe(n).aliquota]]`**
  * **`[[righe(n).applicazione_sconti]]`** ( scalare o non scalare )
  * **`[[righe(n).codiceArticoloFornitore]]`**
  * **`[[righe(n).codice_articolo]]`**
  * **`[[righe(n).descrizione]]`**
  * **`[[righe(n).listino]]`**
  * **`[[righe(n).magazzino]]`**
  * **`[[righe(n).moltiplicatore]]`**
  * **`[[righe(n).multiplo]]`**
  * **`[[righe(n).percentuale_iva]]`**
  * **`[[righe(n).quantita]]`**
  * **`[[righe(n).stringaSconti]]`**
  * **`[[righe(n).totaleRiga]]`**
  * **`[[righe(n).unita_base]]`**
  * **`[[righe(n).valore_unitario_lordo]]`**
  * **`[[righe(n).valore_unitario_netto]]`**
  * ### scadenze ###
  * **`[[scadenze(n).data]]`**
  * **`[[scadenze(n).data_pagamento]]`**
  * **`[[scadenze(n).importo]]`**
  * **`[[scadenze(n).pagamento]]`**
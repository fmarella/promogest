## Fase preparatoria ##

Informazioni da compilare prima di usare la fattura PA.

Dati azienda:
  * denominazione o ragione sociale
  * telefono
  * numero REA
  * codice fiscale o partita IVA
  * account di posta elettronica (inserire anche solo l'indirizzo email)
  * informazioni sulle sedi operativa e legale
  * progressivo di invio

### Alcune note sul progressivo di invio ###
Il progressivo di invio è un numero che viene incrementato in automatico ogni volta che viene generata con successo un file XML per la fattura PA.
Nel caso in cui l'invio al Sistema di Interscambio fallisce perché vengono riportati errori nel file XML bisogna decrementare il progressivo.
Per decrementare il progressivo basta andare nei dati Azienda, selezionare la tab Fattura PA e modificare il progressivo.

Associare a ciascun documento i numeri CIG, CUP tramite i campi del documento (guardare la tab Informazioni Aggiuntive).

### Alcune note relative al documento ###

  1. Ciascuna riga di descrizione dell'articolo o del servizio deve essere lunga 100 caratteri. Viene effettuato un controllo e in caso la lunghezza è maggiore viene riportato un errore.

  1. I codici CIG e CUP hanno lunghezza massima di 15 caratteri. Viene effettuato un controllo e in caso la lunghezza è maggiore viene riportato un errore.


Nell'anagrafica dei pagamenti inserire in corrispondenza di ciascun pagamento un codice appropriato tra i seguenti:
  * MP01 per contanti
  * MP02 per assegno
  * MP03 per assegno circolare
  * MP04 per contanti presso Tesoreria
  * MP05 per bonifico
  * MP06 per vaglia cambiario
  * MP07 per bollettino bancario
  * MP08 per carta di credito
  * MP09 per RID
  * MP10 per RID utenze
  * MP11 per RID veloce
  * MP12 per Riba
  * MP13 per MAV
  * MP14 per quietanza erario stato
  * MP15 per giroconto su conti di contabilità speciale
  * MP16 per domiciliazione bancaria
  * MP17 per domiciliazione postale
  * MP18 per bollettino di c/c postale
  * MP19 per SEPA Direct Debit
  * MP20 per SEPA Direct Debit CORE
  * MP21 per SEPA Direct Debit B2B

Per ciascun ente della PA presente in anagrafica cliente inserire le informazioni generali di ragione sociale, denominazione, partita IVA, codice fiscale, sede. Il campo **codice** deve essere valorizzato con il codice dell'ufficio dell’amministrazione dello stato destinatario della fattura, definito dall'amministrazione di appartenenza come riportato nella rubrica “Indice PA”.


## Creazione di una file XML per la Fattura PA ##

In anagrafica documenti, creare un documento e salvarlo.

Selezionare il documento nella lista e fare click su Esporta Fattura PA. Comparirà una schermata per il salvataggio del file XML su disco, lasciate il nome del file inalterato e selezionate Salva.

Ora il file XML è pronto per l'invio alla pubblica amministrazione.

## Risorse aggiuntive ##

  1. Vorrei testare il file XML prodotto dal Promogest, come posso fare? Vai qui: http://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/AccediAlServizioAction.do?pagina=controlla_fattura
  1. Come firmare la Fattura PA? Leggi qui: http://fatturapa.gov.it/export/fatturazione/it/c-12.htm
  1. Come inviare la Fattura PA? Leggi qui: http://fatturapa.gov.it/export/fatturazione/it/c-13.htm
  1. Come faccio a monitorare lo stato del mio invio? Leggi qui: http://fatturapa.gov.it/export/fatturazione/it/c-14.htm

## Risoluzione di Problemi ##

Se si usa Windows e la finestra di salvataggio del documento rimane aperta dopo aver premuto il tasto Salva, seguire questa procedura:

  1. Selezionare il menu Start -> Esegui -> cmd
  1. nella finestra appena aperta digitare: cd c:\Python26\Scripts e premere Invio
  1. ora digitare easy\_install.exe -U jinja2 e premere Invio
  1. una volta che la procedura è terminata chiudere la finestra
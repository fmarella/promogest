# Dettaglio #
Il sistema utilizza http://sphinx.pocoo.org/index.html come generatore di doc. Questa libreria si occupa di fare un parsing dei file rst e di generare gli html, i loro link, ed un sistema integrato di ricerca nella documentazione stessa. Con pochi ritocchi al CSS il risultato finale è  esteticamente gradevole e permette una facile consultazione.

Nel 2009 avevo iniziato a crearne una ma non era facile da mantenere, quando una cosa richiede troppo sforzo per un risultato modesto subentra la frustrazione e così è stato per quella procedura.

Francesco Marella stavolta ha creato un Makefile ed ha analizzato la possibilità di scrivere la doc direttamente nei sorgenti. Sembrava una buona idea ma ci siamo resi conto che non riduceva il lavoro ma anzi rischiava di creare ulteriore confusione con un rimando di files del tutto inutile.

La procedura concordata quindi è la seguente.
Mantenere una cartella doc nei sorgenti del programma con all'interno SOLO i file rst della documentazione.
Le immagini verranno caricate direttamente sul sito tramite una procedura un po' rudimentale ma funzionante all'interno del siteAdmin di http://www.promogest.me
Ogni volta che si modificherà qualcosa verrà fatto un commit come al solito.

Sul server poi verrà messo in crontab un piccolo script di bash che si occuperà di:

  * Fare periodicamente un svn update dei sorgenti
  * Lanciare il make html per generare la creazione delle pagine statiche con sphinx

La help.promogest.me punterà alla cartella _build della doc riportando online in automatico ogni modifica effettuata magari con cadenza oraria o anche giornaliera._

PRO:
  * Si modificheranno i sorgenti rst insieme agli altri sorgenti
  * Un semplice commit porterà tramite passaggi automatici la doc direttamente online pronta per la consultazione.
  * Il sistema ridurrà notevolmente i sorgenti che al momento sono appesantiti da immagini di screenshot in locale del tutto inutili

DA DECIDERE:
Se tenere gli rst solo su trunk , solo su gcode o su entrambi
Se mettere un try che in presenza di sphinx sul pc client compili in locale la doc per una più veloce consultazione. ....


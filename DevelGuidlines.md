# Linee guida #

**Environment.workingYear** viene memorizzato come stringa. Potrebbe essere necessario convertire
tale valore ad intero in alcuni casi. (es. datetime(int(workingYear), 1, 1))

DAO:
  * il nome del file e il nome della classe seguono la convenzione python per le classi ( CamelCase ) (es. BancheAzienda.py -> class BancheAzienda(Dao): pass);
  * il nome assegnato all'istanza della tabella **deve avere** il prefisso **t`_`**  e segue la convenzione python per le variabili (minuscolo con underscore) (es. t\_banche\_azienda);
  * è **assolutamente vietato** ricreare in un DAO l'istanza di una tabella definita altrove. Tale istanza deve essere _importata_!;
  * all'interno dei DAO non si dovrebbero **MAI** richiamare funzioni di interfaccia (es. messageInfo, messageWarning, ect) in caso di errore ma sollevare una eccezione che andrà gestita a livello di presentazione (nella ui)

http://pythonguy.wordpress.com/2011/08/17/sqlalchemy-tips-performance/

## Creazione di una nuova tabella ##

Inserire in ./core/promogest/dao/DaoOrderedImport.py il riferimento dopo la/le tabella/e da cui dipende la nuova tabella.

TODO: utilizzare session.close e delete\_pickle


# Custom Widgets #

## HTMLViewerWidget ##

Permette di effettuare il rendering di un template HTML e visualizzarne il risultato all'interno di una finestra esistente.
Il widget mette a disposizione un pulsante per la stampa del risultato.

Commit rilevanti: [3330](http://code.google.com/p/promogest/source/detail?r=3330) e [3332](http://code.google.com/p/promogest/source/detail?r=3332)

1. Importiamo il widget:
```
from promogest.ui.widgets.HTMLViewerWidget import HTMLViewerWidget
```

2. Creiamo un'istanza del widget e lo aggiungiamo al contenitore (es. una finestra):
```
self.html_viewer = HTMLViewerWidget(self)
contenitore.add(self.html_viewer.get_viewer())
```

3. Generiamo il codice HTML dal template e visualizziamo il risultato:
```
pageData = {
  'file': 'template.html',
  ...
}
self.html_viewer.renderHTML(pageData)
```

4. profit!

PS: il widget ha anche una progressbar: **self.html\_viewer.progressbar**.
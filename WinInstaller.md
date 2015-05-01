Descrizione del processo di creazione di un installer per
sistemi operativi Microsoft Windows.

Le versioni di Python supportate da PyGI-AIO al momento della scrittura di questa procedura sono: 2.7, 3.1, 3.2, 3.3, 3.4

# Dettagli #

## Strumenti necessari ##
  * NSIS
  * installer Python
  * PyGI-AIO da http://opensourcepack.blogspot.it/p/pygobject-pygi-aio.html (thanks to TumaGonx Zakkum!)
  * PySVN http://pysvn.tigris.org/servlets/ProjectDocumentList?folderID=1768
  * PyWin32 http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/
  * sorgenti installer PromoGest
  * 7zip

## Procedura ##

  * Decomprimere il PyGI-AIO scaricato in precedenza
  * Dalla cartella **binding** di PyGI-AIO, scegliere l'archivio 7z corrispondente alla versione target di Python. Questa cartella (d'ora in poi chiamiamola BASE) funziona da base su cui aggiungere le librerie Gtk+, Gdk, ect.
  * Ora dobbiamo decomprimere le librerie nella cartella _BASE_.
Attenzione: Se abbiamo scelto una versione di Python tra 2.7,3.1,3.2, le librerie a cui dobbiamo fare riferimento sono nella cartella **rtvc9**, altrimenti **rtvc10**.
  * Decomprimere il contenuto gli archivi seguenti in _BASE_, unendo eventualmente le cartelle già presenti:
    * Base
    * Atk
    * Aspell
    * GTK
    * GDK
    * GDKPixbuf
    * Orc
    * Pango
    * Poppler
    * Soup
    * WebkitGTK
    * Gstreamer
    * GXML
    * SQLite
Le dipendenze di ciascuna libreria sono nel file depends.txt della libreria se presente.
  * Aprire il file promogest.nsi per modificare il percorso alla cartella BASE, il percorso agli installer per le librerie PySVN, PyWin32, all'installer di Python. Può essere necessario modificare anche i percorsi e il valore di variabili varie.
  * Copiare le librerie dll AccessControl e AccessControlW nella cartella Plugins di NSIS
  * Compilare il file **promogest.nsi** per ottenere l'installer.

## Dettagli sull'installer ##

  * L'installer usa **pip** per l'installazione di alcuni moduli necessari ad eseguire correttamente PromoGest.
  * L'installer aggiunge alla variabile di sistema **PATH** il percorso alla cartella c:\PythonVERSIONE e c:\PythonVERSIONE\Scripts. Questo significa che **python.exe** e **pip.exe** sono eseguibili da linea di comando.
  * pip install -r requirements.txt sembra non funzionare su win :\
  * la cartella in cui viene clonato il repository si trova in %APPDATA%/pg3

enjoy! :p
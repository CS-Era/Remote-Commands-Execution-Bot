La Botnet è suddivisa in più file, sia lato Client che lato Server.

generalFiles: per uso generico
connectionFiles: per stabilire le connessioni necessarie
remoteCommandsFiles: per il controllo da remoto della vittima

IMPORTANTE: prima di procedere con l'esecuzione di client e/o server, provvedere ad installare tutte le librerie richieste nel .txt "requirements" automaticamente generato tramite pipreqs. A tal proposito, utilizzare il comando <pip install -r requirements.txt>.

Nei files di connessione è possibile modificare indirizzo ip e porto a seconda delle esigenze.


LISTA DEI COMANDI REMOTI DISPONIBILI E RELATIVA SPIEGAZIONE:

<info> 					stampa le informazioni sul sistema operativo della vittima
<help> 					stampa la lista dei comandi con relativa spiegazione
<ls path>   				lista tutti i file in un path
<cd path>				cambia la posizione in base al path indicato
<find .estensione path>			trova i file con una certa estensione in un certo percorso
<filespath .est {1,n}>			trova in tutto il filesystem i file che corrispondono ad una o n estensioni e 		
					li scrive in un .txt con relativi percorsi
<download "nomeFile.estensione">	scarica il file con una certa estensione (è richiesto che ci si trovi nello stesso path in cui si trova il file)
<network/rete>				corrisponde ad un ipconfig/ifconfig
<screenshot>				effettua uno screen
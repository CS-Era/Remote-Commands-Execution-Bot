
IT Version--

ATTENZIONE: Le botnet sono spesso utilizzate per scopi illegali (es. compromissione di infrastrutture critiche, furti, ricatti, diffusione di materiali pedopornografici, etc.). L’applicativo rappresenta un progetto universitario per il corso di Reti di Calcolatori della Federico II di Napoli ed è stato sviluppato solo ed esclusivamente per scopi didattici.
Gli sviluppatori non si assumono nessuna responsabilità in merito all'utilizzo che terzi possano effettuare dell'applicativo in questione nel caso in cui il codice venga reso disponibile OpenSource.

Gli sviluppatori: Erasmo Prosciutto, Biagio Scotto di Covella, Antonio Lanuto


INFO GENERALI:

La Botnet è suddivisa in più file, sia lato Client che lato Server.

generalFiles: per uso generico
connectionFiles: per stabilire le connessioni necessarie
remoteCommandsFiles: per il controllo da remoto della vittima

IMPORTANTE: prima di procedere con l'esecuzione di client e/o server, provvedere ad installare tutte le librerie richieste nel .txt "requirements" automaticamente generato tramite pipreqs. A tal proposito, utilizzare il comando <pip install -r requirements.txt>.
In presenza di problematiche con le librerie provvedere ad installarle singolarmente tramite il seguente comando:

<pip install nomeLibreria>

Librerie necessarie: 
colorama==0.4.6
psutil==5.9.3
PyAutoGUI==0.9.53
tqdm==4.64.1

Il codice è stato testato principalmente su Python 3.8.

Nei files di connessione è possibile modificare indirizzo ip e porto a seconda delle esigenze.

ESECUZIONE:

Vittima: client.py
Server:  server.py


LISTA DEI COMANDI REMOTI DISPONIBILI E RELATIVA SPIEGAZIONE:

<info> 						stampa le informazioni sul sistema operativo della vittima
<clear>						pulisci schermo
<pwd>						stampa la working directory
<help> 						stampa la lista dei comandi con relativa spiegazione
<ls <Path> >   					lista tutti i file in un path
<cd <Path> >					cambia la posizione in base al path indicato
<find .est <Path> >				trova i file con una certa estensione in un certo percorso
<filespath .est {1,n}>				trova in tutto il filesystem i file che corrispondono ad una o n estensioni e 		
						li scrive in un .txt con relativi percorsi
<download "nomeFile.estensione" <Path> > 	scarica il file con una certa estensione
<network/rete>					corrisponde ad un ipconfig/ifconfig
<screenshot>					effettua uno screen
<open "nomeZip">				apre un file zip
<exit>						chiusura controllo remoto


TIPOLOGIE DI PATH:

<.>						path corrente
<..>						path fino al percorso precedente alla wd
<./<Path> >					path dalla cartella corrente + path
<Path>        					path relativo o assoluto




ING Version--


DISCLAIMER: Botnets are often used for illegal purposes (e.g. compromising critical infrastructures, theft, blackmail, spreading child pornography, etc.). The application represents a university project for the Computer Networks course at the Federico II University in Naples and was developed solely and exclusively for teaching purposes.
The developers do not accept any responsibility for the use that third parties may make of the application in question if the code is made available OpenSource.

The developers: Erasmo Prosciutto, Biagio Scotto di Covella, Antonio Lanuto


GENERAL INFO:

The Botnet is divided into several files, both Client and Server side.

generalFiles: for general use
connectionFiles: for establishing the necessary connections
remoteCommandsFiles: for remote control of the victim

IMPORTANT: Before proceeding with client and/or server execution, ensure that all required libraries are installed in the 'requirements' .txt automatically generated via pipreqs. To do this, use the command <pip install -r requirements.txt>.
If there are problems with the libraries, install them individually using the following command:

<pip install library name>.

Required libraries: 
colourama==0.4.6
psutil==5.9.3
PyAutoGUI==0.9.53
tqdm==4.64.1

The code was mainly tested on Python 3.8.

In the connection files it is possible to change ip address and port as required.


LIST OF AVAILABLE REMOTE COMMANDS AND THEIR EXPLANATION:

<info> print information about the victim operating system
<clear> wipe screen
<pwd> print working directory
<help> print the list of commands and their explanation
<ls <Path> > list all files in a path
<cd <Path> > change location to the given path
<find .est <Path> > find files with a certain extension in a certain path
<filespath .est {1,n}> finds files in the whole filesystem that match one or n extensions and 		
						writes them into a .txt file with relative paths
<download "filename.extension" <Path> > downloads the file with a certain extension (it is required to be in the same path as the file)
<network/network> corresponds to an ipconfig/ifconfig
<screenshot> take a screen shot
<open "zipname"> open a zip file
<exit> close remote control


PATH TYPES:

<.> current path
<..> path to previous path to wd
<./<Path> > path from current folder + path
<Path> relative or absolute path


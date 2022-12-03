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



def regexcheck_download(comando):
    windows_regex_tip1 = r'^download \"[a-zA-Z0-9, ,\_,\-,\.,\']+\.[a-z]{1,4}\" (\.(\\[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\\[a-zA-Z0-9, ,\_,\-]+)+)'
    unix_regex_tip1 = '^download \"[a-zA-Z0-9, ,\_,\-,\.,\']+\.[a-z]{1,4}\" (\.(\/[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\/[a-zA-Z0-9, ,\_,\-]+)+)'
    windows_regex_tip2 = r'^'
    unix_regex_tip2 = '^'
    result1 = 'null'
    result2 = 'null'
    systemName = platform.system()

    if systemName == 'Windows':
        print("Ho riconosciuto la regex per windows")
        result1 = re.match(windows_regex_tip1,comando)
        result2 = re.match(windows_regex_tip2,comando)
    else:
        print("Ho riconosciuto la regex per unix")
        result1 = re.match(unix_regex_tip1,comando)
        result2 = re.match(unix_regex_tip2,comando)

    if result1 != 'null':
        if systemName == 'Windows':
            print("ritorno match per windows tipologia 1")
            return "windowstip1"
        else:
            print("ritorno match per unix tipologia 1")
            return "unixtip1"
    elif result2 != 'null':
        if systemName == 'Windows':
            print("ritorno match per windows tipologia 2")
            return "windowstip2"
        else:
            print("ritorno match per unix tipologia 2")
            return "unixtip2"
    else:
        return 'not matched'

# OK regExpr find
def regexcheck_find(comando):
    windows_regex=r'^find \.[a-z]{1,4} (\.(\\[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\\[a-zA-Z0-9, ,\_,\-]+)+)'
    unix_regex='^find \.[a-z]{1,4} (\.(\/[a-zA-Z0-9, ,\_,\-]+)+|\.{1,2}|(\/[a-zA-Z0-9, ,\_,\-]+)+)'
    result = 'null'

    if platform.system()=='Windows':
        result = re.match(windows_regex,comando)
    else:
        result = re.match(unix_regex,comando)

    if result:
        return True
    else:
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
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

    windows_regex_tip1 = r'^download "[\s\S]+\.[a-z]{1,4}" (\.(\\[^\/]+)+|\.{1,2}|(\\[^\/]+)+)'
    unix_regex_tip1 = '^download \"[\s\S]+\.[a-z]{1,4}\" (\.(\/[^\/]+)+|\.{1,2}|(\/[^\/]+)+)'
    windows_regex_tip2 = r'^download "[\s\S]+\.[a-z]{1,4}" nel percorso: C:(\\[^\/]+)+'
    unix_regex_tip2 = '^download \"[\s\S]+\.[a-z]{1,4}\" nel percorso: (\/[^\/]+)+'
    result1 = 'null'
    result2 = 'null'
    systemName = platform.system()

    if systemName == 'Windows':
        if re.match(windows_regex_tip1,comando):
            return "windowstip1"
        elif re.match(windows_regex_tip2,comando):
            return "windowstip2"
        else:
            return "not matched"
    else:
        if re.match(unix_regex_tip1,comando):
            return "unixtip1"
        elif re.match(unix_regex_tip2,comando):
            return "unixtip2"
        else:
            return "not matched"

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
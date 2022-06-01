
#!/usr/bin/python3
import platform
import logging
from collections import defaultdict
import os
import enum
import subprocess

targetFiles = [
    {
        'fileName': 'vscode_extensions',
        'windowsCommand': lambda: subprocess.run(["code","--list-extensions"], stdout=open("vscode_extensions", mode='w'), stderr=subprocess.STDOUT, shell=True)
    }
]

def main():
    pf = platform.system()
    if(pf == 'Windows'):
        for n in targetFiles:
            if (n.get('windowsCommand') is not None):
                n.get('windowsCommand')()
                print('windowsCommand OK')
    elif(pf == 'Linux'):
        pass

if __name__ == "__main__":
    main()

#!/usr/bin/python3
import platform
import logging
from collections import defaultdict
import os
import enum

messageFormat = "[%(who)s %(count)s回目] %(message)s"
formatter = logging.Formatter(messageFormat)
stdHandler = logging.StreamHandler()
stdHandler.setFormatter(formatter)
logging.basicConfig(level=logging.DEBUG, handlers=[stdHandler])
class ExtensionLogRecord(logging.LogRecord):
        counts = defaultdict(int)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            msg = str(self.msg)
            self.counts[msg] += 1
            self.who = platform.uname().node
            self.count = self.counts[msg]
logging.setLogRecordFactory(ExtensionLogRecord)
log = logging.getLogger(__name__)

# os.environ["HOME"]はwindowsに無いので例外が発生する。
# 他のOS環境でも同様の問題が起こりそうなので、ラムダ関数に変更し遅延評価する。
# （文字列にしてeval関数で実行する方法もあるが、補完やIDEアシスト機能が効かなくなるので使いたくない。）
targetFiles = [
    {
        'fileName': 'javascript.json', 
        'windowsPathDir': lambda: os.environ["USERPROFILE"] + "\\AppData\\Roaming\\Code\\User\\snippets"
    },
    {
        'fileName': 'typescript.json', 
        'windowsPathDir': lambda: os.environ["USERPROFILE"] + "\\AppData\\Roaming\\Code\\User\\snippets"
    },
    {
        'fileName': 'Microsoft.PowerShell_profile.ps1', 
        'windowsPathDir': lambda: os.environ["USERPROFILE"] + "\\Documents\\WindowsPowerShell"
    },
    {
        'fileName': '.bashrc_aliases',
        'linuxPathDir': lambda: os.environ["HOME"]
    },
    {
        'fileName': '.zsh_original',
        'linuxPathDir': lambda: os.environ["HOME"]
    },
]
currentDir = os.path.dirname(os.path.abspath(__file__))

def main():
    pf = platform.system()
    if(pf == 'Windows'):
        # windTargetDir = [n for n in targetFiles if n.get('windowsPathDir') is not None]
        for n in targetFiles:
            getPath = n.get('windowsPathDir')
            isExistAttribute = getPath is not None
            if (not isExistAttribute):
                continue
            path = getPath()
            fileName = n.get('fileName')
            # 大半のWin環境はプロファイルディレクトリが無い。無ければ作る。
            if not os.path.isdir(path):
                os.mkdir(path)
            log.debug(currentDir)
            os.symlink(os.path.join(currentDir, fileName), os.path.join(path, fileName))
    elif(pf == 'Linux'):
        for n in targetFiles:
            getPath = n.get('linuxPathDir')
            isExistAttribute = getPath is not None
            if (not isExistAttribute):
                continue
            path = getPath()
            fileName = n.get('fileName')
            # 大半のWin環境はプロファイルディレクトリが無い。無ければ作る。
            if not os.path.isdir(path):
                os.mkdir(path)
            log.debug(currentDir)
            os.symlink(os.path.join(currentDir, fileName), os.path.join(path, fileName))
    else:
        pass


if __name__ == "__main__":
    main()

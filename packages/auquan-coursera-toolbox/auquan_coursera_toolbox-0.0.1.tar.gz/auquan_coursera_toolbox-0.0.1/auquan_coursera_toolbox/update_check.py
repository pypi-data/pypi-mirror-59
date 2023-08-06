__version__ = '0.0.6'

from urllib.request import urlopen
import json

def updateCheck():
    updateStr = ''
    try:
            toolboxJson = urlopen('https://pypi.python.org/pypi/ukv1_toolbox/json')
    except Exception as e:
        return False

    toolboxDict = json.loads(toolboxJson.read().decode('utf8'))

    if __version__ != toolboxDict['info']['version']:
        return True
    else:
        return False

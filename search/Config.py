import json
from collections import namedtuple

def getConfig(configPath):
    configFile = open(configPath,'r')
    data = configFile.read()
    x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return x






from .login import *
from .error import TemplateLoginError

paramsKeysMap = {
        'phone': '手机号',
        'password': '密码',
        }

defaultName = 'TemplateLogin'

def getLoginHandler(name=None):
    name = name or defaultName
    return eval(name)

def checkLoginParams(params={}, name=None):
    name = name or defaultName
    mustKeys = eval(f'mustParams{name}')
    if type(mustKeys) == dict: mustKeys = mustKeys.keys()
    notKeys = [key for key in mustKeys if not params.get(key)]
    if len(notKeys) > 0: raise TemplateLoginError(10003, other=','.join(notKeys))
    return { key: params.get(key) for key in mustKeys }

def getLoginParams(name=None):
    name = name or defaultName
    mustKeys = eval(f'mustParams{name}')
    keysMaps = paramsKeysMap.copy()
    if type(mustKeys) == dict:
        keysMaps.update(mustKeys)
        mustKeys = mustKeys.keys()
    return {key: paramsKeysMap.get(key, '未知') for key in mustKeys}


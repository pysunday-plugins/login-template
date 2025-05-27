from sunday.core import getException

errorMap = {
        10000: '未知登录报错',
        99999: '程序执行异常，请反馈开发人员',
        }

TemplateLoginError = getException(errorMap, [])


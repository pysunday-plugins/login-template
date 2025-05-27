# coding: utf-8
from sunday.utils import LoginBase
from sunday.core import Logger, enver, Auth, getEnv, aesCbcDecrypt, getConfig
from pydash import pick
from .error import errorMap, TemplateLoginError

cryptoKey = getConfig('CRYPTO')('key')

def getUrlMap(url):
    baseUrl = url + '/api'
    return {
            'login': baseUrl + '//login',
            'currentUser': baseUrl + '/profile',
            }

mustParamsTungeeLogin = {
        'phone': '手机号',
        'password': '密码',
        }
class TemplateLogin(LoginBase):
    def __init__(self, phone=None, password=None, isEncrypt=False, useLoginState=True, **_):
        self.logger = Logger('登录').getLogger()
        self.urlMap = getUrlMap('https://user.template.com')
        LoginBase.__init__(self, logger=self.logger, ident=phone or '', error=[99999, '接口异常，请稍后重试'])
        self.phone = phone
        self.password = aesCbcDecrypt(password, cryptoKey) if isEncrypt else password
        self.initAuth()
        self.rs, self.isLogin = self.initRs(self.urlMap['currentUser'], useLoginState)

    def initAuth(self):
        auth = Auth(self.getEnvPwd(), '[登录]')
        self.getenv, self.setenv, *_ = enver(self.getEnvPwd())
        auth.addParams('password', value=self.password or self.getenv('password') or '', isPass=False, tip='密码')
        self.auth = auth

    def checkLogin(self, checkUrl):
        try:
            res = self.fetch.get_json(checkUrl)
        except Exception:
            return True
        return res.get('stat') != 1

    def userLogin(self):
        params = self.auth.getParams()
        self.rs.post_json(
                self.urlMap['login'],
                data={
                    "phone": self.phone,
                    "password": params.get('password')
                },
            )

    def getCurrentUser(self):
        res = self.rs.get_json(self.urlMap['currentUser'])
        return pick(res, 'name', 'phone')

    def login(self):
        if self.isLogin:
            self.logger.info('登录成功')
            return self
        self.userLogin()
        if not self.checkLogin(self.urlMap['currentUser']):
            self.logger.info('登录成功')
            self.saveCookie()
            return self
        else:
            self.logger.error(errorMap[10000])
            raise TemplateLoginError(10000)


if __name__ == "__main__":
    tungee = TemplateLogin(getEnv('SUNDAY_CUS_TEMPLATE_PHONE'), getEnv('SUNDAY_CUS_TEMPLATE_PASSWORD'))
    tungee.login()

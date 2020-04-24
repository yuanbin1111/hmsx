import hashlib,base64

class UserService():
    # 静态方法 生成密码(结合Pwd和salt)
    @staticmethod
    def generatePwd(pwd,salt):
        m = hashlib.md5()
        str = '%s-%s'%(base64.encodebytes(pwd.encode('utf-8')),salt)
        m.update(str.encode('utf-8'))

        return m.hexdigest()
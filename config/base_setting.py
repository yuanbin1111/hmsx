#设置服务器端口
SERVER_PORT = 8999

#连接数据库
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/hmsx_db?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False


#自动登录cookie
AUTH_COOKIE_NAME = '1903_hmsx'

#拦截器忽略规则
IGNORE_URLS = ['^/user/login']
IGNORE_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]


STATUS = {
    '1':'正常',
    '0':'已删除'
}

UPLOAD = {
    'ext':['jpg','png','bmp','jpeg','gif'],
    'prefix_path':'\\web\\static\\upload',
    'prefix_url':'\\static\\upload'
}
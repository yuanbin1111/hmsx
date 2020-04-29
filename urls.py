from web.controllers.user.User import router_user
from application import app
from web.controllers.index import router_index
from web.controllers.account.Account import router_account
# from web.controllers. import router_static

#拦截器的路由
from web.interceptors.AuthInterceptor import *


#蓝图路由
app.register_blueprint(router_user,url_prefix='/user')
app.register_blueprint(router_index,url_prefix='/')
app.register_blueprint(router_account,url_prefix='/account')

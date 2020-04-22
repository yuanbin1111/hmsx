from web.controllers.user.User import router_user
from application import app

app.register_blueprint(router_user,url_prefix='/user')
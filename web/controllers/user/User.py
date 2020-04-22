from flask import Blueprint

router_user = Blueprint('user_page',__name__)

@router_user.route('/login')
def login():
    return '登录页面'
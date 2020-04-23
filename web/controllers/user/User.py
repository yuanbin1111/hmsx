from flask import Blueprint,render_template,request,jsonify

router_user = Blueprint('user_page',__name__)

@router_user.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    resp = {
        'code':200,
        'msg':'登陆成功',
        'data':{}
    }
    req = request.values
    login_name = req['login_name']
    login_pwd = req['login_pwd']
    #后端校检 不为空 长度不小于1 
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确用户名'
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确密码'
        return jsonify(resp)
    return jsonify(resp)

@router_user.route('/logout')
def logout():
    return '登出页面'

@router_user.route('/edit')
def edit():
    return '编辑页面'

@router_user.route('/reset-pwd')
def resetPwd():
    return '重置密码页面'
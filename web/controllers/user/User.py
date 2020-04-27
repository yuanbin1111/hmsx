from flask import Blueprint,render_template,g,request,jsonify,make_response,redirect

from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from application import app,db

import json

router_user = Blueprint('user_page',__name__)

@router_user.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        if g.current_user:
            return redirect(UrlManager.buildUrl('/'))
        return ops_render('user/login.html')

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

    #数据库比对
    user_info = User.query.filter_by(login_name=login_name).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = '用户不存在'
        return jsonify(resp)

    if user_info.status != 1:
        resp['code'] = -1
        resp['msg'] = '账号被禁用，请联系管理员处理'
        return jsonify(resp)

    if user_info.login_pwd != UserService.generatePwd(login_pwd,user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '密码错误'
        return jsonify(resp)
        
    #将用户信息存入到浏览器的Cookie中
    #json.dumps()处理dict,list类型，经过处理后可以直接再浏览器使用
    response = make_response(json.dumps({'code':200,'msg':'登录成功'}))
    # name value(login-name,login_pwd,login_salt,uid) 过期时间
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],'%s@%s'%(UserService.generateAuthCode(user_info),user_info.uid),60*60*24*5)

    return response

@router_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response

@router_user.route('/edit',methods=['GET','POST'])
def edit():
    if request.method ==  'GET':
        return ops_render('/user/edit.html')
    #post:
    resp = {
        'code':200,
        'msg':'编辑成功',
        'data':{}
    }

    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    #校检
    if nickname is  None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的昵称'

        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1 
        resp['msg'] = '请输入规范的邮箱'

        return jsonify(resp)

    #更新数据库
    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)
    # return ops_render('/user/edit.html')

@router_user.route('/reset-pwd',methods=['GET','POST'])
def resetPwd():
    if request.method == 'GET':
        return ops_render('/user/reset_pwd.html')

    #post
    resp = {
        'code':200,
        'msg':'重置密码成功',
        'data':{}
    }

    #缓存
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    
    #校检
    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的原密码'
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的新密码'
        return jsonify(resp)

    if new_password  == old_password:
        resp['code'] = -1
        resp['msg'] = '原密码与新密码不能相同'
        return jsonify(resp)

    #获取用户信息,修改密码生成新的加密后的密码
    user_info = g.current_user
    user_info.login_pwd = UserService.generatePwd(new_password,user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()


    #更新cookie中的旧密码
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],'%s@%s' % (UserService.generateAuthCode(user_info),user_info.uid),60*60*24*5)


    return response
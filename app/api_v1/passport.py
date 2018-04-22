import base64

from flask import g, current_app, jsonify, request,make_response
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from app import db, redis_conn
from app.api_v1 import api
from app.models import User
from app.utils.response_code import RET
from app.utils.email import send_mail


@api.route('/signin', methods=['POST'])
def signin():
    '''用户注册接口
    :return 返回注册信息{'re_code': '0', 'msg': '注册成功'}
    '''
    nickname =request.json.get('nickname')
    email =request.json.get('email')
    password =request.json.get('password')
    mailcode_client =request.json.get('mailcode')

    if not all([email, nickname, password, mailcode_client]):
        return jsonify(re_code=RET.PARAMERR, msg='参数不完整')

    #从Redis中获取此邮箱对应的验证码,与前端传来的数据校验
    try:
        mailcode_server = redis_conn.get('EMAILCODE:'+ email).decode()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询邮箱验证码失败')
    if mailcode_server != mailcode_client:
        current_app.logger.debug(mailcode_server)
        return jsonify(re_code=RET.PARAMERR, msg='邮箱验证码错误')
    user = User()
    user.email = email
    user.nickname = nickname
    user.password = password    #利用user model中的类属性方法加密用户的密码并存入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR, msg='注册失败')
    #6.响应结果
    return jsonify(re_code=RET.OK,msg='注册成功')

@api.route('/login', methods=['POST'])
def login():
    '''登录
    TODO: 添加图片验证
    :return 返回响应,保持登录状态
    '''
    email = request.json.get('email')
    password = request.json.get('password')

    #解析Authorization
    #email, password = base64.b64decode(request.headers['Authorization'].split(' ')[-1]).decode().split(':')

    if not all([email, password]):
        return jsonify(re_code=RET.PARAMERR, msg='参数不完整')
    try:
        user = User.query.filter(User.email==email).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在',user=user)
    if not user.verify_password(password):
        return jsonify(re_code=RET.PARAMERR, msg='帐户名或密码错误')

    #更新最后一次登录时间
    user.update_last_seen()
    token = user.generate_user_token()
    return jsonify(re_code=RET.OK, msg='登录成功',token=token)



@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == '/login':
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = User.verify_user_token(email_or_token)
        if not user:
            return False
        
    g.user = user
    return True

    # if not email_or_token:
    #     return False
    # email_or_token = re.sub(r'^"|"$', '', email_or_token)
    # user = User.verify_auth_token(email_or_token)
    # if not user:
    #     user = User.query.filter_by(email=email_or_token).first()
    #     if not user or not user.verify_password(password):
    #         return False
    # g.user = user
    # return True

    # user = User.verify_user_token(email_or_token)
    # if not user:
    #     # try to authenticate with email/password
    #     user = User.query.filter_by(email=email_or_token).first()
    #     if not user or not user.verify_password(password):
    #         return False
    # g.user = user
    # return True

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@api.route('/')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.email})



# @api.route('/login')
# @auth.login_required
# def get_user_token():
#     token = g.user.generate_user_token()
#     return jsonify(re_code=RET.OK, msg='获取Token成功', token=token.decode('ascii'), usr=g.user.email)


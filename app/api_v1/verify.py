import random
import re
import json

from flask import current_app, jsonify, request, make_response

from app import redis_conn
from app.models import User
from app.utils.response_code import RET,error_map
from app.utils.email import send_mail
from . import api


@api.route('/mailcode', methods=['POST'])
def send_mail_code():
    '''发送邮箱验证码'''
    nickname =request.json.get('nickname')
    email =request.json.get('email')
    if not all([email, nickname]):
        return jsonify(re_code=RET.PARAMERR, msg='请填写完整的注册信息')

    #邮箱匹配正则
    #^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$
    #手机号匹配正则
    #^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$

    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
        return jsonify(RET.PARAMERR, msg='请填写正确的邮箱')

    #判断用户是否已注册
    try:
        user_email = User.query.filter(User.email == email).first()
        user_nickname = User.query.filter(User.nickname == nickname).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询数据库错误')
    #用户存在,提示该账户已被注册
    if user_email or user_nickname:
        return jsonify(re_code=RET.DATAEXIST, msg='该用户已被注册')

    #生成邮箱验证码
    email_code = '%06d' % random.randint(0,99999) 
    current_app.logger.debug('邮箱验证码为: ' + email_code)   
    try:
        redis_conn.set('EMAILCODE:'+ email, email_code, 1800)   #half-hour = 1800有效期
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='存储邮箱验证码失败')
    
    #发送邮件
    send_mail(
        to = email,
        nickname = nickname,
        mailcode = email_code
    )

    return jsonify(re_code=RET.OK, msg='验证码发送成功')
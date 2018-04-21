from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import jsonify, current_app, g, request
from functools import wraps
from app.utils.response_code import RET

from . import db

class User(db.Model):
    '''用户模型
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    nickname = db.Column(db.String(255), unique=True,index=True) 
    password_hash = db.Column(db.String(128))
    join_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('密码不可访问')
    @password.setter
    def password(self, password):
        '''生成hash密码'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''
        密码验证
        :param password-> 用户密码
        :return 验证成功返回True,否则返回False
        '''
        return check_password_hash(self.password_hash, password)

    def generate_user_token(self, expiration=43200):
        '''
        生成确认身份的Token(密令)
        :param expiration-> 有效期限,单位为秒/此处默认设置为12h
        :return 加密过的token
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'email': self.email}).decode('utf-8')
 
    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_user_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    #额外的功能
    def update_last_seen(self):
        '''
        更新最后一次登录时间
        '''
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def to_json(self):
        '''返回用户信息'''
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'email': self.email,
        }

    def __repr__(self):
        return '<User %r>' % self.nickname

    #TODO: 可以添加用户头像




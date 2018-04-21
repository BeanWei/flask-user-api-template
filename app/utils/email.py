from threading import Thread
from flask import current_app
from flask_mail import Message
from datetime import datetime

from app import mail

def send_async_email(app, msg):
    with app.app_context():   #确认程序上下文被激活
        mail.send(msg)

def send_mail(to, nickname, mailcode):
    '''使用新线程异步发送邮箱
    :param to -> 收件人
    :param nickname -> 收件人注册时所填写的昵称
    :param mailcode -> 生成的邮箱验证码
    :return 执行线程
    '''
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + "您的账号注册验证码",
                  sender=app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
    msg.body = 'sended by flask-email'
    msg.html = '''
    <h1>
        亲爱的 {nickname},
    </h1>
    <h3>
        欢迎来到 <b>Flask-Test-Project</b>!
    </h3>
    <p>
        您的验证码为 &nbsp;&nbsp; <b>{mailcode}</b> &nbsp;&nbsp; 赶快去完善注册信息吧！！！
    </p>

    <p>感谢您的支持和理解</p>
    <p>来自：Flask-Test-Project</p>
    <p><small>{time}</small></p>
    '''.format(nickname=nickname, mailcode=mailcode, time=datetime.utcnow)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
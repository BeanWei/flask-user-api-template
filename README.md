## flask + Vue + Vuex + iview => 前后端分离
### 提供一个可以复用的 用户注册登录，Token验证，session/cookie 登录的 模板

#### 已完成
- [x] 用户注册与登录
- [x] 关联QQ邮箱，注册时发送验证码邮件
- [x] 登录成功后获取token并缓存在本地
- [x] 用户登出,销毁Token

#### Todo
- [ ] Session/Cookie 保持会话
- [ ] 用户新登录时需要填写验证码,验证码图片由后台Python生成并缓存到Redis,图片显示于前端,登录时前端数据与数据库数据校验

### 现有的特性
    * 用户密码两次加密,前后端各加密一次
    * 利用flask_mail多线程发送邮箱
    * 邮箱验证码缓存在Redis中

------------------------------------------------------------
#### 展示
* 登录页
![Alt text](https://github.com/BeanWei/flask-user-api-template/blob/master/Screenshots/login.PNG)

* 注册页
![Alt text](https://github.com/BeanWei/flask-user-api-template/blob/master/Screenshots/signin.PNG)

* QQ邮箱
![Alt text](https://github.com/BeanWei/flask-user-api-template/blob/master/Screenshots/email.PNG)

------------------------------------------------------------
此项目基本上实现了关于用户的业务逻辑需求,后续的需求可以在此模板上进行再次开发.
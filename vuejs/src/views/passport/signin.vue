<template>
<div id="signin" >
    <Row type="flex" justify="center">
        <img src="../../assets/login.jpg" alt="" :style="bg">
        <Col span="5">
            <Card class="form">
                <div slot="title">
                    注册页
                </div>
                <Form ref="formInline" :model="formInline" :rules="ruleInline" >
                    <FormItem prop="nickname">
                        <Input type="text" v-model="formInline.nickname" placeholder="昵称" size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="icecream"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem prop="email">
                        <Input type="text" v-model="formInline.email" placeholder="邮箱" size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="email"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem prop="password">
                        <Input type="password" v-model="formInline.password" placeholder="密码"  size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="locked"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem prop="repassword">
                        <Input type="password" v-model="formInline.repassword" placeholder="确认密码"  size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="locked"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem prop="captcha">
                        <Input type="text" v-model="formInline.mailcode" placeholder="邮箱收到的验证码"  size="large" @on-enter="handleSubmit('formInline', formInline)">                          
                            <Icon slot="prepend" type="paper-airplane"></Icon>
                            <Button slot="append" @click="getMailcode()">发送验证码</Button>
                        </Input>
                    </FormItem>
                    <FormItem>
                        <Button type="info" @click="handleSubmit('formInline', formInline)" long>注册</Button>
                    </FormItem>
                </Form>
                <div class="ft">
                    <router-link to="/login">已有账号？马上登录</router-link>
                </div>
            </Card>
        </Col>
    </Row>
</div>
</template>

<script>
import { requestSignin, requestMailcode } from '../../api/api'
import * as coreJS from '../../utils/core'
export default {
    name: 'signin',
    data () {
    var validateUser = (rule, value, cb) => {
      var pattern = /^[\w\u4e00-\u9fa5]{3,10}$/g
      if (value === '') {
        cb(new Error('请输入昵称'))
      } else if (!pattern.test(value)) {
        cb(new Error('请输入3-10个字母/汉字/数字/下划线'))
      } else {
        cb()
      }
    }
    var validatePwd = (rule, value, cb) => {
      var pattern = /^\S{6,20}$/g
      if (value === '') {
        cb(new Error('请输入密码'))
      } else if (!pattern.test(value)) {
        cb(new Error('请输入6-20个非空白字符'))
      } else {
        if (this.formInline.repassword !== '') {
          this.$refs.formInline.validateField('repassword')
        }
        cb()
      }
    }
    var validateCheckPwd = (rule, value, cb) => {
      if (value === '') {
        cb(new Error('请再次输入密码'))
      } else if (value !== this.formInline.password) {
        cb(new Error('两次输入密码不一致!'))
      } else {
        cb()
      }
    }
    return {
      formInline: {
        nickname: '',
        email: '',
        password: '',
        repassword: '',
        mailcode: ''
      },
      ruleInline: {
        nickname: [
        { validator: validateUser, trigger: 'blur' }
        ],
        email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur,change' }
        ],
        password: [
        { validator: validatePwd, trigger: 'blur' }
        ],
        repassword: [
        { validator: validateCheckPwd, trigger: 'blur' }
        ],
        mailcode: [
        { required: true, message: '请输入验证码', trigger: 'blur' }
        ]       
      },
      bg: {
        width: `${window.innerWidth}px`,
        height: `${window.innerHeight}px`,
        position: "absolute",
        }
    }
  },
  computed: {
    mdpassword: function () {
        return coreJS.encryptedPassword(this.formInline.password)
    }
  },
  methods: {
    handleSubmit(name, form) {
        this.$refs[name].validate((valid) => {
            if (valid && this.formInline.mailcode) {
                var signinParams = {
                    nickname: form.nickname,
                    email: form.email,
                    password: this.mdpassword,
                    mailcode: this.formInline.mailcode
                }
                requestSignin(signinParams).then(response => {
                    if (response.re_code === "0" ) {
                        this.$Message.success("注册成功")
                        this.$router.push('/login')
                    } else {
                        this.$Message.error(response.msg)
                    }  
                }).catch(error => {
                    this.$Message.error(error.status)
                })
            } else {
                this.$Message.error('信息不完整');
            }
        })
    },
    getMailcode() {
        if (this.formInline.nickname && this.formInline.email && this.formInline.password && this.formInline.repassword) {
            var mailcodeParams = {
                nickname: this.formInline.nickname,
                email: this.formInline.email
            }
            requestMailcode(mailcodeParams).then(response => {
                if (response.re_code === "0" ) {
                    this.$Message.success("验证码已发送")
                } else {
                    this.$Message.error(response.msg)
                }  
            }).catch(error => {
                this.$Message.error(error.status)
            })
        } else {
            this.$Message.error('信息不完整');
        }
    }
}
}
</script>

<style lang="less" scoped>
#signin {
    font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;
}
.bg {
    position: absolute;
}
.form {
    text-align: center;
    margin-top: 150px;
    p {
        font-size: 30px;
    }
}
.ft {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  width: 300px;
}
.ft a {
  font-size: 14px;
  text-decoration: none;
  color: #20A0FF;
}
</style>
<template>
<div id="login" >
    <Row type="flex" justify="center">
        <img src="../../assets/login.jpg" alt="" :style="bg">
        <Col span="5">
            <Card class="form">
                <div slot="title">
                    登录页
                </div>
                <Form ref="formInline" :model="formInline" :rules="ruleInline" >
                    <FormItem prop="email">
                        <Input type="text" v-model="formInline.email" placeholder="邮箱" size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="person"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem prop="password">
                        <Input type="password" v-model="formInline.password" placeholder="密码"  size="large" @on-enter="handleSubmit('formInline', formInline)">
                            <Icon slot="prepend" type="locked"></Icon>
                        </Input>
                    </FormItem>
                    <FormItem>
                        <Button type="info" @click="handleSubmit('formInline', formInline)" long>登录</Button>
                    </FormItem>
                </Form>
                <div class="ft">
                    <router-link to="/signin">没有账号？马上注册</router-link>
                </div>
            </Card>
        </Col>
    </Row>
</div>
</template>
<script>
    import { requestLogin } from '../../api/api'
    import * as coreJS from '../../utils/core'
    export default {
        name: 'login',
        data () {
            return {
                formInline: {
                    email: '',
                    password: ''
                },
                ruleInline: {
                    email: [
                        { required: true, message: '请填写邮箱', trigger: 'blur' },
                        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur,change' }
                    ],
                    password: [
                        { required: true, message: '请填写密码', trigger: 'blur' },
                        { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
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
                    if (valid) {
                        var loginParams = {
                            email: form.email,
                            password: this.mdpassword
                        }
                        requestLogin(loginParams).then(response => {
                            if (response.re_code === "0" ) {
                                this.$Message.success("登录成功")
                                let token = response.token
                                this.$store.commit('set_token', token)
                                this.$router.push('/')
                            } else {
                                this.$Message.error(response.msg)
                            }  
                        }).catch(error => {
                            this.$Message.error(error.status)
                        })
                    } else {
                        this.$Message.error('表单验证失败!');
                    }
                })
            }
        }
    }
</script>

<style lang="less" scoped>
#login {
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
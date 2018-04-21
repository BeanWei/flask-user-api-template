// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import {Message} from 'iview'

Vue.component('Message', Message)

Vue.use(iView)
Vue.config.productionTip = false

// axios.interceptors.request.use((config) => {
//     console.log(config)
//     return config;
// }, (error) => {
//     Message.error(error)
//     return Promise.reject(error)
// })

axios.interceptors.request.use( config => {
    if (localStorage.token) {
        config.headers.Authorization = `token ${localStorage.token}`
    }
    return config
},err => {
    return Promise.reject(err)
})

axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response) {
        console.log(error)
        switch (error.response.status) {
            case 401:
                store.commit('del_token')
                router.push('/login')
        }
        Message.error('请重新登录')
    }
    return Promise.reject(error.response.data)
})

router.beforeEach((to, from, next) => {
    if (to.meta.required) {
        if (localStorage.token) {
            store.commit('set_token', localStorage.token)
            axios.defaults.auth = {
                email: store.state.token,
                password: store.state.token,
            }
            iView.LoadingBar.start();
            next()
        } else {
            next({
                path: '/login',
            })
        }
    } else {
        iView.LoadingBar.start();
        next()
    }
})

router.afterEach((to, from, next) => {
    iView.LoadingBar.finish();
})


Vue.prototype.$axios = axios
    /* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    components: { App }
})
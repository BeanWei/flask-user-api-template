// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView)
Vue.config.productionTip = false

axios.defaults.baseURL = 'http://127.0.0.1:5000/api/v1.0'
axios.defaults.auth = {
    email: '',
    password: '',
}

// axios.interceptors.request.use((config) => {
//     console.log(config)
//     return config;
// }, (error) => {
//     return Promise.reject(error)
// })

axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response) {
        switch (error.response.status) {
            case 401:
                store.commit('del_token')
                router.push('/login')
        }
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
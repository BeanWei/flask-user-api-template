import Vue from 'vue'
import Router from 'vue-router'
import Index from '../views/index'
import Login from '../views/passport/login'
import Signin from '../views/passport/signin'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'index',
        component: Index,
        meta: {
            required: true,
        }
    }, {
        path: '/login',
        name: 'login',
        component: Login,
    }, {
        path: '/signin',
        name: 'signin',
        component: Signin
    }]
})
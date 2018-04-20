import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: ''
    },
    mutations: {
        set_token(state, token) {
            state.token = token
            localStorage.token = token
        },
        del_token(state) {
            state.token = ''
            localStorage.removeItem('token')
        }
    }
})
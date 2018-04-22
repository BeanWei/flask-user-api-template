import axios from 'axios'

let baseURL = 'http://127.0.0.1:5000/api/v1.0'

export const requestLogin = params => {
    return axios ({
        method: 'POST',
        url: `${baseURL}/login`,
        data: params
    })
    .then(res => res.data)
}

export const requestSignin = params => {
    return axios ({
        method: 'POST',
        url: `${baseURL}/signin`,
        data: params
    })
    .then(res => res.data)
}

export const requestMailcode = params => {
    return axios ({
        method: 'POST',
        url: `${baseURL}/mailcode`,
        data: params
    })
    .then(res => res.data)
}
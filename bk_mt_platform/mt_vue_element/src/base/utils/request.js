import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '../store'
import Cookies from 'js-cookie'

const axiosConfig = {
  baseURL: process.env.VUE_APP_BASE_API, // api 的 base_url
  withCredentials: true, // 跨域请求时发送 cookies
  timeout: 10000 // request timeout
}

function requestConfig(config) {
  config.headers['X-CSRFToken'] = Cookies.get('bk_mt_framework_csrftoken')
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  return config
}

function requestError(error) {
  return Promise.reject({ 'code': 60000, 'message': error.message })
}

function responseSuccess(response) {
  const res = response.data
  if (res.code !== 0) {
    Message({
      showClose: true,
      message: res.code + ': ' + JSON.stringify(res.message),
      type: 'error',
      duration: 5 * 1000
    })

    return Promise.reject({ 'code': res.code, 'message': res.message })
  } else {
    return res.data
  }
}

function responseError(error) {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    if (error.response.status === 401) {
      MessageBox.confirm('你已被登出，可以取消继续留在该页面，或者重新登录', '确定登出', {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.dispatch('user/resetUserInfo').then(() => {
          location.reload()
        })
      })
    } else {
      Message({
        message: 'System: ' + error.message,
        type: 'error',
        duration: 5 * 1000
      })
    }
  } else {
    // Something happened in setting up the request that triggered an Error
    Message({
      message: 'Unknown: ' + error.message,
      type: 'error',
      duration: 5 * 1000
    })
  }

  return Promise.reject({ 'code': 50000, 'message': error.message })
}

function raw_responseSuccess(response) {
  const res = response.data
  if (res.code !== 0) {
    return Promise.reject({ 'code': res.code, 'message': res.message })
  } else {
    return res.data
  }
}

function raw_responseError(error) {
  return Promise.reject({ 'code': 50000, 'message': error.message })
}

// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// axios实例, 上层处理错误情况, 逻辑层直接处理数据
// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const service = axios.create(axiosConfig)

// request interceptor
service.interceptors.request.use(
  requestConfig,
  requestError
)

// response interceptor
service.interceptors.response.use(
  responseSuccess,
  responseError
)

export const request = service.request

// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// axios原生实例, 直接返回错误
// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const raw_service = axios.create(axiosConfig)

// request interceptor
raw_service.interceptors.request.use(
  requestConfig,
  requestError
)

// response interceptor
raw_service.interceptors.response.use(
  raw_responseSuccess,
  raw_responseError
)

export const raw_request = raw_service.request

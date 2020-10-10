import { request } from '@/base/utils/request'

export function testAPI(data) {
  return request({
    url: '/api/test_api/',
    method: 'get',
    data
  })
}

export function getInfo() {
  return request({
    url: '/api/login/get_user_info/',
    method: 'get'
  })
}

export function getAllUserInfo() {
  return request({
    url: '/api/login/get_all_user_info/',
    method: 'get'
  })
}

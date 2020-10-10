import {request} from '@/base/utils/request'

export function getSelectServers(biz_id) {
  return request({
    url: '/order_center/release/servers/?biz_id=' + biz_id,
    method: 'get'
  })
}

export function getServer(params) {
  return request({
    url: '/order_center/release/serverlist/',
    method: 'get',
    params: params
  })
}

export function getVersion(biz_id) {
  return request({
    url: '/order_center/release/version/?biz_id=' + biz_id,
    method: 'get'
  })
}

export function getSerVersion(biz_id) {
  return request({
    url: '/order_center/release/get_version/?biz_id=' + biz_id,
    method: 'get'
  })
}

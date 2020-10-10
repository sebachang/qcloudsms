import { request } from '@/base/utils/request'

//获取平台主机关联
export function getPlatfromHostList(args) {
  return request({
    url: './order_center/deliver/order/platform/host/' + args,
    method: 'get'
  })
}

export function getPlatfromCenterList(args) {
  return request({
    url: './order_center/deliver/order/platform/center/' + args,
    method: 'get'
  })
}

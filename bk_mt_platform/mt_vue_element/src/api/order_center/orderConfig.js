import { request } from '@/base/utils/request'

//获取所有订单配置
export function getOrderConfigList(page, biz_id) {
  return request({
    url: './order_center/config/config/?page=' + page + '&biz_id=' + biz_id,
    method: 'get'
  })
}

//自动生成订单配置
export function postAutoCreateOrderConfig(data) {
  return request({
    url: './order_center/config/auto/create/',
    method: 'post',
    data
  })
}

//更新工单配置
export function putOrderConfig(id, data) {
  return request({
    url: './order_center/config/config/' + id + '/',
    method: 'put',
    data
  })
}

// 获取流程
export function getProcessManagement(page, biz_id) {
  return request({
    url: './order_center/process/config/?page=' + page + '&biz_id=' + biz_id,
    method: 'get'
  })
}

// 获取审批流
export function getApprovalFlowList(process_id) {
  return request({
    url: './order_center/process/approval/flow/?process_id=' + process_id,
    method: 'get'
  })
}

// 更新审批流
export function putApprovalFlow(id, data) {
  return request({
    url: './order_center/process/approval/flow/' + id + '/',
    method: 'put',
    data
  })
}

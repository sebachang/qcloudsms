import { request } from '@/base/utils/request'

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


import { request } from '@/base/utils/request'

//创建订单
export function postOrder(data) {
  return request({
    url: './order_center/order/order/',
    method: 'post',
    data
  })
}

//获取所有工单
export function getOrderList(page, audit_state, biz_id) {
  return request({
    url: './order_center/order/order/?page=' + page + '&audit_state=' + audit_state + '&biz_id=' + biz_id,
    method: 'get'
  })
}

//更新工单
export function updateOrderList(id, data) {
  return request({
    url: './order_center/order/order/' + id + '/',
    method: 'put',
    data
  })
}

//获取我提交的工单
export function getMyOrderList(page, biz_id) {
  return request({
    url: './order_center/order/my/order/?page=' + page + '&biz_id=' + biz_id,
    method: 'get'
  })
}

//获取我审批的工单
export function getMyApprovalOrderList(page, biz_id) {
  return request({
    url: './order_center/order/my/approval/order/?page=' + page + '&biz_id=' + biz_id,
    method: 'get'
  })
}

//获取订单审批记录
export function getApprovalOrder(order_id) {
  return request({
    url: './order_center/order/order/approval/record/?order_id=' + order_id,
    method: 'get'
  })
}

//审批订单
export function postApprovalOrder(data) {
  return request({
    url: './order_center/order/order/approval/record/',
    method: 'post',
    data
  })
}

//获取是否有审批权限
export function getApprovalPermission(order_id) {
  return request({
    url: './order_center/order/approval/permission/?order_id=' + order_id,
    method: 'get'
  })
}

//获取订单审批流程
export function getApprovalFlow(order_id) {
  return request({
    url: './order_center/order/order/approval/flow/?order_id=' + order_id,
    method: 'get'
  })
}

//获取子订单
export function getSuborder(order_id) {
  return request({
    url: './order_center/order/suborder/?order_id=' + order_id,
    method: 'get'
  })
}

//获取搜索订单
export function getSearchOrder(page, biz_id, order_value) {
  return request({
    url: './order_center/order/search/order/?page=' + page + '&biz_id=' + biz_id + '&search=' + order_value + '&ordering=-id'
  })
}

//获取异常工单
export function getExceptionOrderList(page, biz_id) {
  return request({
    url: './order_center/order/exception/order/?page=' + page + '&biz_id=' + biz_id,
    method: 'get'
  })
}

//重新执行任务
export function postJobExecute(data) {
  return request({
    url: './order_center/order/job/execute/',
    method: 'post',
    data
  })
}

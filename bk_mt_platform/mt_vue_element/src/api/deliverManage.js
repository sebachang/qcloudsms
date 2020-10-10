import { request } from '@/base/utils/request'

// 获取平台信息
export function getPlatformList(biz_id) {
  return request({
    url: './deliver_manage/platform/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

// 新增平台信息
export function postPlatform(data) {
  return request({
    url: './deliver_manage/platform/',
    method: 'post',
    data
  })
}

// 更新平台信息
export function putPlatform(id, data) {
  return request({
    url: './deliver_manage/platform/' + id + '/',
    method: 'put',
    data
  })
}

// 删除平台信息
export function deletePlatform(id) {
  return request({
    url: './deliver_manage/platform/' + id + '/',
    method: 'delete'
  })
}

// 获取主机配置
export function getHostList(biz_id) {
  return request({
    url: './deliver_manage/host/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

// 新增主机配置
export function postHostProfile(data) {
  return request({
    url: './deliver_manage/host/',
    method: 'post',
    data
  })
}

// 更新主机配置
export function putHostProfile(id, data) {
  return request({
    url: './deliver_manage/host/' + id + '/',
    method: 'put',
    data
  })
}

// 删除主机配置
export function deleteHostProfile(id) {
  return request({
    url: './deliver_manage/host/' + id + '/',
    method: 'delete'
  })
}

// 获取机房配置
export function getCenterList(biz_id) {
  return request({
    url: './deliver_manage/center/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

// 新增机房配置
export function postCenter(data) {
  return request({
    url: './deliver_manage/center/',
    method: 'post',
    data
  })
}

// 更新机房配置
export function putCenter(id, data) {
  return request({
    url: './deliver_manage/center/' + id + '/',
    method: 'put',
    data
  })
}

// 删除机房配置
export function deleteCenter(id) {
  return request({
    url: './deliver_manage/center/' + id + '/',
    method: 'delete'
  })
}

// 获取平台和主机关联
export function getPlatformHostMap(pid) {
  return request({
    url: './deliver_manage/map/platform/host/',
    method: 'get',
    params: { pid }
  })
}

// 获取平台和机房关联
export function getPlatformCenterMap(pid) {
  return request({
    url: './deliver_manage/map/platform/center/',
    method: 'get',
    params: { pid }
  })
}

// 新增平台和主机关联
export function postPlatformHostMap(data) {
  return request({
    url: './deliver_manage/map/platform/host/',
    method: 'post',
    data
  })
}

// 新增平台和机房关联
export function postPlatformCenterMap(data) {
  return request({
    url: './deliver_manage/map/platform/center/',
    method: 'post',
    data
  })
}

// 获取交付所有工单
export function getDeliverOrderList(page, biz_id) {
  return request({
    url: './deliver_manage/deliver/order/',
    method: 'get',
    params: { page, biz_id }
  })
}

// 获取我的交付工单
export function getMyDeliverOrderList(page, biz_id) {
  return request({
    url: './deliver_manage/my/deliver/order/',
    method: 'get',
    params: { page, biz_id }
  })
}

// 获取搜索交付详情
export function getSearchDeliverDetail(params) {
  return request({
    url: './deliver_manage/search/deliver/detail/',
    method: 'get',
    params: params
  })
}

// 获取交付订单详情
export function getDeliverDetailList(page, order_id, flag, page_size) {
  return request({
    url: './deliver_manage/deliver/detail/',
    method: 'get',
    params: { page, order_id, flag, page_size }
  })
}

// 添加交付订单详情
export function addDeliverDetail(data) {
  return request({
    url: './deliver_manage/deliver/detail/',
    method: 'post',
    data
  })
}

// 更新交付订单详情
export function putDeliverDetail(id, data) {
  return request({
    url: './deliver_manage/deliver/detail/' + id + '/',
    method: 'put',
    data
  })
}

// 删除交付订单详情
export function deleteDeliverDetail(id) {
  return request({
    url: './deliver_manage/deliver/detail/' + id + '/',
    method: 'delete'
  })
}

// excel 批量创建交付订单详情
export function postDeliverDetailUpload(fileobj, id) {
  var param = new FormData()
  param.append('files', fileobj)
  param.append('id', id)
  return request({
    method: 'post',
    url: './deliver_manage/deliver/upload/detail/',
    headers: { 'Content-Type': 'multipart/form-data' },
    data: param
  })
}

// 根据状态获取清退工单
export function getClearanceOrderList(page, biz_id, clearance_flag) {
  return request({
    url: './deliver_manage/clearance/order/?page=' + page + '&biz_id=' + biz_id + '&clearance_flag=' + clearance_flag,
    method: 'get'
  })
}

// 根据状态获取清退工单
export function getClearanceDetailList(page, page_size, order_id, biz_id, clearance_flag) {
  return request({
    url: './deliver_manage/clearance/detail/?page=' + page + '&page_size=' + page_size + '&order_id=' + order_id + '&biz_id=' + biz_id + '&clearance_flag=' + clearance_flag,
    method: 'get'
  })
}

// 更新清退详情
export function putClearanceDetail(id, data) {
  return request({
    url: './deliver_manage/clearance/detail/' + id + '/',
    method: 'put',
    data
  })
}

// 获取搜索清退详情
export function getSearchClearanceDetail(params) {
  return request({
    url: './deliver_manage/search/clearance/detail/',
    method: 'get',
    params: params
  })
}

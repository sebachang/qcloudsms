import { request, raw_request } from '@/base/utils/request'

// 登录时, 获取业务, 用户角色对应权限
export function getRoleSettingsByLogin(biz_id, name) {
  return request({
    url: '/permission/user_routes/',
    method: 'get',
    params: { biz_id: biz_id, name: name }
  })
}

// 获取所有的role
export function getRoutes(params) {
  return request({
    url: './permission/route/',
    method: 'get',
    params: params
  })
}

// 获取某个role
export function getRoute(id) {
  return request({
    url: './permission/route/' + id + '/',
    method: 'get'
  })
}

// 删除某个role
export function deleteRoute(id) {
  return request({
    url: './permission/route/' + id + '/',
    method: 'delete'
  })
}

// 添加role
export function addRoute(data) {
  return request({
    url: './permission/route/',
    method: 'post',
    data
  })
}

// 更新role
export function updateRoute(id, data) {
  return request({
    url: `./permission/route/` + id + '/',
    method: 'put',
    data
  })
}

// ///////////////////////////////////////////////////////////////////////////
// 获取所有的group
export function getGroups(params) {
  return request({
    url: './permission/group/',
    method: 'get',
    params: params
  })
}

export function getGroupList(id) {
  return request({
    url: './permission/group_list/' + id + '/',
    method: 'get'
  })
}

// 获取某个group
export function getGroup(id) {
  return request({
    url: './permission/group/' + id + '/',
    method: 'get'
  })
}

// 删除某个group
export function deleteGroup(id) {
  return request({
    url: './permission/group/' + id + '/',
    method: 'delete'
  })
}

// 添加group
export function addGroup(data) {
  return request({
    url: './permission/group/',
    method: 'post',
    data
  })
}

// 更新group
export function updateGroup(id, data) {
  return request({
    url: `./permission/group/` + id + '/',
    method: 'put',
    data
  })
}

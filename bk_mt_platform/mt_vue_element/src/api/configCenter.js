import { request } from '@/base/utils/request'

export async function getConfigTemplate(biz_id) {
  return request({
    url: './config_center/template/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

export async function updateConfigTemplate(biz_id, key, data) {
  return request({
    url: './config_center/template/' + key + '/',
    method: 'put',
    params: { biz_id: biz_id },
    data
  })
}

export async function deleteConfigTemplate(biz_id, key) {
  return request({
    url: './config_center/template/' + key + '/',
    method: 'delete',
    params: { biz_id: biz_id }
  })
}

export async function addConfigTemplate(data) {
  return request({
    url: './config_center/template/',
    method: 'post',
    data
  })
}

export async function getConfigKV(biz_id) {
  return request({
    url: './config_center/kv/',
    params: { biz_id: biz_id }
  })
}

export async function addConfigKV(data) {
  return request({
    url: './config_center/kv/',
    method: 'post',
    data
  })
}

export async function updateConfigKV(biz_id, key, data) {
  return request({
    url: './config_center/kv/' + key + '/',
    method: 'put',
    params: { biz_id: biz_id },
    data
  })
}

export async function deleteConfigKV(biz_id, key) {
  return request({
    url: './config_center/kv/' + key + '/',
    method: 'delete',
    params: { biz_id: biz_id }
  })
}

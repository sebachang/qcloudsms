import { request, raw_request } from '@/base/utils/request'

export async function getSystemConfig(biz_id) {
  return request({
    url: './system_config/setting_generic/get_list/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

export function addSystemConfig(biz_id, data) {
  return request({
    url: '/system_config/setting/',
    method: 'post',
    params: { biz_id: biz_id },
    data
  })
}

export function updateSystemConfig(config_key, data, biz_id) {
  return request({
    url: `/system_config/setting/` + config_key + '/',
    method: 'put',
    params: { biz_id: biz_id },
    data
  })
}

export async function getSystemConfigKey(biz_id, key) {
  return request({
    url: './system_config/sc/',
    method: 'get',
    params: { biz_id: biz_id, config_key: key }
  })
}

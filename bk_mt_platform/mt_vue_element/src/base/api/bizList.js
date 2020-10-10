import { request } from '@/base/utils/request'

export function getBizList(currName) {
  return request({
    url: '/api/cmdb/get_biz_list_by_user/',
    method: 'get',
    params: { name: currName }
  })
}

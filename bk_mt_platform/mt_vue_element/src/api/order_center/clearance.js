import { request } from '@/base/utils/request'

// 获取清退列表
export function getCmdbClearanceList(biz_id, page) {
  return request({
    url: './order_center/clearance/cmdb/clearance/',
    method: 'get',
    params: { biz_id, page }
  })
}

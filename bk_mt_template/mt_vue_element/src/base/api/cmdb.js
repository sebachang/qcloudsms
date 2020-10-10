import { request } from '@/base/utils/request'

export async function searchHost(biz_id, opts) {
  const page_limit = opts.pageSize
  const page_start = opts.pageStart
  const ip = opts.ip
  return request({
    url: './api/cmdb/search_host/',
    timeout: 60000,
    params: { biz_id, page_limit, page_start, ip }
  })
}

export async function searchHost2(biz_id, data) {
  return request({
    url: './api/cmdb/search_host2/',
    timeout: 60000,
    params: { biz_id },
    method: 'post',
    data
  })
}

export async function searchBizInstTopo(biz_id) {
  return request({
    url: './api/cmdb/search_biz_inst_topo/',
    params: { biz_id: biz_id }
  })
}

export async function searchCustomQuery(biz_id) {
  return request({
    url: './api/cmdb/search_custom_query/',
    params: { biz_id }
  })
}

export async function searchInstByObject(data) {
  return request({
    url: './api/cmdb/search_inst_by_object/',
    method: 'post',
    data
  })
}

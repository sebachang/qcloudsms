import { request } from '../utils/request'

export async function getChangelog(biz_id, start, end) {
  return request({
    url: './audit/changelog/',
    params: { biz_id: biz_id, start: start, end: end }
  })
}

export async function addLog(biz_id, data) {
  return request({
    url: './audit/changelog/',
    method: 'post',
    params: { biz_id },
    data
  })
}

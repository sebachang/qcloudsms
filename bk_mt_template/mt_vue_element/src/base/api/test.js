import { request, raw_request } from '@/base/utils/request'

export async function test_example(biz_id) {
  return request({
    url: './example/test_example/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

export async function test_generic_api(biz_id) {
  return request({
    url: './example/generic_view/test_generic_api/',
    method: 'get',
    params: { biz_id: biz_id }
  })
}

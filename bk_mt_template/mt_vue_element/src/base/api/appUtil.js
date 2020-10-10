import { request, raw_request } from '@/base/utils/request'
import url from 'url'

export async function get_jump_site(router) {
  return request({
    url: './api/app_util/get_jump_site/',
    method: 'get',
    params: { router: router }
  })
}

export async function get_download_site(router) {
  return request({
    url: './api/app_util/get_download_site/',
    method: 'get',
    params: { router: router }
  })
}

export async function get_api_root() {
  const { site } = await request({
    url: './api/app_util/get_jump_site/',
    method: 'get',
    params: {}
  })
  return url.resolve(site, process.env['VUE_APP_BASE_API'] + '/')
}

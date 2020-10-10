import { request } from '@/base/utils/request'

export async function getChannels(biz_id) {
  return request({
    url: './notify_manage/channel/',
    params: { biz_id }
  })
}

export async function addChannel(data) {
  return request({
    url: './notify_manage/channel/',
    method: 'post',
    data
  })
}

export async function updateChannel(biz_id, id, data) {
  return request({
    url: `./notify_manage/channel/${id}/`,
    method: 'put',
    params: { biz_id },
    data
  })
}

export async function deleteChannel(biz_id, id) {
  return request({
    url: `./notify_manage/channel/${id}/`,
    method: 'delete',
    params: { biz_id }
  })
}

export async function getRules(biz_id) {
  return request({
    url: './notify_manage/rule/',
    params: { biz_id }
  })
}

export async function addRule(data) {
  return request({
    url: './notify_manage/rule/',
    method: 'post',
    data
  })
}

export async function updateRule(biz_id, id, data) {
  return request({
    url: `./notify_manage/rule/${id}/`,
    method: 'put',
    params: { biz_id },
    data
  })
}

export async function deleteRule(biz_id, id) {
  return request({
    url: `./notify_manage/rule/${id}/`,
    method: 'delete',
    params: { biz_id }
  })
}

export async function getTags() {
  return request({
    url: './notify_manage/tag/taglist/'
  })
}

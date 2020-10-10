import { request } from '@/base/utils/request'

export async function getProcesses(biz_id) {
  return request({
    url: './process_manage/process/',
    params: { biz_id: biz_id }
  })
}

export async function addProcess(data) {
  return request({
    url: './process_manage/process/',
    method: 'post',
    data
  })
}

export async function updateProcess(biz_id, id, data) {
  return request({
    url: './process_manage/process/' + id + '/',
    method: 'put',
    params: { biz_id: biz_id },
    data
  })
}

export async function deleteProcess(biz_id, id) {
  return request({
    url: './process_manage/process/' + id + '/',
    method: 'delete',
    params: { biz_id: biz_id }
  })
}

export async function getInstances(biz_id, currentPage, pageSize, search) {
  return request({
    url: './process_manage/instance/',
    params: { biz_id: biz_id, page: currentPage, page_size: pageSize, search: search }
  })
}

export async function addInstance(data) {
  return request({
    url: './process_manage/instance/',
    method: 'post',
    data
  })
}

export async function updateInstance(biz_id, id, data) {
  return request({
    url: './process_manage/instance/' + id + '/',
    method: 'put',
    params: { biz_id: biz_id },
    data
  })
}

export async function deleteInstance(biz_id, id) {
  return request({
    url: './process_manage/instance/' + id + '/',
    method: 'delete',
    params: { biz_id: biz_id }
  })
}

export async function runOperation(biz_id, id, action) {
  return request({
    url: './process_manage/operation/' + id + '/' + action + '/',
    method: 'post',
    params: { biz_id: biz_id }
  })
}

export async function runBatchOperation(biz_id, ids, action) {
  return request({
    // url: './process_manage/operation/' + id + '/' + action + '/',
    method: 'post',
    params: { biz_id: biz_id }
  })
}

export async function getJobStatus(biz_id, job_id) {
  return request({
    url: './process_manage/operation/job_status/' + job_id + '/',
    params: { biz_id: biz_id }
  })
}

export async function getOperationHistory(biz_id) {
  return request({
    url: './task/taskinstance/',
    params: { job__job_uuid: 'bfc0a2ea-71a7-40c0-b40a-7334798d4afc' }
  })
}

export async function getInstanceStatus(biz_id, id) {
  return request({
    url: './process_manage/instance/' + id + '/status/',
    params: { biz_id: biz_id }
  })
}

export async function getBkJobLog(biz_id, id) {
  return request({
    url: './process_manage/job_log/' + id + '/',
    params: { biz_id: biz_id }
  })
}

export async function getInstanceConfig(biz_id, id) {
  return request({
    url: './process_manage/' + id + '/config_md5/',
    params: { biz_id: biz_id }
  })

}

export async function getPackageList(biz_id) {
  return request({
    url: './process_manage/package/',
    params: { biz_id: biz_id }
  })
}

export async function deletePackage(biz_id, file) {
  return request({
    url: `./process_manage/package/${file}/`,
    method: 'delete',
    params: { biz_id: biz_id }
  })
}

export async function uploadPackage(biz_id, data) {
  return request({
    url: `./process_manage/package/`,
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    params: { biz_id: biz_id },
    timeout: 600000,
    data
  })
}

export async function downloadPackage(biz_id, file) {
  return request({
    url: `./process_manage/download/${file}/`,
    method: 'get',
    params: {biz_id}
  })
}

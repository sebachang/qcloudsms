import { request, raw_request } from '@/base/utils/request'

// 获取单个实例
export function getTaskInstance(id) {
  return request({
    url: './task/taskinstance/' + id + '/',
    method: 'get'
  })
}

// 获取所有实例
export function getTaskInstances(params) {
  return request({
    url: './task/taskinstance/',
    method: 'get',
    params: params
  })
}

// 获取实例日志
export function getJobs(params) {
  return request({
    url: './task/job/',
    method: 'get',
    params: params
  })
}

// 删除作业
export function deleteJob(id) {
  return request({
    url: './task/job/' + id + '/',
    method: 'delete'
  })
}

// 添加作业
export function addJob(data) {
  return request({
    url: './task/job/',
    method: 'post',
    data
  })
}

// 更新作业
export function updateJob(id, data) {
  return request({
    url: `./task/job/` + id + '/',
    method: 'put',
    data
  })
}

// 执行任务
export function runJob(id, data) {
  return request({
    url: './task/task/' + id + '/',
    method: 'post',
    data
  })
}

// 获取任务最进一次执行状态
export function getTaskLog(id) {
  return request({
    url: './task/log/' + id + '/',
    method: 'get'
  })
}

// 注册jobs
export function registerJobs(data) {
  return request({
    url: './task/register/',
    method: 'post',
    data
  })
}


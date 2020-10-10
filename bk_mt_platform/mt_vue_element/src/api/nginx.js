import {request, raw_request} from '@/base/utils/request'

//////////////Cluster/////////////
export function getClusters(params) {
  return request({
    url: './nginx/cluster/',
    method: 'get',
    params: params
  })
}

export function getCluster(id) {
  return request({
    url: './nginx/cluster/' + id + '/',
    method: 'get',
  })
}

export function deleteCluster(id) {
  return request({
    url: './nginx/cluster/' + id + '/',
    method: 'delete',
  })
}

export function addCluster(data) {
  return request({
    url: './nginx/cluster/',
    method: 'post',
    data
  })
}

export function updateCluster(id, data) {
  return request({
    url: `./nginx/cluster/` + id + '/',
    method: 'put',
    data
  })
}

//////////////Config/////////////
export function getConfigs(params) {
  return request({
    url: './nginx/config/',
    method: 'get',
    params: params
  })
}

export function getConfigList() {
  return request({
    url: './nginx/config_list/',
    method: 'get'
  })
}

export function getConfigListById(id) {
  return request({
    url: './nginx/config_list/'+ id + '/',
    method: 'get'
  })
}

export function getConfig(id) {
  return request({
    url: './nginx/config/' + id + '/',
    method: 'get',
  })
}

export function deleteConfig(id) {
  return request({
    url: './nginx/config/' + id + '/',
    method: 'delete',
  })
}

export function addConfig(data) {
  return request({
    url: './nginx/config/',
    method: 'post',
    data
  })
}

export function updateConfig(id, data) {
  return request({
    url: `./nginx/config/` + id + '/',
    method: 'put',
    data
  })
}

//////////////Vhost/////////////
export function getVhosts(params) {
  return request({
    url: './nginx/vhost/',
    method: 'get',
    params: params
  })
}

export function getVhostList() {
  return request({
    url: './nginx/vhost_list/',
    method: 'get'
  })
}

export function getVhost(id) {
  return request({
    url: './nginx/vhost/' + id + '/',
    method: 'get',
  })
}

export function deleteVhost(id) {
  return request({
    url: './nginx/vhost/' + id + '/',
    method: 'delete',
  })
}

export function addVhost(data) {
  return request({
    url: './nginx/vhost/',
    method: 'post',
    data
  })
}

export function updateVhost(id, data) {
  return request({
    url: `./nginx/vhost/` + id + '/',
    method: 'put',
    data
  })
}


////////////// Template/////////////
export function getTemplateBase(data) {
  return request({
    url: './nginx/template_base/',
    method: 'post',
    data
  })
}

export function getTemplateBaseByCert(id) {
  return request({
    url: './nginx/template_base/' + id + '/',
    method: 'get',
  })
}

export function getTemplateVhost(id, data) {
  return request({
    url: `./nginx/template_vhost/` + id + '/',
    method: 'put',
    data
  })
}

////////////// Instance/////////////
export function getInstance(id) {
  return request({
    url: './nginx/instance/' + id + '/',
    method: 'get',
  })
}

////////////// Job/////////////
export function getJobLog(params) {
  return request({
    url: './nginx/job/',
    method: 'get',
    params: params
  })
}

////////////// Operator/////////////
export function addOperator(id, data) {
  return request({
    url: `./nginx/operator/` + id + '/',
    method: 'put',
    data
  })
}

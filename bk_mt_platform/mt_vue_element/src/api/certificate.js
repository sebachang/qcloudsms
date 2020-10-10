import {request, raw_request} from '@/base/utils/request'

//////////////Cert/////////////
export function getCerts(params) {
  return request({
    url: './certificate/cert/',
    method: 'get',
    params: params
  })
}

export function getCertList() {
  return request({
    url: './certificate/cert_list/',
    method: 'get'
  })
}

export function getCert(id) {
  return request({
    url: './certificate/cert/' + id + '/',
    method: 'get',
  })
}

export function deleteCert(id) {
  return request({
    url: './certificate/cert/' + id + '/',
    method: 'delete',
  })
}

export function addCert(data) {
  return request({
    url: './certificate/cert/',
    method: 'post',
    data
  })
}

export function updateCert(id, data) {
  return request({
    url: `./certificate/cert/` + id + '/',
    method: 'put',
    data
  })
}


//////////////Domain/////////////
export function getDomains(params) {
  return request({
    url: './certificate/domain/',
    method: 'get',
    params: params
  })
}

export function getDomainList() {
  return request({
    url: './certificate/domain_list/',
    method: 'get'
  })
}

export function deleteDomain(id) {
  return request({
    url: './certificate/domain/' + id + '/',
    method: 'delete',
  })
}

export function addDomain(data) {
  return request({
    url: './certificate/domain/',
    method: 'post',
    data
  })
}

export function updateDomain(id, data) {
  return request({
    url: `./certificate/domain/` + id + '/',
    method: 'put',
    data
  })
}

export function checkDomain(id) {
  return request({
    url: './certificate/check/' + id + '/',
    method: 'get',
  })
}

//////////////Cluster/////////////
export function getClusters(params) {
  return request({
    url: './certificate/cluster/',
    method: 'get',
    params: params
  })
}

export function deleteCluster(id) {
  return request({
    url: './certificate/cluster/' + id + '/',
    method: 'delete',
  })
}

export function addCluster(data) {
  return request({
    url: './certificate/cluster/',
    method: 'post',
    data
  })
}

export function updateCluster(id, data) {
  return request({
    url: `./certificate/cluster/` + id + '/',
    method: 'put',
    data
  })
}

//////////////Register/////////////
export function registerCert(data) {
  return request({
    url: './certificate/register/',
    method: 'post',
    timeout: 60000,
    data
  })
}

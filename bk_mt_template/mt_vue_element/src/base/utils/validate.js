/**
 * Created by jiachenpan on 16/11/18.
 */

export function validateName(name) {
  return name !== ''
}

// 角色验证和配置
export const UserRoleInfo = {
  ordinary: { value: 0, label: '普通用户' },
  admin: { value: 1, label: '管理员' },
  developer: { value: 2, label: '开发者' },
  functor: { value: 3, label: '职能化' },
  auditor: { value: 4, label: '审计员' }
}

export function validateRole(role) {
  return role >= UserRoleInfo.ordinary.value && role <= UserRoleInfo.auditor.value
}

export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

export function validUsername(str) {
  const valid_map = ['admin', 'editor']
  return valid_map.indexOf(str.trim()) >= 0
}

export function validURL(url) {
  const reg = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return reg.test(url)
}

export function validLowerCase(str) {
  const reg = /^[a-z]+$/
  return reg.test(str)
}

export function validUpperCase(str) {
  const reg = /^[A-Z]+$/
  return reg.test(str)
}

export function validAlphabets(str) {
  const reg = /^[A-Za-z]+$/
  return reg.test(str)
}

export function validEmail(email) {
  const reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return reg.test(email)
}

export function isString(str) {
  if (typeof str === 'string' || str instanceof String) {
    return true
  }
  return false
}

export function isArray(arg) {
  if (typeof Array.isArray === 'undefined') {
    return Object.prototype.toString.call(arg) === '[object Array]'
  }
  return Array.isArray(arg)
}

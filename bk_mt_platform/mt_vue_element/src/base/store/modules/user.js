import { testAPI, logout, getInfo, getPermission } from '@/base/api/user'
import { validateName, validateRole } from '@/base/utils/validate'
import { getRoleSettingsByLogin } from '@/base/api/roleSetting'

const state = {
  name: '',
  role: -1,
  permission: []
}

const mutations = {
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_ROLE: (state, role) => {
    state.role = role
  },
  SET_PERMISSION: (state, permission) => {
    state.permission = permission
  }
}

const actions = {
  // test api
  testAPI({ commit }, data) {
    return new Promise((resolve, reject) => {
      testAPI(data).then(data => {
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo().then(data => {
        const { bk_username, bk_role } = data
        if (validateName(bk_username) && validateRole(bk_role)) {
          commit('SET_NAME', bk_username)
          commit('SET_ROLE', bk_role)
          resolve({ 'name': bk_username, 'role': bk_role })
        } else {
          reject(new Error('用户和角色数据错误: ' + bk_username + '|' + bk_role))
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  getPermission({ commit, state }, info) {
    return new Promise((resolve, reject) => {
      getRoleSettingsByLogin(info.bizId, info.name).then(data => {
        const permission = JSON.parse(data.setting)
        commit('SET_PERMISSION', permission)
        resolve(permission)
      }).catch(error => {
        resolve([])
      })
    })
  },

  // remove token
  resetUserInfo({ commit }) {
    return new Promise(resolve => {
      commit('SET_NAME', '')
      commit('SET_ROLE', -1)
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

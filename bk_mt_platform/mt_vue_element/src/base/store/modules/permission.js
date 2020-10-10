import path from 'path'
import { UserRoleInfo } from '@/base/utils/validate'
import { getRoutesByPermission } from '@/base/router/utils'
import { constantRoutes, permissionGroup, permissionPath, permissionRoutes, permissionUser } from '@/base/router'
import { getAllRoutes } from '@/base/utils/routes'

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.routes = constantRoutes.concat(routes)
    state.addRoutes = routes
  }
}

const actions = {
  generateRoutes({ commit }, info) {
    return new Promise(async resolve => {
      // 如果是admin, 强制拥有权限设置页面
      const permission = [...info['permission']]

      if (info['role'] === UserRoleInfo.admin.value) {
        if (permission.indexOf(permissionPath) == -1) {
          permission.push(permissionPath)
        }

        const permissionUserPath = path.resolve(permissionPath, permissionUser)
        if (permission.indexOf(permissionUserPath) == -1) {
          permission.push(permissionUserPath)
        }

        const permissionGroupPath = path.resolve(permissionPath, permissionGroup)
        if (permission.indexOf(permissionGroupPath) == -1) {
          permission.push(permissionGroupPath)
        }

        const permissionRoutePath = path.resolve(permissionPath, permissionRoutes)
        if (permission.indexOf(permissionRoutePath) == -1) {
          permission.push(permissionRoutePath)
        }
      }
      const allRoutes = await getAllRoutes()
      const routes = getRoutesByPermission(allRoutes, permission)
      console.log(routes)
      commit('SET_ROUTES', routes)
      resolve(routes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

import router from './router'
import store from './store'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { MessageBox, Message } from 'element-ui'
import { UserRoleInfo, validateName, validateRole } from './utils/validate'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  // cookie bk_token是http only, 客户端无法获取, django后台会在cookie过期时自动重定向到蓝鲸登录页面
  // 使用vuex里面是否有name/role信息判断玩家是否登录
  const hasUserInfo = validateName(store.getters.name) && validateRole(store.getters.role)
  if (hasUserInfo) {
    next()
  } else {
    try {
      // get user name, role
      const { name, role } = await store.dispatch('user/getInfo')

      // get biz list
      const { bizList, currBiz } = await store.dispatch('bizList/getBizList', name)
      if (bizList.length == 0 || currBiz == '') {
        MessageBox.alert('当前用户蓝鲸业务biz列表为空, 请联系蓝鲸管理员配置业务biz权限!', '提示', {
          confirmButtonText: '确定' })
        NProgress.done()
        return
      }

      // permission
      const permission = await store.dispatch('user/getPermission', { bizId: currBiz, name: name })
      // if (permission.length == 0 && role != UserRoleInfo.admin.value) {
      //   MessageBox.alert('当前用户功能权限为空, 请联系管理员配置功能权限!', '提示', {
      //     confirmButtonText: '确定' })
      //   NProgress.done()
      //   return
      // }

      // generate accessible routes map based on roles
      const accessRoutes = await store.dispatch('permission/generateRoutes', { 'role': role, 'permission': permission })
      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      // hack method to ensure that addRoutes is complete
      // set the replace: true, so the navigation will not leave a history record
      next({ ...to, replace: true })
    } catch (error) {
      // 重定向到蓝鲸登录界面
      MessageBox.alert('登录流程出错: ' + error.message, '提示', {
        confirmButtonText: '确定' }).then(() => {
        location.reload()
        NProgress.done()
      })
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})

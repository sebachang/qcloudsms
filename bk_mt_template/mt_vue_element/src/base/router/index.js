import Vue from 'vue'
import Router from 'vue-router'
/* Layout */
import Layout from '../layout'

Vue.use(Router)

/* Router Modules */

/** note: sub-menu only appear when children.length>=1
 *  detail see  https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 **/

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    will control the page roles (you can set multiple roles)
    title: 'title'               the name show in sub-menu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if true, the page will no be cached(default is false)
    breadcrumb: false            if false, the item will hidden in breadcrumb(default is true)
    affix: true                  if true, the tag will affix in the tags-view
  }
 **/

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 * */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('../views/redirect/index')
      }
    ]
  },
  {
    path: '/404',
    component: () => import('../views/errorPage/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('../views/errorPage/401'),
    hidden: true
  },
  {
    path: '*',
    component: () => import('../views/errorPage/404'),
    hidden: true
  },
  {
    path: '',
    component: Layout,
    redirect: 'dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('../views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: '首页', icon: 'dashboard', noCache: true, affix: true }
      }
    ]
  }
]

export const permissionPath = '/permission'
export const permissionRoutes = 'route'
export const permissionUser = 'user'
export const permissionGroup = 'group'

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/audit',
    component: Layout,
    redirect: '/audit/changelog',
    alwaysShow: true,
    meta: {
      title: '操作审计',
      icon: 'audit'
    },
    children: [
      {
        path: 'changelog',
        component: () => import('../views/audit/changelog'),
        name: 'changelog',
        meta: { title: '变更历史', icon: 'history', noCache: true }
      }
    ]
  },
  {
    path: '/notify',
    component: Layout,
    redirect: '/notify/channel',
    alwaysShow: true,
    meta: {
      title: '通知管理',
      icon: 'notify'
    },
    children: [
      {
        path: 'channel',
        component: () => import('../views/notifyManage/channel'),
        name: 'channel',
        meta: {
          title: '通知通道',
          icon: 'channel',
          noCache: true
        }
      },
      {
        path: 'rule',
        component: () => import('../views/notifyManage/rule'),
        name: 'rule',
        meta: {
          title: '规则配置',
          icon: 'edit',
          noCache: true
        }
      }
    ]
  },
  {
    path: '/task',
    component: Layout,
    redirect: '/task/index',
    alwaysShow: true,
    meta: {
      title: '任务管理',
      icon: 'list'
    },
    children: [
      {
        path: 'job',
        component: () => import('../views/task/job'),
        name: 'job',
        meta: {
          title: '作业管理'
        }
      },
      {
        path: 'job_uuid/:uuid(\\S+)',
        component: () => import('../views/task/job_uuid'),
        name: 'job_uuid',
        meta: {
          title: '作业UUID',
          noCache: true
        },
        hidden: true
      },
      {
        path: 'job_module/:module(\\S+)',
        component: () => import('../views/task/job_module'),
        name: 'job_module',
        meta: {
          title: '作业模块',
          noCache: true
        },
        hidden: true
      },
      {
        path: 'taskinstance',
        component: () => import('../views/task/taskInstance'),
        name: 'taskinstance',
        meta: {
          title: '任务实例'
        }
      },
      {
        path: 'taskinstance_module/:module(\\S+)',
        component: () => import('../views/task/taskInstance_module'),
        name: 'taskinstance_module',
        meta: {
          title: '模块实例',
          noCache: true
        },
        hidden: true
      }
    ]
  },
  {
    path: '/systemConfig',
    component: Layout,
    redirect: '/systemConfig/index',
    alwaysShow: true,
    meta: {
      title: '系统管理',
      icon: 'star'
    },
    children: [
      {
        path: 'index',
        component: () => import('../views/systemConfig/index'),
        name: 'systemConfig',
        meta: { title: '系统配置', icon: 'edit', noCache: true }
      }
    ]
  },
  {
    path: permissionPath,
    component: Layout,
    redirect: permissionPath + '/index',
    alwaysShow: true,
    meta: {
      title: '权限管理',
      icon: 'lock'
    },
    children: [
      {
        path: permissionUser,
        component: () => import('../views/permission/user'),
        name: 'user',
        meta: {
          title: '用户管理'
        }
      },
      {
        path: permissionGroup,
        component: () => import('../views/permission/group'),
        name: 'group',
        meta: {
          title: '组管理'
        }
      },
      {
        path: permissionRoutes,
        component: () => import('../views/permission/route'),
        name: 'route',
        meta: {
          title: '路由授权'
        }
      }
    ]
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export default router

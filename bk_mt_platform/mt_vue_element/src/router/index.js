import router from '@/base/router'
import settings from '@/base/settings'
import Layout from '@/base/layout'

settings.load_route_func = async () => {
  return [
    {
      path: '/order',
      component: Layout,
      redirect: '/order/index',
      alwaysShow: true,
      meta: {
        title: '工单中心',
        icon: 'money'
      },
      children: [
        {
          path: 'orderConfig',
          component: () => import('@/views/order_center/orderConfig'),
          name: 'orderConfig',
          meta: {
            title: '工单配置'
          }
        },
        {
          path: 'order',
          component: () => import('@/views/order_center/order'),
          name: 'order',
          meta: {
            title: '工单详情'
          }
        },
        {
          path: 'order_table/:order_id(\\d*)',
          component: () => import('@/views/order_center/order'),
          name: 'order_table',
          meta: {
            title: '工单审批'
          },
          hidden: true
        },
        {
          path: 'deliver',
          component: () => import('@/views/order_center/deliver'),
          name: 'deliver',
          meta: {
            title: '交付申请'
          }
        },
        {
          path: 'clearance',
          component: () => import('@/views/order_center/clearance'),
          name: 'clearance',
          meta: {
            title: '清退申请'
          }
        },
        {
          path: 'release',
          component: () => import('@/views/order_center/release'),
          name: 'release',
          meta: {
            title: '发布申请'
          }
        },
        {
          path: 'domain',
          component: () => import('@/views/order_center/domain'),
          name: 'domain',
          meta: {
            title: '域名申请'
          }
        }]
    },
    {
      path: '/deliver',
      component: Layout,
      redirect: '/deliver/index',
      alwaysShow: true,
      meta: {
        title: '交付管理',
        icon: 'edit'
      },
      children: [
        {
          path: 'platfrom',
          component: () => import('@/views/deliverManage/platfrom'),
          name: 'platfrom',
          meta: {
            title: '厂商配置'
          }
        },
        {
          path: 'host',
          component: () => import('@/views/deliverManage/host'),
          name: 'host',
          meta: {
            title: '机型配置'
          }
        },
        {
          path: 'center',
          component: () => import('@/views/deliverManage/center'),
          name: 'center',
          meta: {
            title: '机房配置'
          }
        },
        {
          path: 'deliverOrder',
          component: () => import('@/views/deliverManage/deliverOrder'),
          name: 'deliverOrder',
          meta: {
            title: '交付详情'
          }
        },
        {
          path: 'clearanceOrder',
          component: () => import('@/views/deliverManage/clearanceOrder'),
          name: 'clearanceOrder',
          meta: {
            title: '清退详情'
          }
        }
      ]
    },
    {
      path: '/certificate',
      component: Layout,
      redirect: '/certificate/index',
      alwaysShow: true,
      meta: {
        title: '证书管理',
        icon: 'cert'
      },
      children: [
        {
          path: 'cert',
          component: () => import('@/views/certificate/cert'),
          name: 'cert',
          meta: {
            title: '证书'
          }
        },
        {
          path: 'domain',
          component: () => import('@/views/certificate/domain'),
          name: 'domain',
          meta: {
            title: '域名'
          }
        },
        {
          path: 'cluster',
          component: () => import('@/views/certificate/cluster'),
          name: 'cluster',
          meta: {
            title: '集群'
          }
        }
      ]
    }, {
      path: '/nginx',
      component: Layout,
      redirect: '/nginx/index',
      alwaysShow: true,
      meta: {
        title: 'Nginx管理',
        icon: 'international'
      },
      children: [
        {
          path: 'cluster',
          component: () => import('@/views/nginx/cluster'),
          name: 'cluster',
          meta: {
            title: '集群管理'
          }
        }, {
          path: 'config',
          component: () => import('@/views/nginx/config'),
          name: 'config',
          meta: {
            title: '配置管理'
          }
        },
      ]
    },
    {
      path: '/configCenter',
      component: Layout,
      redirect: '/configCenter/kv',
      alwaysShow: true,
      meta: {
        title: '配置中心',
        icon: 'excel'
      },
      children: [
        {
          path: 'kv',
          component: () => import('@/views/configCenter/kv'),
          name: 'kv',
          meta: {title: '配置项', icon: 'storage', noCache: true}
        },
        {
          path: 'template',
          component: () => import('@/views/configCenter/configTemplate'),
          name: 'template',
          meta: {title: '配置模板', icon: 'file', noCache: true}
        }
      ]
    },
    {
      path: '/processManage',
      component: Layout,
      name: 'processManage',
      meta: {title: '进程管理', icon: 'gear', noCache: true},
      redirect: '/processManage/instance',
      children: [{
        path: 'instance',
        name: 'instance',
        component: () => import('@/views/processManage/instance'),
        meta: {title: '进程实例', icon: 'gear', noCache: true}
      }, {
        path: 'process',
        name: 'process',
        component: () => import('@/views/processManage/process'),
        meta: {title: '进程列表', icon: 'list', noCache: true}
      }, {
        path: 'package',
        name: 'package',
        component: () => import('@/views/processManage/package'),
        meta: {title: '程序包管理', icon: 'zip', noCache: true}
      }]
    }
  ]
}

export default router

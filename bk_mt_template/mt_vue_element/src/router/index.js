import router from '@/base/router'
import settings from '@/base/settings'
import Layout from '@/base/layout'

settings.load_route_func = async() => {
  return [
    {
      path: '/example',
      component: Layout,
      noCache: true,
      children: [
        { path: 'example', component: () => import('@/views/example/index'), meta: { title: '示例', icon: 'el-icon-info' }}
      ]
    }
  ]
}

export default router

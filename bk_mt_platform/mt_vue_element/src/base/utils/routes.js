import { asyncRoutes } from '@/base/router'
import settings from '@/base/settings'

export async function getAllRoutes() {
  let allRoutes = []
  if (settings.load_route_func) {
    allRoutes = allRoutes.concat(await settings.load_route_func())
  }
  allRoutes = allRoutes.concat(asyncRoutes)
  return allRoutes
}

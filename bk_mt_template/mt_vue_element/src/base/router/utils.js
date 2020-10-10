import path from 'path'

// 根据权限生成路径
export function getRoutesByPermission(routes, permission) {
  const result = { children: [] }
  routes.forEach(route => {
    filterRoutes('', route, permission, result)
  })

  return result.children
}

// 递归函数, 过滤路由表
function filterRoutes(parentPath, route, permission, result) {
  if (route.hasOwnProperty('children') == false) {
    if (route.hidden || hasPermission(parentPath, route.path, permission)) {
      result.children.push(route)
    }
  } else {
    if (route.hidden || hasPermission(parentPath, route.path, permission)) {
      const tmpRoute = { ...route }
      tmpRoute.children = []
      result.children.push(tmpRoute)

      route.children.forEach(children => {
        filterRoutes(path.resolve(parentPath, route.path), children, permission, result.children[result.children.length - 1])
      })
    }
  }
}

// 判断是否有权限
function hasPermission(parentPath, childrenPath, permission) {

  const pathStr = path.resolve(parentPath, childrenPath)
  for (const permissionStr of permission) {
    if (permissionStr.startsWith(pathStr)) {
      return true
    }
  }


  return false
}

// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 根据权限生成路径
export function generateRoutesForTree(routes) {
  const result = { children: [] }
  for (const route of routes) {
    if (route.hidden) { continue }

    filterRoutesForTree('', route, result)
  }

  return result.children
}

// 递归函数, 过滤路由表
function filterRoutesForTree(parentPath, route, result) {
  if (isHasChildrenForTree(route) == false) {
    result.children.push({
      path: path.resolve(parentPath, route.path),
      title: route.meta && route.meta.title
    })
  } else {
    const isShow = isShowingParentForTree(route, route.children)
    if (isShow == true) {
      result.children.push({
        path: path.resolve(parentPath, route.path),
        title: route.meta && route.meta.title,
        children: []
      })

      route.children.forEach(children => {
        filterRoutesForTree(path.resolve(parentPath, route.path), children, result.children[result.children.length - 1])
      })
    } else {
      route.children.forEach(children => {
        filterRoutesForTree(path.resolve(parentPath, route.path), children, result)
      })
    }
  }
}

function isShowingParentForTree(parent, children = []) {
  const showingChildren = children.filter(item => !item.hidden)

  // 只有一个子节点 && 父节点非总显示
  if (showingChildren.length === 1 && !parent.alwaysShow) {
    return false
  }

  return true
}

function isHasChildrenForTree(parent) {
  if (parent.hasOwnProperty('children') == false) {
    return false
  }

  const childrenList = parent.children.filter(item => !item.hidden)
  if (childrenList.length == 0) {
    return false
  }

  return true
}

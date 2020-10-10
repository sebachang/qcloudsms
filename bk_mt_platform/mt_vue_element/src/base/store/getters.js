const getters = {
  sidebar: state => state.app.sidebar,
  language: state => state.app.language,
  size: state => state.app.size,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,

  // 用户, 角色和权限
  name: state => state.user.name,
  role: state => state.user.role,
  permission: state => state.user.permission,
  permission_routes: state => state.permission.routes,
  addRoutes: state => state.permission.addRoutes,

  // biz业务列表
  bizList: state => state.bizList.bizList,
  currBiz: state => state.bizList.currBiz,
  currBizName: state => state.bizList.currBizName,

  errorLogs: state => state.errorLog.logs
}
export default getters

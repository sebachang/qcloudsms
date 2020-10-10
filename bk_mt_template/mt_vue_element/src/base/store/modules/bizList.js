import Cookies from 'js-cookie'
import { getBizList } from '@/base/api/bizList'

// 当前业务
const curr_biz_key = 'mt_curr_biz'

const state = {
  bizList: [],
  currBiz: ''
}

const mutations = {
  SET_BIZ_LIST: (state, bizList) => {
    state.bizList = bizList
  },
  SET_CURR_BIZ: (state, currBiz) => {
    state.currBiz = currBiz
  }
}

const actions = {
  getBizList({ commit, state }, currName) {
    return new Promise((resolve, reject) => {
      getBizList(currName).then(data => {
        const bizList = []
        let currBiz = ''
        if (Cookies.get(curr_biz_key) !== undefined) {
          currBiz = Cookies.get(curr_biz_key)
        }

        if (data.count > 0) {
          let bMatchCurrBiz = false

          data.info.forEach(bizData => {
            bizList.push({
              value: bizData.bk_biz_id.toString(),
              label: bizData.bk_biz_name
            })

            // 如果cookie有值且在这次获取的业务列表里面
            if (currBiz && currBiz == bizData.bk_biz_id) {
              bMatchCurrBiz = true
            }
          })

          if (currBiz == '' || bMatchCurrBiz === false) {
            currBiz = data.info[0].bk_biz_id.toString()
          }
        }

        commit('SET_BIZ_LIST', bizList)
        commit('SET_CURR_BIZ', currBiz)
        Cookies.set(curr_biz_key, currBiz, { expires: 365 })
        resolve({ bizList: bizList, currBiz: currBiz })
      }).catch(error => {
        reject(error)
      })
    })
  },

  changeCurrBiz({ commit, state }, currBiz) {
    return new Promise((resolve, reject) => {
      commit('SET_CURR_BIZ', currBiz)
      Cookies.set(curr_biz_key, currBiz, { expires: 365 })
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

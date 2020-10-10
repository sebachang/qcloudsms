<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name:{{ name }}</div>
    <div class="dashboard-text">role: {{ role }}</div>
    <div class="dashboard-text">currBiz: {{ currBiz }}</div>
<!--    <el-button @click="doTestAPI" v-permission="false">测试API</el-button>-->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Message } from 'element-ui'
import { test_example, test_generic_api } from '@/base/api/test'
import { get_jump_site, get_download_site } from '@/base/api/appUtil'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'role',
      'currBiz'
    ])
  },
  methods: {
    doTestAPI() {
      test_generic_api(this.currBiz).then(value => {
        Message({
          showClose: true,
          message: JSON.stringify(value),
          type: 'error',
          duration: 5 * 1000
        })
      }).catch(error => {
        // error 在顶层同意弹窗
        console.log('error code: ' + error.code)
        console.log('error  msg: ' + error.message)
      })

      get_jump_site('123').then(value => {
        Message({
          showClose: true,
          message: JSON.stringify(value),
          type: 'error',
          duration: 5 * 1000
        })
      })

      get_download_site('456').then(value => {
        Message({
          showClose: true,
          message: JSON.stringify(value),
          type: 'error',
          duration: 5 * 1000
        })
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>

<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-s-platform" /> 清退申请</span></el-tab-pane>
    </el-tabs>
    <el-container>
      <el-header style="height: 25px">
        <el-button-group>
          <el-tooltip class="item" effect="dark" content="刷新" placement="bottom">
            <el-button :loading="loadingButtion" type="primary" icon="el-icon-refresh" @click="handleCmdbClearanceRefresh" />
          </el-tooltip>
        </el-button-group>
        <el-button-group>
          <el-tooltip class="item" effect="dark" content="检查" placement="bottom">
            <el-button type="primary" icon="el-icon-video-play" @click="handleClearanceCheckJobs" />
            <el-dropdown size="medium" split-button type="primary" @command="handleCommand" @click="handleClearanceCheckJobs">
              <i class="el-icon-video-play el-icon--right" />
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">编辑作业</el-dropdown-item>
                <el-dropdown-item command="b">查看实例</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-tooltip>
        </el-button-group>
      </el-header>
    </el-container>
    <el-container>
      <el-main style="width: 65%">
        <el-card>
          <el-form ref="ruleForm" :rules="rules" :model="ruleForm" label-width="80px">
            <el-form-item label="清退编号" prop="removeId">
              <el-select v-model="ruleForm.removeId" placeholder="请选择编号" size="small">
                <el-option
                  v-for="(u,i) in ruleForm.removeIdObj"
                  :key="u"
                  :label="i"
                  :value="i"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-table
                v-loading="loading"
                size="small"
                highlight-current-row
                :data="ruleForm.clearanceRemoveIdList"
                @current-change="handleCurrentChange"
              >
                <el-table-column
                  prop="bk_host_id"
                  label="主机ID"
                />
                <el-table-column
                  prop="remove_id"
                  label="清退编号"
                />
                <el-table-column
                  prop="bk_host_innerip"
                  label="内网地址"
                />
                <el-table-column
                  prop="bk_host_outerip"
                  label="外网地址"
                />
                <el-table-column
                  prop="server_country"
                  label="国家"
                />
                <el-table-column
                  prop="server_city"
                  label="城市"
                />
                <el-table-column
                  prop="isp"
                  label="服务器供应商"
                />
              </el-table>
            </el-form-item>
            <!--            <el-pagination style="margin:10px 0px 0px 0px;" background :page-size="pageSizeFirst" @current-change="handleCurrentChangeFirst" :current-page="pageFirst" layout="prev, pager, next" :total="totalFirst" align="center"></el-pagination>-->
            <div style="text-align:right;">
              <p />
              <el-form-item>
                <el-button size="small" type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                <el-button size="small" @click="resetForm('ruleForm')">重置</el-button>
              </el-form-item>
            </div>
          </el-form>
        </el-card>
      </el-main>
      <el-main style="width: 35%">
        <el-card>
          <el-collapse v-model="activeNames">
            <el-collapse-item title="基础信息" name="1">
              <div style="font-size:12px;">连接ip：<span class="dd-info">{{ tableDataOne.bk_host_innerip }}</span></div>
              <div style="font-size:12px;">内网ip：<span class="dd-info">{{ tableDataOne.bk_host_innerip }}</span></div>
              <div style="font-size:12px;">外网ip：<span class="dd-info">{{ tableDataOne.bk_host_outerip }}</span></div>
              <div style="font-size:12px;">外网ip数量：<span class="dd-info">{{ tableDataOne.bk_host_outerip_2 }}</span></div>
              <div style="font-size:12px;">服务器供应商：<span class="dd-info">{{ tableDataOne.isp }}</span></div>
              <div style="font-size:12px;">国家：<span class="dd-info">{{ tableDataOne.server_country }}</span></div>
              <div style="font-size:12px;">地区：<span class="dd-info">{{ tableDataOne.server_city }}</span></div>
              <div style="font-size:12px;">流量：<span class="dd-info">{{ tableDataOne.bandwidth }}</span></div>
              <div style="font-size:12px;">价格：<span class="dd-info">{{ tableDataOne.price }}</span></div>
              <div style="font-size:12px;">磁盘类型：<span class="dd-info">{{ tableDataOne.disk_type }}</span></div>
              <div style="font-size:12px;">录入时间：<span class="dd-info">{{ tableDataOne.create_time }}</span></div>
              <div style="font-size:12px;">账号：<span class="dd-info">{{ tableDataOne.sl_account }}</span></div>
              <div style="font-size:12px;">密码：<span class="dd-info">{{ tableDataOne.password }}</span></div>
            </el-collapse-item>
            <el-collapse-item title="配置信息" name="2">
              <div style="font-size:12px;">主机名称：<span class="dd-info">{{ tableDataOne.bk_host_name }}</span></div>
              <div style="font-size:12px;">操作系统类型：<span class="dd-info">{{ tableDataOne.bk_os_type }}</span></div>
              <div style="font-size:12px;">操作系统名称：<span class="dd-info">{{ tableDataOne.bk_os_name }}</span></div>
              <div style="font-size:12px;">操作系统版本：<span class="dd-info">{{ tableDataOne.bk_os_version }}</span></div>
              <div style="font-size:12px;">操作系统位数：<span class="dd-info">{{ tableDataOne.bk_os_bit }}</span></div>
              <div style="font-size:12px;">cpu逻辑核心数：<span class="dd-info">{{ tableDataOne.bk_cpu }}</span></div>
              <div style="font-size:12px;">cpu频率：<span class="dd-info">{{ tableDataOne.bk_cpu_mhz }}</span></div>
              <div style="font-size:12px;">cpu型号：<span class="dd-info">{{ tableDataOne.bk_cpu_module }}</span></div>
              <div style="font-size:12px;">内存容量：<span class="dd-info">{{ tableDataOne.bk_mem }}</span></div>
              <div style="font-size:12px;">磁盘容量：<span class="dd-info">{{ tableDataOne.bk_disk }}</span></div>
              <div style="font-size:12px;">内网mac地址：<span class="dd-info">{{ tableDataOne.bk_mac }}</span></div>
              <div style="font-size:12px;">外网mac地址：<span class="dd-info">{{ tableDataOne.bk_outer_mac }}</span></div>
            </el-collapse-item>
            <el-collapse-item title="备注信息" name="3">
              <div style="font-size:12px;">备注：<span class="dd-info">{{ tableDataOne.bk_comment }}</span></div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>

import { postOrder } from '@/api/order_center/order'
import { getCmdbClearanceList } from '@/api/order_center/clearance'
import { runJob } from '@/base/api/task'
import { mapGetters } from 'vuex'

const defaultOrderInfo = {
  order_type: '',
  biz_id: '',
  sub_order: {
    remove_id: '',
    clearance_list: []
  }
}

export default {
  data() {
    return {
      settingInfo: Object.assign({}, defaultOrderInfo),
      activeName: 'first',
      activeNames: ['1'],
      tableDataOne: {},
      loadingButtion: false,
      loading: false,
      job_uuid: '9d1d0ce0-4521-4fe3-94c8-fd7d30b45d40',
      pageSizeFirst: 10,
      pageFirst: 1,
      totalFirst: 0,
      tableDataOneTmp: {
        bandwidth: '',
        bk_comment: '',
        bk_cpu: '',
        bk_cpu_mhz: '',
        bk_cpu_module: '',
        bk_disk: '',
        bk_host_innerip: '',
        bk_host_name: '',
        bk_host_outerip: '',
        bk_host_outerip_2: '',
        bk_mac: '',
        bk_mem: '',
        bk_os_bit: '',
        bk_os_name: '',
        bk_os_type: '',
        bk_os_version: '',
        bk_outer_mac: '',
        create_time: '',
        disk_type: '',
        id: '',
        isp: '',
        order_id: '',
        password: '',
        price: '',
        server_city: '',
        server_country: '',
        sl_account: '',
        ssh_ip: ''
      },
      ruleForm: {
        removeId: '',
        removeIdObj: {},
        clearanceList: [],
        clearanceRemoveIdList: []
      },
      rules: {
        removeId: [
          { required: true, message: '请选择清退编号', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz'
    ])
  },
  watch: {
    'ruleForm.removeId': function(val) {
      var c = 0
      for (var i = 0; i < this.ruleForm.clearanceList.length; i++) {
        if (this.ruleForm.clearanceList[i].remove_id === val) {
          this.$set(this.ruleForm.clearanceRemoveIdList, c, this.ruleForm.clearanceList[i])
          c++
        }
      }
    }
  },
  created() {
    this.getCmdbClearanceLists()
  },
  methods: {
    getCmdbClearanceLists() {
      getCmdbClearanceList(this.currBiz, 1).then(data => {
        this.ruleForm.clearanceList = data
        for (var i = 0; i < this.ruleForm.clearanceList.length; i++) {
          this.$set(this.ruleForm.removeIdObj, this.ruleForm.clearanceList[i].remove_id, this.ruleForm.clearanceList[i].remove_id)
        }
      })
    },
    // getCmdbClearanceLists() {
    //   getCmdbClearanceList(this.currBiz, 1).then(data => {
    //     this.totalFirst = data.count
    //     this.ruleForm.clearanceList = data.data
    //     for (var i = 0; i < this.ruleForm.clearanceList.length; i++) {
    //       this.$set(this.ruleForm.removeIdObj, this.ruleForm.clearanceList[i].remove_id, this.ruleForm.clearanceList[i].remove_id)
    //     }
    //   })
    // },
    // handleCurrentChangeFirst(val) {
    //   getCmdbClearanceList(this.currBiz, val).then(data => {
    //     this.totalFirst = data.count
    //     this.ruleForm.clearanceList = data.data
    //   })
    // },
    handleCurrentChange(val) {
      if (val === null) {
        this.tableDataOne = this.tableDataOneTmp
      } else {
        this.tableDataOne = val
      }
    },
    // handleCmdbClearanceRefresh() {
    //   this.loadingButtion = true
    //   this.loading = true
    //   this.ruleForm.removeIdObj = {}
    //   this.tableDataOne = this.tableDataOneTmp
    //   this.ruleForm.clearanceRemoveIdList = []
    //   this.ruleForm.removeId = ''
    //   getCmdbClearanceList(this.currBiz, 1).then(data => {
    //     this.totalFirst = data.count
    //     this.ruleForm.clearanceList = data.data
    //     for (var i = 0; i < this.ruleForm.clearanceList.length; i++) {
    //       this.$set(this.ruleForm.removeIdObj, this.ruleForm.clearanceList[i].remove_id, this.ruleForm.clearanceList[i].remove_id)
    //     }
    //     this.loadingButtion = false
    //     this.loading = false
    //   })
    // },
    handleCmdbClearanceRefresh() {
      this.loadingButtion = true
      this.loading = true
      this.ruleForm.removeIdObj = {}
      this.tableDataOne = this.tableDataOneTmp
      this.ruleForm.clearanceRemoveIdList = []
      this.ruleForm.removeId = ''
      getCmdbClearanceList(this.currBiz, 1).then(data => {
        this.ruleForm.clearanceList = data
        for (var i = 0; i < this.ruleForm.clearanceList.length; i++) {
          this.$set(this.ruleForm.removeIdObj, this.ruleForm.clearanceList[i].remove_id, this.ruleForm.clearanceList[i].remove_id)
        }
        this.loadingButtion = false
        this.loading = false
      })
    },
    handleClearanceCheckJobs() {
      if (!this.ruleForm.removeId) {
        this.$notify({
          title: '警告',
          message: '请选择你要检查的清退编号',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      this.$confirm('确定执行作业吗', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        runJob(this.job_uuid, {
          'bk_biz': this.currBiz,
          'script_param': this.ruleForm.removeId
        })
        this.$message({
          type: 'success',
          message: '成功!'
        })
      }).catch(err => { console.error(err) })
    },
    submitForm(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          this.settingInfo.sub_order.remove_id = this.ruleForm.removeId
          this.settingInfo.sub_order.clearance_list = this.ruleForm.clearanceRemoveIdList
          this.settingInfo.biz_id = this.currBiz
          this.settingInfo.order_type = 'clearance'
          // console.log(this.settingInfo)
          postOrder(this.settingInfo).then(data => {
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
                  <div>工单 : ${this.settingInfo.order_type}</div>
                `,
              type: 'success'
            })
            this.$router.push('./order')
          })
          // console.log(this.settingInfo)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(form) {
      this.$refs[form].resetFields()
      this.tableDataOne = this.tableDataOneTmp
      this.ruleForm.clearanceRemoveIdList = []
    },
    handleCommand(command) {
      if (command === 'a') {
        this.$router.push({ path: '/task/job_module/clearance_check' })
      }
      if (command === 'b') {
        this.$router.push({ path: '/task/taskinstance_module/clearance_check' })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  .roles-table {
    margin-top: 30px;
  }
  .permission-tree {
    margin-bottom: 30px;
  }
}
</style>

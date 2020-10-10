<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-s-platform"></i> 厂商配置</span></el-tab-pane>
    </el-tabs>
    <el-button size="small" type="primary" icon="el-icon-document-add" @click="handleAddPlatform">
      添加配置
    </el-button>
    <el-card style="margin : 10px 0px 0px 0px;">
      <el-table :data="platformList" size="small" style="width: 100%;" v-loading="loading1">
        <el-table-column align="center" label="平台名称" width="300">
          <template slot-scope="scope">
            {{ scope.row.platform_name }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="账号" width="300">
          <template slot-scope="scope">
            {{ scope.row.account }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="密码" width="300">
          <template slot-scope="scope">
            {{ scope.row.passwd }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="状态" width="300">
          <template slot-scope="scope">
            <span v-if="scope.row.state === 0" style="color: #00bb00">可用</span>
            <span v-if="scope.row.state === 1" style="color: #ff4949">不可用</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleGetHostProfile(scope)">
              机型
            </el-button>
            <el-button type="text" size="small" @click="handleGetCenter(scope)">
              数据中心
            </el-button>
            <el-button type="text" size="small" @click="handleEditPlatform(scope)">
              编辑
            </el-button>
            <el-button type="text" style="color: #cd0a0a" size="small" @click="handleDeletePlatform(scope)" >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="机型" :visible.sync="dialogVisible1" style="width: 1160px; margin: 0 auto">
      <el-card>
        <el-transfer :titles="biaoti" v-model="hostValue" :data="hostProfile"></el-transfer>
      </el-card>
      <div style="text-align:right;margin-top: 10px">
        <el-button type="danger" size="small" @click="dialogVisible1=false">
          取消
        </el-button>
        <el-button type="primary" size="small" @click="platformHostProfileSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog title="数据中心" :visible.sync="dialogVisible2" style="width: 1160px; margin: 0 auto">
      <el-card>
        <el-transfer :titles="biaoti" v-model="centerValue" :data="center" style="margin: 0 auto"></el-transfer>
      </el-card>
      <div style="text-align:right;margin-top: 10px">
        <el-button type="danger" size="small" @click="dialogVisible2=false">
          取消
        </el-button>
        <el-button type="primary" size="small" @click="platformCenterSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="dialogVisible0" :title="dialogType==='edit'?'编辑':'新增'">
      <el-card>
        <el-form size="small" :model="settingInfo" label-width="100px" label-position="left">
          <el-form-item size="small" label="名称">
            <el-input size="small" v-model="settingInfo.platform_name" placeholder="平台名称" />
          </el-form-item>
          <el-form-item size="small" label="账号">
            <el-input size="small" v-model="settingInfo.account" placeholder="账号" />
          </el-form-item>
          <el-form-item size="small" label="密码">
            <el-input size="small" v-model="settingInfo.passwd" placeholder="密码" />
          </el-form-item>
          <el-form-item size="small" label="状态">
            <el-radio size="small" v-model="settingInfo.state" :label="0">开启</el-radio>
            <el-radio size="small" v-model="settingInfo.state" :label="1">关闭</el-radio>
          </el-form-item>
        </el-form>
      </el-card>
      <div style="text-align:right;margin-top: 10px">
        <el-button size="small" type="danger" @click="dialogVisible0=false">
          取消
        </el-button>
        <el-button size="small" type="primary" @click="platformSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import { getPlatformList, postPlatform, putPlatform, deletePlatform, getPlatformHostMap, getPlatformCenterMap } from '@/api/deliverManage'
import { getHostList, postPlatformHostMap } from '@/api/deliverManage'
import { getCenterList, postPlatformCenterMap } from '@/api/deliverManage'
import { deepClone } from '@/base/utils'
import { mapGetters } from 'vuex'

const defaultPlatformInfo = {
  id: '',
  platfrom_name: '',
  account: '',
  passwd: '',
  biz_id: '',
  state: 0
}

const defaultPlatformHostMap = {
  pid: '',
  hid_list: []
}

const defaultPlatformCenterMap = {
  pid: '',
  cid_list: []
}

export default {
  data() {
    return {
      loading1: true,
      activeName: 'first',
      settingInfo: Object.assign({}, defaultPlatformInfo),
      settingInfo1: Object.assign({}, defaultPlatformHostMap),
      settingInfo2: Object.assign({}, defaultPlatformCenterMap),
      platformList: [],
      hostList: [],
      centerList: [],
      biaoti: ['未选择列表', '已选择列表'],
      dialogType: 'new',
      dialogType1: ' ',
      dialogType2: ' ',
      dialogVisible0: false,
      dialogVisible1: false,
      dialogVisible2: false,
      hostProfile: [],
      hostValue: [],
      platformId: ' ',
      center: [],
      centerValue: []
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ])
  },
  created() {
    this.getAllPlatformList()
    this.getAllHostList()
    this.getAllCenterLists()
  },
  methods: {
    getAllPlatformList() {
      getPlatformList(this.currBiz).then(data => {
        this.platformList = data
      })
      this.loading1 = false
    },
    getAllHostList() {
      getHostList(this.currBiz).then(data => {
        this.hostList = data
      })
    },
    getAllCenterLists() {
      getCenterList(this.currBiz).then(data => {
        this.centerList = data
      })
    },
    handleAddPlatform() {
      this.dialogVisible1 = false
      this.dialogVisible2 = false
      this.settingInfo = Object.assign({}, defaultPlatformInfo)
      this.dialogType = 'new'
      this.dialogVisible0 = true
    },
    async handleGetHostProfile(scope) {
      this.dialogVisible1 = false
      this.dialogVisible2 = false
      this.dialogType1 = 'info'
      var result = await getPlatformHostMap(scope.row.id)
      this.hostProfile = []
      for (var i = 0; i < this.hostList.length; i++) {
        this.hostProfile.push({
          key: this.hostList[i].id,
          label: this.hostList[i].host_name
        })
      }
      this.hostValue = []
      for (var x = 0; x < result.length; x++) {
        this.hostValue[x] = result[x].hid
      }
      this.platformId = scope.row.id
      this.dialogVisible1 = true
    },
    async handleGetCenter(scope) {
      this.dialogVisible1 = false
      this.dialogVisible2 = false
      this.dialogType2 = 'info'
      var result = await getPlatformCenterMap(scope.row.id)
      this.center = []
      for (var i = 0; i < this.centerList.length; i++) {
        this.center.push({
          key: this.centerList[i].id,
          label: this.centerList[i].center_name
        })
      }
      this.centerValue = []
      for (var x = 0; x < result.length; x++) {
        this.centerValue[x] = result[x].cid
      }
      this.platformId = scope.row.id
      this.dialogVisible2 = true
    },
    handleEditPlatform(scope) {
      this.dialogVisible1 = false
      this.dialogVisible2 = false
      this.settingInfo = deepClone(scope.row)
      this.dialogType = 'edit'
      this.dialogVisible0 = true
    },
    handleDeletePlatform({ row }) {
      this.$confirm('确定删除厂商配置?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        await deletePlatform(row.id)
        for (var i = 0; i < this.platformList.length; i++) {
          if (this.platformList[i].id === row.id) {
            this.platformList.splice(i, 1)
          }
        }
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => { console.error(err) })
    },
    async platformSetting() {
      if (this.dialogType === 'edit') {
        this.settingInfo.biz_id = this.currBiz
        await putPlatform(this.settingInfo.id, this.settingInfo)
        this.dialogVisible0 = false
        for (var i = 0; i < this.platformList.length; i++) {
          if (this.platformList[i].id === this.settingInfo.id) {
            this.$set(this.platformList, i, this.settingInfo)
          }
        }
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>厂商 : ${this.settingInfo.platform_name}</div>
          `,
          type: 'success'
        })
      }
      if (this.dialogType === 'new') {
        this.settingInfo.biz_id = this.currBiz
        var res = await postPlatform(this.settingInfo)
        this.dialogVisible0 = false
        this.platformList.push(res)
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>厂商 : ${this.settingInfo.platform_name}</div>
          `,
          type: 'success'
        })
      }
    },
    async platformHostProfileSetting() {
      if (this.dialogType1 === 'info') {
        this.settingInfo1 = Object.assign({}, defaultPlatformHostMap)
        this.settingInfo1.pid = this.platformId
        this.settingInfo1.hid_list = this.hostValue
        await postPlatformHostMap(this.settingInfo1)
        this.dialogVisible1 = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>添加成功</div>
          `,
          type: 'success'
        })
      }
    },
    async platformCenterSetting() {
      if (this.dialogType2 === 'info') {
        this.settingInfo2 = Object.assign({}, defaultPlatformCenterMap)
        this.settingInfo2.pid = this.platformId
        this.settingInfo2.cid_list = this.centerValue
        await postPlatformCenterMap(this.settingInfo2)
        this.dialogVisible2 = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>添加成功</div>
          `,
          type: 'success'
        })
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

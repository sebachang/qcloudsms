<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-cpu"/> 机型配置</span></el-tab-pane>
    </el-tabs>
    <el-button @click="handleAddHostProfile" icon="el-icon-document-add" size="small" type="primary">
      添加配置
    </el-button>
    <el-card style="margin : 10px 0px 0px 0px;">
      <el-table :data="hostProfileList" :highlight-current-row="true" size="small" style="width: 100%;"
                v-loading="loading1">
        <el-table-column align="center" label="机型" width="150">
          <template slot-scope="scope">
            {{ scope.row.host_name }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="核心" width="150">
          <template slot-scope="scope">
            {{ scope.row.cpu }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="内存" width="150">
          <template slot-scope="scope">
            {{ scope.row.mem }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="系统盘" width="150">
          <template slot-scope="scope">
            {{ scope.row.sdisk }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="机械盘" width="150">
          <template slot-scope="scope">
            {{ scope.row.disk }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="固态盘" width="150">
          <template slot-scope="scope">
            {{ scope.row.ssd }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="带宽" width="150">
          <template slot-scope="scope">
            {{ scope.row.net }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="预估价格" width="150">
          <template slot-scope="scope">
            {{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="状态" width="150">
          <template slot-scope="scope">
            <span style="color: #00bb00" v-if="scope.row.state === 0">可用</span>
            <span style="color: #ff4949" v-if="scope.row.state === 1">不可用</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
          <template slot-scope="scope">
            <el-button @click="handleEditHostProfile(scope)" size="small" type="text">
              编辑
            </el-button>
            <el-button @click="handleDeleteHostProfile(scope)" size="small" style="color: #cd0a0a" type="text">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :title="dialogType==='edit'?'编辑':'新增'" :visible.sync="dialogVisible0">
      <el-card>
        <el-form :model="settingInfo" :rules="rules" label-position="left" label-width="100px" ref="form" size="small">
          <el-form-item label="机型" prop="host_name" size="small">
            <el-input placeholder="机型名" size="small" v-model="settingInfo.host_name"/>
          </el-form-item>
          <el-form-item label="核心" prop="cpu" size="small">
            <el-input placeholder="核心数" size="small" v-model="settingInfo.cpu">
              <span slot="append">逻辑核</span>
            </el-input>
          </el-form-item>
          <el-form-item label="内存" prop="mem" size="small">
            <el-input placeholder="内存数" size="small" v-model="settingInfo.mem">
              <span slot="append">GB</span>
            </el-input>
          </el-form-item>
          <el-form-item label="系统盘" prop="sdisk" size="small">
            <el-input placeholder="系统盘容量" size="small" v-model="settingInfo.sdisk">
              <span slot="append">GB</span>
            </el-input>
          </el-form-item>
          <el-form-item label="机械盘" prop="disk" size="small">
            <el-input placeholder="机械盘容量" size="small" v-model="settingInfo.disk">
              <span slot="append">GB</span>
            </el-input>
          </el-form-item>
          <el-form-item label="固态盘" prop="ssd" size="small">
            <el-input placeholder="固态盘容量" size="small" v-model="settingInfo.ssd">
              <span slot="append">GB</span>
            </el-input>
          </el-form-item>
          <el-form-item label="带宽" prop="net" size="small">
            <el-input placeholder="带宽" size="small" v-model="settingInfo.net">
              <span slot="append">Mbps</span>
            </el-input>
          </el-form-item>
          <el-form-item label="预估价" prop="price" size="small">
            <el-input placeholder="价格" size="small" v-model="settingInfo.price">
              <span slot="append">$</span>
            </el-input>
          </el-form-item>
          <el-form-item label="状态" prop="state" size="small">
            <el-radio :label="0" size="small" v-model="settingInfo.state">开启</el-radio>
            <el-radio :label="1" size="small" v-model="settingInfo.state">关闭</el-radio>
          </el-form-item>
        </el-form>
      </el-card>
      <div style="text-align:right;margin-top: 10px">
        <el-button @click="dialogVisible0=false" size="small" type="danger">
          取消
        </el-button>
        <el-button @click="hostProfileSetting" size="small" type="primary">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import {getHostList, postHostProfile, putHostProfile, deleteHostProfile} from '@/api/deliverManage'
import {deepClone} from '@/base/utils'
import {mapGetters} from 'vuex'

const defaultHostProfile = {
  id: '',
  host_name: '',
  cpu: '',
  mem: '',
  sdisk: '',
  disk: '',
  ssd: '',
  net: '',
  price: '',
  state: 0,
  biz_id: ''
}

export default {
  data() {
    return {
      loading1: true,
      activeName: 'first',
      settingInfo: Object.assign({}, defaultHostProfile),
      hostProfileList: [],
      dialogVisible0: false,
      dialogType: '',
      rules: {
        host_name: [{required: true, message: '请填写机型', trigger: 'blur'}],
        cpu: [
          {required: true, message: '请填写核心数', trigger: 'blur'},
          // {type: 'integer', message: '核心数量不正确', trigger: 'blur'}
        ],
        mem: [{required: true, message: '请填写内存大小', trigger: 'blur'}],
        sdisk: [{required: true, message: '请填写系统盘大小', trigger: 'blur'}],
        disk: [{required: true, message: '请填写机械硬盘大小', trigger: 'blur'}],
        ssd: [{required: true, message: '请填写固态硬盘大小', trigger: 'blur'}],
        net: [{required: true, message: '请填写网卡带宽', trigger: 'blur'}],
        price: [{required: true, message: '请填写价格', trigger: 'blur'}],
      }
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ])
  },
  created() {
    this.getAllHostList()
  },
  methods: {
    getAllHostList() {
      getHostList(this.currBiz).then(data => {
        this.hostProfileList = data
      })
      this.loading1 = false
    },
    handleAddHostProfile() {
      this.settingInfo = Object.assign({}, defaultHostProfile)
      this.dialogType = 'new'
      this.dialogVisible0 = true
    },
    handleEditHostProfile(scope) {
      this.settingInfo = deepClone(scope.row)
      this.dialogType = 'edit'
      this.dialogVisible0 = true
    },
    handleDeleteHostProfile(scope) {
      this.$confirm('确定删除机型配置?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async () => {
        await deleteHostProfile(scope.row.id)
        for (var i = 0; i < this.hostProfileList.length; i++) {
          if (this.hostProfileList[i].id === scope.row.id) {
            this.hostProfileList.splice(i, 1)
          }
        }
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },
    async hostProfileSetting() {
      this.$refs.form.validate(async (ok) => {
        if (!ok) {
          return false
        }
        if (this.dialogType === 'edit') {
          await putHostProfile(this.settingInfo.id, this.settingInfo)
          this.dialogVisible0 = false
          for (var i = 0; i < this.hostProfileList.length; i++) {
            if (this.hostProfileList[i].id === this.settingInfo.id) {
              this.$set(this.hostProfileList, i, this.settingInfo)
            }
          }
          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>机型 : ${this.settingInfo.host_name}</div>
          `,
            type: 'success'
          })
        }
        if (this.dialogType === 'new') {
          this.settingInfo.biz_id = this.currBiz
          var res = await postHostProfile(this.settingInfo)
          this.dialogVisible0 = false
          this.hostProfileList.push(res)
          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>厂商 : ${this.settingInfo.host_name}</div>
          `,
            type: 'success'
          })
        }
      })
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

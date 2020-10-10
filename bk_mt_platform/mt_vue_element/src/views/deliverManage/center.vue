<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-s-home"></i> 机房配置</span></el-tab-pane>
    </el-tabs>
    <el-button size="small" type="primary" icon="el-icon-document-add" @click="handleAddCenter">
      添加配置
    </el-button>
    <el-card class="box-card" style="margin : 10px 0px 0px 0px;">
      <el-table
        size="small"
        v-loading="loading1"
        :data="centerList"
        :highlight-current-row="true">
        <el-table-column
          align="center"
          label="序号">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          label="数据中心">
          <template slot-scope="scope">
            <span>{{ scope.row.center_name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="状态">
          <template slot-scope="scope">
            <span v-if="scope.row.state === 0" style="color: #00bb00">可用</span>
            <span v-if="scope.row.state === 1" style="color: #ff4949">不可用</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEditCenter(scope)">
              编辑
            </el-button>
            <el-button type="text" style="color: #cd0a0a" size="small" @click="handleDeleteCenter(scope)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :visible.sync="dialogVisible0" :title="dialogType==='edit'?'编辑':'新增'">
      <el-card class="box-card">
        <el-form size="small" :model="settingInfo" label-width="100px" label-position="left">
          <el-form-item size="small" label="数据中心">
            <el-input size="small" v-model="settingInfo.center_name" placeholder="数据中心名" />
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
        <el-button size="small" type="primary" @click="centerSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getCenterList, postCenter, putCenter, deleteCenter } from '@/api/deliverManage'
import { deepClone } from '@/base/utils'
import { mapGetters } from 'vuex'
const defaultCenter = {
  id: '',
  center_name: '',
  state: 0,
  biz_id: ''
}
export default {
  data() {
    return {
      activeName: 'first',
      loading1: true,
      settingInfo: Object.assign({}, defaultCenter),
      centerList: [],
      dialogVisible0: false,
      dialogType: ''
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ])
  },
  created() {
    this.getAllCenterList()
  },
  methods: {
    getAllCenterList() {
      getCenterList(this.currBiz).then(data => {
        this.centerList = data
      })
      this.loading1 = false
    },
    handleAddCenter() {
      this.settingInfo = Object.assign({}, defaultCenter)
      this.dialogType = 'new'
      this.dialogVisible0 = true
    },
    handleEditCenter(scope) {
      this.settingInfo = deepClone(scope.row)
      this.dialogType = 'edit'
      this.dialogVisible0 = true
    },
    handleDeleteCenter(scope) {
      this.$confirm('确定删除机型配置?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        await deleteCenter(scope.row.id)
        for (var i = 0; i < this.centerList.length; i++) {
          if (this.centerList[i].id === scope.row.id) {
            this.centerList.splice(i, 1)
          }
        }
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => { console.error(err) })
    },
    async centerSetting() {
      if (this.dialogType === 'edit') {
        await putCenter(this.settingInfo.id, this.settingInfo)
        this.dialogVisible0 = false
        for (var i = 0; i < this.centerList.length; i++) {
          if (this.centerList[i].id === this.settingInfo.id) {
            this.$set(this.centerList, i, this.settingInfo)
          }
        }
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>数据中心 : ${this.settingInfo.center_name}</div>
          `,
          type: 'success'
        })
      }
      if (this.dialogType === 'new') {
        this.settingInfo.biz_id = this.currBiz
        var res = await postCenter(this.settingInfo)
        this.dialogVisible0 = false
        this.centerList.push(res)
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>厂商 : ${this.settingInfo.center_name}</div>
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

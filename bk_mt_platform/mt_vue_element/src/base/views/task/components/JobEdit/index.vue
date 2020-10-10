<template>
  <el-dialog
    :visible.sync="dialogVisible"
    title="编辑"
    :close-on-click-modal="false"
    @open="handleDialogOpen"
    @close="handleDialogClose"
  >
    <el-form ref="ruleForm" :model="settingInfo" :rules="rules" label-width="80px">
      <el-row>
        <el-col :span="12">
          <el-form-item label="任务名" prop="title">
            <el-input v-model="settingInfo.title" :disabled="true" placeholder="标题" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="模块" prop="module">
            <el-input v-model="settingInfo.module" :disabled="true" placeholder="模块" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="执行账户" prop="username">
            <el-input v-model="settingInfo.username" placeholder="执行账户" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="脚本名" prop="script_name">
            <el-input v-model="settingInfo.script_name" :disabled="true" placeholder="" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="回调地址" prop="callback">
            <el-input v-model="settingInfo.callback" placeholder="回调地址" />
          </el-form-item>

        </el-col>
        <el-col :span="12">
          <el-form-item label="创建时间" prop="create_time">
            <el-input v-model="settingInfo.create_time" :disabled="true" placeholder="创建时间" />
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>

    <div class="table-head-container">
      <div align="left" style="float:left">
        <el-button
          icon="el-icon-circle-plus-outline"
          size="mini"
          type="primary"
          plain
          @click="handleAddHost"
        >
          添加主机
        </el-button>
      </div>
      <div align="right" class="right-menu">
        <el-input
          v-model="searchHost"
          size="mini"
          placeholder="输入关键字搜索"
        />
      </div>
    </div>
    <el-table
      border
      :data="hostTableData"
      style="width: 100%"
      :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
      :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
    >
      <el-table-column
        prop="bk_cloud_id"
        label="区域ID"
        width="180"
      />
      <el-table-column
        prop="ip"
        label="IP地址"
      />
      <el-table-column label="操作" width="160">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            plain
            @click="handleHostDelete(scope)"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div
      style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid"
    >
      <el-pagination
        background
        layout="prev, pager, next, sizes, total, jumper"
        :current-page="currentHostPage"
        :page-sizes="[5]"
        :page-size="pageHostSize"
        :total="currentHostTotal"
        @current-change="handleHostCurrentChange"
      />
    </div>
    <div style="text-align:right;">
      <el-button type="danger" @click="dialogVisible=false">
        取消
      </el-button>
      <el-button type="primary" @click="confirmSetting">
        确认
      </el-button>
    </div>
    <IpSelect ref="ip_select" :append-to-body="true" @pick="handlePickIp" />
  </el-dialog>
</template>

<script>
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'
import IpSelect from '@/base/views/components/IpSelect/index'

import { updateJob } from '@/base/api/task'

const defaultSettingInfo = {
  job_uuid: '',
  bk_biz: 0,
  title: '',
  module: 'default',
  exec_ip: '[]',
  username: 'root',
  callback: '',
  script_name: '',
  create_time: ''
}

export default {
  name: 'TaskDetails',
  props: {},
  computed: {
    ...mapGetters(['currBiz'])
  },
  components: { IpSelect },
  data() {
    return {
      dialogVisible: false,
      settingInfo: Object.assign({}, defaultSettingInfo),

      hosts: [],
      hostTableData: [],
      currentHostPage: 1,
      pageHostSize: 5,
      currentHostTotal: 0,

      searchHost: '',

      rules: {
        title: [
          { required: true, message: '请输入任务名', trigger: 'change' }
        ],
        // exec_ip: [
        //   {required: true, message: '执行IP', trigger: 'change'}
        // ],
        username: [
          { required: true, message: '请输入执行账户', trigger: 'change' }
        ],
        create_at: [
          { required: true, message: '请输入创建时间', trigger: 'change' }
        ]
      }

    }
  },
  watch: {
    // 监听搜索改变
    searchHost(curVal, oldVal) {
      // 实现input连续输入，只发一次请求
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.searchHostChange()
      }, 300)
    }
  },
  methods: {
    show(scope) {
      try {
        this.$refs['ruleForm'].resetFields()
      } catch (e) {

      }

      this.settingInfo = deepClone(scope.row)
      this.searchHost = ''
      this.hosts = JSON.parse(this.settingInfo.exec_ip)
      this.searchHostChange()
      this.dialogVisible = true
    },

    searchHostChange(val = 1) {
      let cache = []
      if (this.searchHost !== '') {
        for (const value of this.hosts) {
          var reg = RegExp(this.searchHost)
          if (value.ip.match(reg)) {
            cache.push(value)
          }
        }
      } else {
        cache = this.hosts
      }

      this.hostTableData = cache
      this.currentHostTotal = this.hostTableData.length
      this.currentHostPage = val

      if (this.pageHostSize * this.currentHostPage >= this.currentHostTotal) {
        this.hostTableData = this.hostTableData.slice((this.currentHostPage - 1) * this.pageHostSize, this.currentHostTotal)
      } else {
        this.hostTableData = this.hostTableData.slice((this.currentHostPage - 1) * this.pageHostSize, this.pageHostSize * this.currentHostPage)
      }
    },

    handleHostCurrentChange(val) {
      this.searchHostChange(val)
    },

    // 删除主机
    handleHostDelete({ $index, row }) {
      const obj = this.hosts.find(c => c.bk_cloud_id === row.bk_cloud_id && c.ip === row.ip)
      let dl_index = null

      this.hosts.find(function(value, index) {
        if (value.bk_cloud_id === row.bk_cloud_id && value.ip === row.ip) {
          dl_index = index
        }
      })

      this.hosts.splice(dl_index, 1)
      if (this.currentHostPage > 1 && this.hostTableData.length >= 2) {
        this.searchHostChange(this.currentHostPage)
      } else if (this.currentHostPage > 1 && this.hostTableData.length === 1) {
        this.searchHostChange(this.currentHostPage - 1)
      } else {
        this.searchHostChange()
      }
    },

    handleDialogOpen() {

    },

    handleDialogClose() {

    },

    handleAddHost() {
      this.$refs.ip_select.show()
    },

    SetHosts(arr) {
      for (const t of arr) {
        // 检查缓存中是否已经存在
        if (this.hosts.find(c => c.bk_cloud_id === t.bk_cloud_id && c.ip === t.ip)) {
          // 已经存在说明以前记录过，现在这个就是多余的，直接忽略
          continue
        }
        // 不存在就说明以前没遇到过，把它记录下来
        this.hosts.push(t)
      }
    },

    handlePickIp(ip) {
      this.SetHosts(ip)
      this.searchHostChange()
    },

    // 添加 or 更新提交
    async confirmSetting() {
      this.settingInfo.exec_ip = JSON.stringify(this.hosts)
      await updateJob(this.settingInfo.id, this.settingInfo).then(() => {
        const title = this.settingInfo.title
        this.dialogVisible = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>更新 :  ${title}</div>
          `,
          type: 'success'
        })

        this.$emit('dataRefresh')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .table-head-container {
    background: #f2f2f2;
    height: 50px;
    margin-top: 10px;
    padding: 10px;
    line-height: 22px;
    border-radius: 4px 4px 0 0;
    border-color: #dfe6ec;
    border-width: 1px 1px 0 1px;
    border-style: solid;
  }

  .right-menu {
    float: right;
    height: 100%;

    &:focus {
      outline: none;
    }
  }
</style>

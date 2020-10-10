<template>
  <div class="app-container">
    <el-card>
      <div class="clearfix datatable-head-container">
        <el-button @click="showCreateInstance()" icon="el-icon-circle-plus-outline" plain size="mini" type="primary">
          创建实例
        </el-button>
        <el-button @click="handleSelectAll" icon="el-icon-finished" plain size="mini">
          跨页全选
        </el-button>
        <el-button @click="handleClearSelect" icon="el-icon-files" plain size="mini">取消选择</el-button>

        <span style="color: darkgray">
          选择了{{ totalNum }}中的{{ selection.length }}条
        </span>
        <span style="margin-left: 50px" v-show="!selectionEmpty">
          <el-button-group>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('start')" size="mini">
              <svg-icon icon-class="play"/>
              启动
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('stop')" size="mini">
              <svg-icon icon-class="stop"/>
              停止
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('restart')" size="mini">
              <svg-icon icon-class="restart"/>
              重启
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('reload')" size="mini">
              <svg-icon icon-class="reload"/>
              重载
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('pull_config')" size="mini">
              <svg-icon icon-class="gear"/>
              下发配置
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('pull_config_restart')" size="mini">
              <svg-icon icon-class="gear"/>
              下发并重启
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('pull_config_reload')" size="mini">
              <svg-icon icon-class="gear"/>
              下发并重载
            </el-button>
            <el-button :disabled="selectionEmpty" @click="handleBatchOperation('publish')" size="mini">
              <svg-icon icon-class="publish"/>
              发布
            </el-button>
          </el-button-group>
        </span>
        <div style="float:right;">
          <search-box @enter="handleSearch" v-model="search"/>
          <el-button @click="handleRefresh" circle class="el-icon-refresh rounded-button"/>
        </div>
      </div>
      <el-table
        :data="instances"
        :row-key="getRowKey"
        @selection-change="selection=$event"
        border
        cell-class-name="datatable-cell"
        header-cell-class-name="datatable-header"
        ref="dataTable"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column reserve-selection type="selection"/>
        <el-table-column align="center" header-align="center" label="名称" prop="process_obj.name"/>
        <el-table-column align="center" header-align="center" label="描述" prop="desc"/>
        <el-table-column align="center" header-align="center" label="机器" prop="machine"/>
        <el-table-column align="center" header-align="center" label="状态">
          <InstanceStatus :data="row.status" slot-scope="{row}"/>
        </el-table-column>
        <el-table-column align="center" header-align="center" label="工作路径" prop="work_dir"/>
        <el-table-column align="center" header-align="center" width="420px">
          <template slot-scope="{row}">
            <div>
              <el-button @click="handleMenuCommand(row, 'clone')" type="warning" plain size="mini">
                <svg-icon icon-class="clone"/>
                克隆
              </el-button>
              <el-button @click="showModifyInstance(row)" type="success" plain size="mini">
                <svg-icon icon-class="edit"/>
                编辑
              </el-button>
              <el-button @click="removeInstance(row)" type="danger" plain size="mini">
                <svg-icon icon-class="delete"/>
                删除
              </el-button>
              <el-dropdown :show-timeout="100" @command="onOperationClick($event, row)">
                <el-button class="el-icon-more" size="mini"/>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item :command="btn.action" v-for="btn in operationButtons">
                    <svg-icon :icon-class="btn.icon"/>
                    {{btn.title}}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div
        style="height: 50px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid"
      >
        <el-pagination
          :current-page.sync="currentPage"
          :page-size.sync="pageSize"
          :page-sizes="[5, 10, 15, 20]"
          :total="totalNum"
          @current-change="reloadInstances"
          @size-change="reloadInstances"
          align="center"
          background
          layout="prev, pager, next, sizes, total, jumper"
        />
      </div>
      <el-collapse v-model="collapse">
        <el-collapse-item name="log">
          <template slot="title">
            <div style="text-align: center; width: 100%">
              <el-button :icon="collapse.length > 0 ? 'el-icon-caret-top':'el-icon-caret-bottom'">操作历史</el-button>
            </div>
          </template>
          <task-instance :modules="'process_manage'" ref="history"/>
        </el-collapse-item>
      </el-collapse>
      <el-dialog
        :close-on-click-modal="false"
        :title="instanceCreate ? '创建实例' : '修改实例'"
        :visible.sync="instanceDialogVisible"
      >
        <el-form label-width="120px">
          <el-form-item label="描述">
            <el-input placeholder="" v-model="instanceForm.desc"/>
          </el-form-item>
          <el-form-item label="进程">
            <el-select v-model="instanceForm.process">
              <el-option :key="process.id" :label="process.name" :value="process.id" v-for="process in processes"/>
            </el-select>
          </el-form-item>
          <el-form-item label="主机">
            <el-input placeholder="1.1.1.1" v-model="instanceForm.machine">
              <el-button @click="handleShowIpSelect()" slot="append">选择IP</el-button>
            </el-input>
          </el-form-item>
          <el-form-item label="工作目录">
            <el-input placeholder="" v-model="instanceForm.work_dir"/>
          </el-form-item>
          <el-form-item label="启动用户">
            <el-input placeholder="" v-model="instanceForm.launch_user"/>
          </el-form-item>
          <el-form-item label="pid文件">
            <el-input placeholder="" v-model="instanceForm.pid_path"/>
          </el-form-item>
          <el-form-item label="是否自动拉起">
            <el-switch active-value="1" inactive-value="0" v-model="instanceForm.auto_restart"/>
          </el-form-item>
          <el-form-item label="拉起间隔">
            <el-input placeholder="" v-model="instanceForm.restart_interval"/>
          </el-form-item>
          <el-form-item label="操作超时时间">
            <el-input placeholder="" v-model="instanceForm.operate_timeout"/>
          </el-form-item>
          <el-form-item>
            <el-button @click="saveInstanceForm()" type="primary">保存</el-button>
            <el-button @click="instanceDialogVisible=false" type="danger">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
      <IpSelect :limit="1" @pick="handlePickIp" ref="ip_select"/>
      <batch-operation @finish="reloadInstanceStatus" ref="batch_operation"/>
    </el-card>
  </div>
</template>

<script>
import {
  addInstance,
  deleteInstance,
  getBkJobLog,
  getInstances,
  getInstanceStatus,
  getProcesses,
  runOperation,
  updateInstance
} from '@/api/processManage'
import {mapGetters} from 'vuex'
import {getTaskInstance} from '@/base/api/task'
import SearchBox from '@/base/components/SearchBox/index'
import IpSelect from '@/base/views/components/IpSelect/index'
import taskInstance from '@/base/views/components/TaskInstance/index'
import Popconfirm from '@/base/views/components/Popconfirm/index'
import InstanceStatus from '@/views/processManage/components/InstanceStatus'
import BatchOperation from '@/views/processManage/components/BatchOperation'
import {confirmPromise} from '@/base/utils/interactive'
import {deepClone} from '@/base/utils'

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

export default {
  name: 'Instance',
  components: {BatchOperation, InstanceStatus, Popconfirm, taskInstance, IpSelect, SearchBox},
  data() {
    return {
      instances: [],
      processes: [],
      loading: true,
      totalNum: 0,
      selection: [],
      search: '',
      instanceDialogVisible: false,
      instanceCreate: true,
      instanceForm: {},
      operationHistory: [],
      collapse: [],
      currentPage: 1,
      currentSearch: '',
      pageSize: 5,
      show: false,
      operationButtons: [{
        action: 'start',
        title: '启动',
        icon: 'play'
      }, {
        action: 'restart',
        title: '重启',
        icon: 'restart'
      }, {
        action: 'reload',
        title: '重载',
        icon: 'reload'
      }, {
        action: 'publish',
        title: '发布',
        icon: 'publish'
      }, {
        action: 'pull_config',
        title: '下发配置',
        icon: 'gear'
      }, {
        action: 'pull_config_restart',
        title: '下发并重启',
        icon: 'gear'
      },{
        action: 'pull_config_reload',
        title: '下发并重载',
        icon: 'gear'
      },{
        action: 'stop',
        title: '停止',
        icon: 'stop'
      }]
    }
  },
  computed: {
    ...mapGetters(['currBiz']),
    selectionEmpty() {
      return this.selection.length === 0
    }
  },
  async created() {
    await this.reloadProcesses()
    await this.reloadInstances()
  },
  methods: {
    async reloadProcesses() {
      this.processes = await getProcesses(this.currBiz)
    },
    async reloadInstances() {
      this.loading = true
      const {results, count} = await getInstances(this.currBiz, this.currentPage, this.pageSize, this.currentSearch)

      this.loading = false
      results.forEach((obj) => obj.status = '未知')
      this.instances = results
      this.totalNum = count
      await this.reloadInstanceStatus()
    },
    async reloadInstanceStatus() {
      for (const instance in this.instances) {
        await this.updateInstanceStatus(this.instances[instance])
      }
    },
    async updateInstanceStatus(instance) {
      const {job_instance_id} = await getInstanceStatus(this.currBiz, instance.id)

      for (; ;) {
        await sleep(2000)
        const data = await getBkJobLog(this.currBiz, job_instance_id)
        if (data[0].is_finished) {
          let status = data[0].step_results[0].ip_logs[0].log_content
          status = status.split('!!!!!')[1]
          const result = status.split('\n')
          let upToDate = false
          if (instance.config_md5 === result[0]) {
            upToDate = true
          }
          this.instances.filter((inst) => inst.id === instance.id).forEach((inst) => {
            inst.status = (upToDate ? '' : '[配置不是最新]') + result[1]
          })
          break
        }
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.reloadInstances()
    },
    handleSizeChange() {
      this.currentPage = 1
      this.reloadInstances()
    },
    showCreateInstance(defaultData) {
      defaultData = defaultData || {biz_id: this.currBiz, machine: ''}
      this.instanceCreate = true

      this.instanceForm = defaultData
      this.instanceDialogVisible = true
    },
    showModifyInstance(row) {
      this.instanceCreate = false
      this.instanceForm = Object.assign({}, row)
      this.instanceDialogVisible = true
    },
    async saveInstanceForm() {
      if (this.instanceCreate) {
        await addInstance(this.instanceForm)
      } else {
        await updateInstance(this.currBiz, this.instanceForm.id, this.instanceForm)
      }
      this.instanceDialogVisible = false
      await this.reloadInstances()
    },
    async removeInstance(row) {
      try {
        await this.$confirm(`确定删除实例${row.desc}吗？`)
        await deleteInstance(this.currBiz, row.id)
        await this.reloadInstances()
      } catch (e) {

      }
    },
    async onOperationClick(action, row) {
      const {task_instance_id} = await runOperation(this.currBiz, row.id, action)

      for (; ;) {
        await sleep(2000)
        const {is_finished, status} = await getTaskInstance(task_instance_id)
        if (is_finished) {
          if (status === 3) {
            this.$message({message: '操作成功', type: 'success'})
          } else {
            this.$message({message: '操作失败', type: 'error'})
          }
          await this.updateInstanceStatus(row)
          break
        }
      }

      this.$refs.history.handleRefresh()
    },
    async handleBatchOperation(action) {
      // const ids = []
      // for (const sel in this.selection) {
      //   ids.push(sel.id)
      // }
      // runBatchOperation(this.currBiz, ids, action)
      const num = this.selection.length
      const action_name = this.operationButtons.find(o => o.action === action).title
      await this.$confirm(`确定要在【${num}】个实例上执行【${action_name}】操作吗？`)
      this.$refs.batch_operation.runBatch(async task => {
        const {task_instance_id} = await runOperation(this.currBiz, task.id, action)
        for (; ;) {
          await sleep(2000)
          const {is_finished, status, name} = await getTaskInstance(task_instance_id)
          if (is_finished) {
            if (status === 3) {
              return {result: true, name}
            } else {
              return {result: false, name}
            }
          }
        }
      }, this.selection)
      // this.selection.forEach((d) => this.onOperationClick(action, d))
    },
    handleSelectionChange(selection) {
      this.selection = selection
    },
    handleShowSearch() {
      this.show = !this.show
      if (this.show) {
        this.$refs.search_input.focus()
      }
    },
    handleSearch() {
      this.currentPage = 1
      this.currentSearch = this.search
      this.reloadInstances()
    },
    handleRefresh() {
      this.reloadInstances()
    },
    handleShowIpSelect() {
      this.$refs.ip_select.show()
    },
    handlePickIp(ip) {
      this.instanceForm.machine = ip.map((h) => h.bk_cloud_id === 0 ? h.ip : `${h.bk_cloud_id}:${h.ip}`).join(',')
    },
    handleSelectAll() {
      this.loading = true
      this.$refs.dataTable.clearSelection()
      this.$refs.dataTable.toggleAllSelection()
      getInstances(this.currBiz, 1, 1000, this.search)
        .then(data => {
          this.loading = false
          this.selection = data.results
        })
    },
    handleClearSelect() {
      this.$refs.dataTable.clearSelection()
      this.selection = []
    },
    getRowKey(row) {
      return row.id
    },
    async handleMenuCommand(row, cmd) {
      switch (cmd) {
        case 'edit':
          this.showModifyInstance(row)
          break
        case 'delete':
          confirmPromise(`确定要删除${row.desc}吗？`)
            .then(() => {
              this.removeInstance(row)
            })
          break
        case 'clone': {
          const data = deepClone(row)
          data.machine = ''
          this.showCreateInstance(data)
        }
          break
        default:
          break
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .rounded-button {
    outline: none;
    border: none;
    background: transparent;
  }
</style>

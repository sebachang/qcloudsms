<template>
  <el-dialog :visible.sync="dialogVisible" :title="tasktitle" :append-to-body="appendToBody" :modal-append-to-body="modalAppendToBody" @open="handleDialogOpen" @close="handleDialogClose">
    <div style="height: 500px; width: auto">
      <el-progress
        v-if="jobRow.status==='执行成功'"
        :percentage="100"
        status="success"
      />
      <el-progress
        v-else-if="jobRow.status==='执行失败'"
        :percentage="100"
        status="exception"
      />
      <el-progress v-else :percentage="50" />
      <div style="margin-top: 10px; padding: 5px;line-height: 22px;border-radius: 0 2px 2px 0;">
        <el-row :gutter="5">
          <el-col :span="10">
            <div>
              <el-input v-model="jobRow.job_name" :disabled="true">
                <template slot="prepend">名字</template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="7">
            <div>
              <el-input v-model="jobRow.user" :disabled="true">
                <template slot="prepend">账户</template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="7">
            <div>
              <el-input v-model="jobRow.total_time" :disabled="true">
                <template slot="prepend">总时间(s)</template>
              </el-input>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="5" style="margin-top: 5px">
          <el-col :span="5">
            <div>
              <el-input v-model="jobRow.start_way" :disabled="true">
                <template slot="prepend">调用</template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="5">
            <div>
              <el-input v-model="jobRow.status" :disabled="true">
                <template slot="prepend">状态</template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="7">
            <div>
              <el-input v-model="jobRow.start_time" :disabled="true">
                <template slot="prepend">开始</template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="7">
            <div>
              <el-input v-model="jobRow.end_time" :disabled="true">
                <template slot="prepend">结束</template>
              </el-input>
            </div>
          </el-col>
        </el-row>
      </div>
      <div style="margin-top: 10px; padding: 5px;line-height: 22px;border-radius: 0 2px 2px 0;">
        <el-row :gutter="10">
          <el-col :span="12">
            <el-tabs ref="jobInstanceTabe" type="border-card">
              <el-tab-pane label="成功">
                <span slot="label">
                  成功
                  <el-badge
                    :value="currentTotalSuccess"
                    size="mini"
                    type="primary"
                    class="item"
                  />
                </span>

                <div>
                  <el-table
                    :data="jobInstanceData.success.slice((currentPageSuccess-1)*pageSizeSuccess,currentPageSuccess*pageSizeSuccess)"
                    border
                    style="width: 100%"
                    highlight-current-row
                    @current-change="handleSuccessTableCurrentChange"
                  >
                    <el-table-column prop="ip" label="IP" width="180" />
                    <el-table-column prop="exit_code" label="返回码" width="80" />
                    <el-table-column prop="total_time" label="耗时" />
                  </el-table>
                  <el-pagination
                    style="margin-top: 10px;"
                    background
                    layout="prev, pager, next, sizes, total, jumper"
                    :current-page="currentPageSuccess"
                    :page-sizes="[5]"
                    :page-size="pageSizeSuccess"
                    :total="currentTotalSuccess"
                    @size-change="handleSuccessSizeChange"
                    @current-change="handleSuccessCurrentChange"
                  />
                </div>
              </el-tab-pane>
              <el-tab-pane label="失败">
                <span slot="label">
                  失败
                  <el-badge :value="currentTotalFailure" size="mini" class="item" />
                </span>
                <div>
                  <el-table
                    :data="jobInstanceData.failure.slice((currentPageFailure-1)*pageSizeFailure,currentPageFailure*pageSizeFailure)"
                    border
                    style="width: 100%"
                    highlight-current-row
                    @current-change="handleFailureTableCurrentChange"
                  >
                    <el-table-column prop="ip" label="IP" width="180" />
                    <el-table-column prop="exit_code" label="返回码" width="80" />
                    <el-table-column prop="total_time" label="耗时" />
                  </el-table>
                  <el-pagination
                    style="margin-top: 10px;"
                    background
                    layout="prev, pager, next, sizes, total, jumper"
                    :current-page="currentPageFailure"
                    :page-sizes="[5]"
                    :page-size="pageSizeFailure"
                    :total="currentTotalFailure"
                    @size-change="handleFailureSizeChange"
                    @current-change="handleFailureCurrentChange"
                  />
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-col>
          <div>
            <el-col :span="12">
              <el-input v-model="jobInstanceLog" type="textarea" :rows="18" :disabled="true" />
            </el-col>
          </div>
        </el-row>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { mapGetters } from 'vuex'
import { getTaskLog, getTaskInstance } from '@/base/api/task'
import { deepClone } from '@/base/utils'

const defaultSettingInfo = {
  id: -1,
  job_name: '',
  name: '',
  user: '',
  is_finished: '',
  status: '',
  create_time: '',
  start_time: '',
  end_time: '',
  total_time: ''
}

export default {
  name: 'TaskDetails',
  props:
      {
        autoRefresh: {
          type: Boolean,
          default:
            false
        },
        refreshInterval: {
          type: Number,
          default:
            12000
        },
        appendToBody: {
          type: Boolean,
          default: false
        },
        modalAppendToBody: {
          type: Boolean,
          default: false
        }
      },
  computed: {
    ...
    mapGetters(['currBiz'])
  },
  created() {
    clearInterval(this.timer)
    this.timer = null
    this.setTimer()
  },
  data() {
    return {
      timer: null,
      init: false,
      dialogVisible: false,
      jobInstanceLog: '',
      jobInstanceData: {
        success: [],
        failure: []
      },

      currentPageSuccess: 1,
      pageSizeSuccess: 5,
      currentTotalSuccess: 0,

      currentPageFailure: 1,
      pageSizeFailure: 5,
      currentTotalFailure: 0,

      tasktitle: '任务详情',

      jobRow: Object.assign({}, defaultSettingInfo)

    }
  },
  methods: {
    setTimer() {
      if (this.timer == null) {
        this.timer = setInterval(() => {
          if (this.autoRefresh && this.jobRow.is_finished !== true && this.init === true && this.jobRow.id !== -1) {
            this.updateTaskInstance(this.jobRow.id)
            this.updateTaskLog(this.jobRow.id)
          }
        }, this.refreshInterval)
      }
    },

    updateTaskInstance(id) {
      getTaskInstance(id).then(data => {
        this.jobRow = data
        this.tasktitle = '任务详情: ' + data.name
        this.jobRow.start_way = 'API调用'
        this.jobRow.status = this.formatStatus('', '', data.status)
        this.jobRow.start_time = this.formatDateTime('', '', data.start_time)
        this.jobRow.end_time = this.formatDateTime('', '', data.end_time)
        this.jobRow.total_time = data.total_time
        this.jobRow.is_finished = data.is_finished

        this.updateTaskLog(id)
      })
    },

    updateTaskLog(id) {
      getTaskLog(this.jobRow.id).then(data => {
        this.jobInstanceLog = ''
        this.jobInstanceData = { success: [], failure: [] }
        for (const q of data) {
          if (q.is_finished === true) {
            for (const i of q.step_results) {
              if (i.ip_status === 9) {
                this.jobInstanceData.success = this.jobInstanceData.success.concat(i.ip_logs)
              } else {
                this.jobInstanceData.failure = this.jobInstanceData.failure.concat(i.ip_logs)
              }
            }
          }
        }
        this.currentTotalSuccess = this.jobInstanceData.success.length
        this.currentTotalFailure = this.jobInstanceData.failure.length
      })
    },

    show(id) {
      this.jobRow = Object.assign({}, defaultSettingInfo)
      this.jobInstanceData = { success: [], failure: [] }

      this.updateTaskInstance(id)

      this.init = true
      this.dialogVisible = true
    },
    handleSuccessSizeChange: function(size) {
      this.pageSizeSuccess = size
    },

    handleSuccessCurrentChange: function(currentPage) {
      this.currentPageSuccess = currentPage
    },

    handleFailureSizeChange: function(size) {
      this.pageSizeFailure = size
    },

    handleFailureCurrentChange: function(currentPage) {
      this.currentPageFailure = currentPage
    },

    handleSuccessTableCurrentChange(val) {
      try {
        this.jobInstanceLog = val.log_content
      } catch (e) {
        this.jobInstanceLog = ''
      }
    },

    handleFailureTableCurrentChange(val) {
      try {
        this.jobInstanceLog = val.log_content
      } catch (e) {
        this.jobInstanceLog = ''
      }
    },

    // 时间戳转时间
    formatDateTime: function(row, column, cellValue) {
      var moment = require('moment')
      if (cellValue !== undefined) {
        return moment(cellValue).format('YYYY-MM-DD HH:mm:ss')
      } else {
        return ''
      }
    },

    // status字段格式化展示
    formatStatus: function(row, column, cellValue) {
      var ret = ''
      if (cellValue === 1) {
        ret = '未执行'
      } else if (cellValue === 2) {
        ret = '正在执行'
      } else if (cellValue === 3) {
        ret = '执行成功'
      } else if (cellValue === 4) {
        ret = '执行失败'
      } else if (cellValue === 5) {
        ret = '跳过'
      } else if (cellValue === 6) {
        ret = '忽略错误'
      } else if (cellValue === 7) {
        ret = '等待用户'
      } else if (cellValue === 8) {
        ret = '手动结束'
      } else if (cellValue === 9) {
        ret = '状态异常'
      } else if (cellValue === 10) {
        ret = '步骤强制终止中'
      } else if (cellValue === 11) {
        ret = '步骤强制终止成功'
      } else if (cellValue === 12) {
        ret = '步骤强制终止失败'
      }

      return ret
    },

    handleDialogOpen() {

    },

    handleDialogClose() {
      this.$emit('dataRefresh')
    }

  }
}
</script>

<style scoped>

</style>

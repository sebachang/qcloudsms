<template>
  <el-drawer
    title="审批流程"
    :visible.sync="drawer"
    size="55%"
  >
    <el-container style="height: 900px; border: 1px solid #eee">
      <el-aside width="100%">
        <div style="margin:10px 0px 20px 20px;">
          <el-steps direction="vertical" :active="progressActive">
            <el-step v-for="(btn, i) of approvalFlowList" icon="el-icon-edit" :description="btn.description"
                     :title="btn.step_name" :status="btn.state===1?'error':''">
              <el-card slot="description" style="width: 800px;margin:20px 20px 20px 20px;">
                <div style="width: 750px;white-space: pre-line">{{ approvalOrderList[i]===undefined?'待操作人：': '操作人： '
                  }}{{ approvalOrderList[i]===undefined?btn.audit_name.join(' '):approvalOrderList[i].auditor }}
                </div>
                <!--                  <div style="width: 750px;white-space: pre-line">{{ "描述： " + btn.description }} </div>-->
                <div style="width: 750px;white-space: pre-line">{{ '时间： ' }}{{
                  approvalOrderList[i]===undefined?'':approvalOrderList[i].create_time }}
                </div>
                <div style="width: 750px;white-space: pre-line">{{ '结果： ' }}{{ translateStepResult(approvalOrderList[i])
                  }}
                </div>
                <div style="width: 750px;white-space: pre-line">{{ '备注： ' }}{{
                  approvalOrderList[i]===undefined?'':approvalOrderList[i].approval_step_remark }}
                </div>
                <div v-if="btn.task_flag === 0" style="width: 750px;white-space: pre-line">{{ '作业： ' + btn.task_id }}
                </div>
                <div v-if="btn.task_flag === 0" style="width: 750px;">{{ '作业实例：' }}
                  <el-tooltip class="item" effect="dark" content="点击查看详情" placement="right-end">
                    <el-button type="text" size="mini" @click="handleOpen(approvalOrderList[i].task_instance_id)">{{
                      approvalOrderList[i]===undefined?'':approvalOrderList[i].task_instance_id===0?'':approvalOrderList[i].task_instance_id
                      }}
                    </el-button>
                  </el-tooltip>
                </div>
                <div v-if="btn.task_flag === 0" style="width: 750px;">{{ '作业重做：' }}
                  <el-tooltip class="item" effect="dark" content="点击执行" placement="bottom">
                    <el-button type="text" size="mini" @click="jobExecute(approvalOrderList[i].task_instance_id)">{{
                      '执行' }}
                    </el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" content="点击编辑" placement="bottom">
                    <el-button type="text" size="mini" @click="jump(btn.task_id)">{{ '编辑' }}
                    </el-button>
                  </el-tooltip>
                </div>
              </el-card>
            </el-step>
          </el-steps>
        </div>
      </el-aside>
      <task-details ref="taskDetails" :auto-refresh="true" modal-append-to-body append-to-body/>
    </el-container>
  </el-drawer>
</template>

<script>
import {
  getApprovalFlow,
  getApprovalOrder,
  getExceptionOrderList,
  getSuborder,
  postJobExecute
} from '@/api/order_center/order'
import TaskDetails from '@/base/views/components/TaskDetails/index'

export default {
  name: 'ApprovalFlowDrawer',
  components: { TaskDetails },
  data() {
    return {
      drawer: false,
      approvalOrderList: [],
      approvalFlowList: [],
      progressActive: 0,
      tmpOrderId: 0,
      activeName: ''
    }
  },
  methods: {
    show(id, activeName) {
      this.activeName = activeName
      this.drawer = true
      this.tmpOrderId = id
      getApprovalOrder(id).then(data => {
        this.approvalOrderList = data
        this.progressActive = this.approvalOrderList.length

        getApprovalFlow(id).then(data => {
          this.approvalFlowList = data
          for (var i = 0; i < this.approvalOrderList.length; i++) {
            this.approvalOrderList[i].create_time = this.approvalOrderList[i].create_time.split('.')[0].replace('T', ' ')
            for (var c = 0; c < this.approvalFlowList.length; c++) {
              if (this.approvalOrderList[i].approval_step === this.approvalFlowList[c].step) {
                this.$set(this.approvalFlowList[c], 'state', this.approvalOrderList[i].approval_step_result)
              }
            }
          }
        })
      })
    },
    handleOpen(id) {
      this.$refs.taskDetails.show(id)
    },
    translateStepResult(data) {
      const step_result = { 0: '审批通过', 1: '审批未通过', 2: '工单生成', 3: '步骤跳过' }
      if (data === undefined) {
        return '未审批'
      }
      return step_result[data.approval_step_result]
    },
    jobExecute(task_instance_id) {
      var p = { 'task_instance_id': task_instance_id, 'order_id': this.tmpOrderId }
      this.$confirm('确定重新执行作业' + task_instance_id + '?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        postJobExecute(p)
          .then(data => {
            this.$message({
              type: 'success',
              message: '成功!'
            })
            this.$emit('confirm')
          })
      })
    },
    jump(task_id) {
      this.$router.push({ path: '/task/job_uuid/' + task_id })
    }
  }
}
</script>

<style scoped>

</style>

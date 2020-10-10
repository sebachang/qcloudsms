<template>
  <el-drawer
    :title="title_active"
    :visible.sync="visible"
    :with-header="false"
    size="40%"
  >
    <el-container>
      <el-form>
        <el-header>
          <div v-if="approvalFlowList.length !== 0">
            <el-steps finish-status="finish" salign-center simple>
              <el-step
                v-for="btn of approvalFlowList"
                :key="btn.id"
                :description="btn.description + ':' + btn.auditor"
                :status="btn.step===active?'finish':''"
                :title="btn.step_name"
                icon="el-icon-edit"
              />
            </el-steps>
          </div>
        </el-header>
        <el-main>
          <el-card>
            <div>
              <el-form-item>
                <el-input
                  v-model="approvalFlowListOne.step_name"
                  :disabled="active==0"
                  class="input-suffix-s"
                  placeholder="请输入内容"
                >
                  <template slot="prepend">编辑步骤名称</template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input
                  v-model="approvalFlowListOne.task_id"
                  :disabled="true"
                  class="input-suffix-s"
                  placeholder="请输入内容"
                >
                  <template slot="prepend">
                    <el-link :href="taskUrl" type="primary">编辑作业连接</el-link>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="approvalFlowListOne.description" class="input-suffix-s" placeholder="请输入内容">
                  <template slot="prepend">编辑步骤描述</template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-select
                  v-model="approvalFlowListOne.audit_type"
                  default-first-option
                  placeholder="审批人员类型"
                  style="width: 140px"
                >
                  <el-option :value="1" label="用户" />
                  <el-option :value="2" label="用户组" />
                </el-select>
                <el-select
                  v-if="approvalFlowListOne.audit_type===1"
                  v-model="users"
                  default-first-option
                  filterable
                  multiple
                  placeholder="请选择审批人员"
                  style="width: 450px"
                  @change="handleChangeSelect"
                >
                  <el-option
                    v-for="item in allUsers"
                    :key="item.bk_username"
                    :label="item.bk_username"
                    :value="item.bk_username"
                  />
                </el-select>
                <el-select
                  v-if="approvalFlowListOne.audit_type===2"
                  v-model="groups"
                  multiple
                  placeholder="请选择用户组"
                  style="width: 450px"
                  @change="handleChangeSelect"
                >
                  <el-option
                    v-for="group in allGroups"
                    :key="group.id"
                    :label="group.name"
                    :value="group.id.toString()"
                  />
                </el-select>
              </el-form-item>
            </div>
            <div style="margin-top: 30px">
              <el-form-item label="作业开关" label-width="8em">
                <el-switch
                  v-model="approvalFlowListOne.task_flag"
                  :active-value="0"
                  :inactive-value="1"
                  active-text="开启"
                  inactive-text="关闭"
                />
              </el-form-item>
              <el-form-item :label="active==0?'审批完成后通知':'通知开关'" label-width="8em">
                <el-switch
                  v-model="approvalFlowListOne.notify_flag"
                  :active-value="0"
                  :inactive-value="1"
                  active-text="开启"
                  inactive-text="关闭"
                />
              </el-form-item>
              <el-form-item label="步骤开关" label-width="8em">
                <el-switch
                  v-model="approvalFlowListOne.step_flag"
                  :active-value="0"
                  :disabled="active==0"
                  :inactive-value="1"
                  active-text="开启"
                  inactive-text="关闭"
                />
              </el-form-item>
            </div>
          </el-card>
        </el-main>
      </el-form>
      <el-footer style="margin: auto">
        <el-button style="margin-top: 12px;" @click="back">上一步</el-button>
        <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
        <el-button style="margin-top: 12px;" type="primary" @click="submitForm">提交</el-button>
      </el-footer>
    </el-container>
  </el-drawer>
</template>

<script>
import { getApprovalFlowList, putApprovalFlow } from '@/api/order_center/orderConfig'
import { getAllUserInfo } from '@/base/api/user'
import { getGroups } from '@/base/api/roleSetting'
import { mapGetters } from 'vuex'

export default {
  name: 'EditOrderConfig',
  data() {
    return {
      visible: false,
      processLen: 0,
      active: 0,
      title_active: '编辑审批步骤',
      users: [],
      groups: [],
      approvalFlowList: [],
      approvalFlowListOne: {},
      taskUrl: '',
      allUsers: [],
      allGroups: []

    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  methods: {
    reset() {
      this.users = []
      this.groups = []
    },
    show(id) {
      this.reset()
      this.visible = true
      getAllUserInfo().then(data => {
        this.allUsers = data
      })
      getGroups({ biz_id: this.currBiz, page_size: 0 }).then(data => {
        this.allGroups = data.results
      })
      getApprovalFlowList(id).then(data => {
        this.approvalFlowList = data
        this.approvalFlowListOne = this.approvalFlowList[0]
        this.processLen = data.length
        let auditors = []
        if (this.approvalFlowListOne.auditor !== '') {
          auditors = this.approvalFlowListOne.auditor.split(',')
        }
        if (this.approvalFlowListOne.audit_type === 1) {
          this.users = auditors
        } else if (this.approvalFlowListOne.audit_type === 2) {
          this.groups = auditors
        }

        this.taskUrl = '#/task/job_uuid/' + this.approvalFlowListOne.task_id
      })
      this.active = 0
    },
    submitForm() {
      for (const i in this.approvalFlowList) {
        const flow = this.approvalFlowList[i]
        if (flow.step_flag === 0) {
          if (flow.auditor === '') {
            this.$message.error(`请选择流程【第${1 + parseInt(i)}步:${flow.step_name}】审批用户`)
            return
          }
        }
      }
      // console.log(this.server_value)
      for (const i in this.approvalFlowList) {
        putApprovalFlow(this.approvalFlowList[i].id, this.approvalFlowList[i])
      }
      this.visible = false
      this.$notify({
        title: 'Success',
        dangerouslyUseHTMLString: true,
        message: `
              <div> </div>
            `,
        type: 'success'
      })
    },
    refreshCurrentPage() {
      this.reset()
      this.approvalFlowListOne = this.approvalFlowList[this.active]
      let auditors = []
      if (this.approvalFlowListOne.auditor !== '') {
        auditors = this.approvalFlowListOne.auditor.split(',')
      }
      if (this.approvalFlowListOne.audit_type === 1) {
        this.users = auditors
      } else if (this.approvalFlowListOne.audit_type === 2) {
        this.groups = auditors
      }

      this.taskUrl = '#/task/job_uuid/' + this.approvalFlowListOne.task_id
    },
    next() {
      this.active++
      if (this.active === this.processLen) {
        this.active--
      }
      this.refreshCurrentPage()
    },
    back() {
      this.active--
      if (this.active === -1) {
        this.active++
      }
      this.refreshCurrentPage()
    },
    handleChangeSelect(val) {
      this.approvalFlowListOne.auditor = val.join(',')
    }
  }
}
</script>

<style lang="scss" scoped>
  .input-suffix-s {
    width: 600px;
    margin-top: 10px;
  }
</style>

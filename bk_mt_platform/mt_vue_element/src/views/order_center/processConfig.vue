<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-s-custom" /> 审批流程</span></el-tab-pane>
    </el-tabs>
    <el-card class="box-card">
      <el-table
        v-loading="loading1"
        :data="ProcessManagementList"
        :highlight-current-row="true"
        size="small"
        stripe
        style="width: 100%"
      >
        <el-table-column
          label="流程号"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="流程名称"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.process_name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="流程名称"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.process_type }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="流程步骤"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.process_steps }}</span>
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
        >
          <template slot-scope="scope">
            <el-button size="small" type="text" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <div>
      <el-pagination
        :current-page="pageFirst"
        :page-size="pageSizeFirst"
        :total="totalFirst"
        align="center"
        background
        layout="prev, pager, next"
        style="margin:10px 0px 0px 0px;"
        @current-change="handleCurrentChangeFirst"
      />
    </div>
    <el-dialog :visible.sync="dialogVisible0" title="编辑流程">
      <div v-if="approvalFlowList.length != 0">
        <el-steps :active="active" finish-status="finish" salign-center simple>
          <el-step
            v-for="btn of approvalFlowList"
            :description="btn.description + ':' + btn.auditor"
            :title="btn.step_name"
            icon="el-icon-edit"
          />
        </el-steps>
        <br>
        <el-table
          :data="approvalFlowListOne"
          :highlight-current-row="true"
          size="small"
          stripe
          style="width: 100%"
        >
          <el-table-column
            label="步骤"
            width="60"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.step }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="步骤名称"
          >
            <template slot-scope="scope">
              <span><el-input
                v-model="scope.row.step_name"
                :disabled="flag1"
                :placeholder="scope.row.step_name"
              /></span>
            </template>
          </el-table-column>
          <el-table-column
            label="审批人"
          >
            <template slot-scope="scope">
              <span><el-input v-model="scope.row.auditor" :placeholder="scope.row.auditor" /></span>
            </template>
          </el-table-column>
          <el-table-column
            label="描述"
          >
            <template slot-scope="scope">
              <span><el-input v-model="scope.row.description" :placeholder="scope.row.description" /></span>
            </template>
          </el-table-column>
          <el-table-column
            label="作业号"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.task_id }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="作业开关"
          >
            <template slot-scope="scope">
              <span>
                <el-switch
                  v-model="scope.row.task_flag"
                  :active-value="0"
                  :inactive-value="1"
                />
              </span>
            </template>
          </el-table-column>
          <el-table-column
            label="步骤开关"
          >
            <template slot-scope="scope">
              <span>
                <el-switch
                  v-model="scope.row.step_flag"
                  :active-value="0"
                  :inactive-value="1"
                />
              </span>
            </template>
          </el-table-column>
        </el-table>
        <div style="text-align:right;">
          <el-button style="margin-top: 12px;" @click="back">上一步</el-button>
          <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
          <el-button style="margin-top: 12px;" type="primary" :disabled="flag" @click="submitForm">提交</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import { getProcessManagement, getApprovalFlowList, putApprovalFlow } from '@/api/order_center/processConfig'
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      loading1: true,
      activeName: 'first',
      ProcessManagementList: [],
      pageFirst: 1,
      pageSizeFirst: 10,
      totalFirst: 0,
      dialogVisible0: false,
      active: 0,
      approvalFlowList: [],
      approvalFlowListOne: [],
      processLen: 0,
      flag: true,
      flag1: true
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz'
    ])
  },
  created() {
    this.getProcessManagementList()
  },
  methods: {
    getProcessManagementList() {
      getProcessManagement(this.pageFirst, this.currBiz).then(data => {
        this.totalFirst = data.count
        this.ProcessManagementList = data.results
        this.loading1 = false
      })
    },
    handleCurrentChangeFirst(val) {
      this.loading1 = true
      getProcessManagement(val, this.currBiz).then(data => {
        this.totalFirst = data.count
        this.ProcessManagementList = data.results
      })
      this.loading1 = false
    },
    handleEdit(index, row) {
      this.flag1 = true
      this.flag = true
      this.active = 1
      this.dialogVisible0 = true
      this.approvalFlowListOne = []
      getApprovalFlowList(row.id).then(data => {
        this.approvalFlowList = data
        this.approvalFlowListOne.push(data[0])
        this.processLen = data.length
      })
    },
    next() {
      this.flag1 = false
      if (this.active++ >= this.processLen) {
        this.active = this.processLen
      }

      if (this.active === this.processLen) {
        this.flag = false
      }
      this.$set(this.approvalFlowListOne, 0, this.approvalFlowList[this.active - 1])
    },
    back() {
      if (this.active === 1 || this.active === 2) {
        this.flag1 = true
      }
      if (this.active-- <= 1) {
        this.active = 1
      }
      if (this.active !== this.processLen) {
        this.flag = true
      }
      this.$set(this.approvalFlowListOne, 0, this.approvalFlowList[this.active - 1])
    },
    submitForm() {
      for (var i = 0; i < this.approvalFlowList.length; i++) {
        putApprovalFlow(this.approvalFlowList[i].id, this.approvalFlowList[i])
      }
      this.dialogVisible0 = false
      this.$notify({
        title: 'Success',
        dangerouslyUseHTMLString: true,
        message: `
              <div> </div>
            `,
        type: 'success'
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

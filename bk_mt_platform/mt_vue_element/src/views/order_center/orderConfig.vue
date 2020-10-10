<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first">
        <span slot="label"><i class="el-icon-s-order" /> 所有配置</span>
        <el-button size="small" type="primary" icon="el-icon-refresh" @click="handleAutoCreate">生成配置</el-button>
        <el-card class="box-card" style="margin-top: 10px">
          <el-table
            v-loading="loading1"
            size="small"
            :data="tableDataFirst"
            style="width: 100%"
            :highlight-current-row="true"
          >
            <el-table-column label="序号" prop="id" />
            <el-table-column label="工单类型" prop="order_type" />
            <el-table-column label="类型名称" prop="order_name" />
            <el-table-column label="流程名称" prop="process__process_name" />
            <el-table-column label="流程类型" prop="process__process_type" />
            <el-table-column label="流程步骤" prop="process__process_steps" />
            <el-table-column fixed="right" label="操作">
              <template slot-scope="scope">
                <el-button type="text" size="mini" @click="handleEdit(scope.$index, scope.row)">编辑流程</el-button>
                <el-button type="text" size="mini" @click="jump(scope.$index, scope.row)">编辑作业</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        <div>
          <el-pagination style="margin:10px 0px 0px 0px;" background :page-size="pageSizeFirst" :current-page="pageFirst" layout="prev, pager, next" :total="totalFirst" align="center" @current-change="handleCurrentChangeFirst" />
        </div>
      </el-tab-pane>
    </el-tabs>
    <edit-order-config ref="editOrderConfig" />
  </div>
</template>

<script>

import { getOrderConfigList, postAutoCreateOrderConfig, putOrderConfig } from '@/api/order_center/orderConfig'
import { mapGetters } from 'vuex'
import EditOrderConfig from '@/views/order_center/components/EditOrderConfig'

export default {
  components: { EditOrderConfig },
  data() {
    return {
      activeName: 'first',
      loading1: true,
      tableDataFirst: [],
      pageFirst: 1,
      pageSizeFirst: 10,
      totalFirst: 0,
      defaultData: {}
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
    this.getOrderConfigLists()
  },
  methods: {
    getOrderConfigLists() {
      getOrderConfigList(this.pageFirst, this.currBiz).then(data => {
        this.totalFirst = data.count
        this.tableDataFirst = data.results
        this.loading1 = false
      })
    },
    handleCurrentChangeFirst(val) {
      getOrderConfigList(val, this.currBiz).then(data => {
        this.totalFirst = data.count
        this.tableDataFirst = data.results
        this.loading1 = false
      })
    },
    handleAutoCreate() {
      this.defaultData['biz_id'] = this.currBiz
      postAutoCreateOrderConfig(this.defaultData).then(data => {
        getOrderConfigList(this.pageFirst, this.currBiz).then(data => {
          this.totalFirst = data.count
          this.tableDataFirst = data.results
        })
      })
      this.$message({
        message: '配置已经生成',
        type: 'success'
      })
    },
    handleEdit(index, row) {
      this.$refs.editOrderConfig.show(row.id)
    },
    jump(index, row) {
      this.$router.push({ path: '/task/job_module/' + row.process__process_type })
    },
  }
}
</script>

<style>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
    font-size: 12px;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>

<template>
  <el-table
    v-loading="loading"
    size="small"
    :data="tableData"
    style="width: 100%"
  >
    <el-table-column type="expand">
      <template slot-scope="scope">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
            <span style="color: #B00000;font-size:12px;" v-html="value.replace(/\n/g, '<br/>')"></span>
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
    <el-table-column label="工单号" prop="id" />
    <el-table-column label="工单类型" prop="order_type" />
    <el-table-column label="类型名称" prop="order_name" />
    <el-table-column label="提单人" prop="submitter" />
    <el-table-column label="提单时间" prop="create_time" />
    <el-table-column label="工单状态">
      <template slot-scope="scope">
        <span v-if="scope.row.order_state === 0" style="color: #00bb00">审批完成</span>
        <span v-if="scope.row.order_state === 1" style="color: #ffce00">待审批</span>
        <span v-if="scope.row.order_state === 2" style="color: #ff4949">审批拒绝</span>
        <span v-if="scope.row.order_state === 3" style="color: #ff4949">撤销</span>
      </template>
    </el-table-column>
    <el-table-column label="当前步骤" prop="current_approval_step" />
    <el-table-column label="操作" align="center">
      <template slot-scope="{row}">
        <slot :row="row" />
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: 'OrderTable',
  props: {
    data: {
      type: Array
    },
    loading: {
      type: Boolean
    }
  },
  data() {
    return {
      tableData: []
    }
  },
  watch: {
    data(val) {
      this.tableData = val
    }
  }
}
</script>

<style scoped>

</style>

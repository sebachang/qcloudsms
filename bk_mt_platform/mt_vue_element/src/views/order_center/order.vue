<template>
  <div class="app-container" style="overflow-y:hidden">
    <el-tabs v-model="activeName" @tab-click="handleTagClick">
      <el-tab-pane name="first" label="所有工单" />
      <el-tab-pane name="second" label="我的工单" />
      <el-tab-pane name="third" label="我的审批工单" />
      <el-tab-pane name="fourth" label="异常工单" />
    </el-tabs>
    <order-view ref="orderView" :data-provider="dataProvider" @detail="handleApprovalInfo" />
    <approval-dialog ref="approvalDialog" @confirm="reloadCurrentTab" />
    <approval-flow-drawer ref="approvalFlow" @confirm="reloadCurrentTab" />
  </div>
</template>
<script>

import {
  getExceptionOrderList,
  getMyApprovalOrderList,
  getMyOrderList,
  getOrderList,
  updateOrderList
} from '@/api/order_center/order'
import { mapGetters } from 'vuex'
import ApprovalFlowDrawer from '@/views/order_center/components/ApprovalFlowDrawer'
import ApprovalDialog from '@/views/order_center/components/ApprovalDialog'
import OrderView from '@/views/order_center/components/OrderView'
import { deepClone } from '@/base/utils'

export default {
  components: { OrderView, ApprovalDialog, ApprovalFlowDrawer },
  data() {
    return {
      process_name: '交付审批流程',
      process_id: 0,
      activeName: 'first',
      progressActive: 1,
      approvalFlowList: [],
      approvalOrderList: [],
      radio: '',
      remarks: false,

      dialogVisible1: false,
      dialogVisible2: false,
      dialogVisible3: false,

      search_value: '',
      tmp_search_value: '',
      dataProvider: {},
      order_id: 0,
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz',
    ])
  },
  created() {
    this.order_id = this.$route.params && parseInt(this.$route.params.order_id)
    if (this.order_id && this.order_id !== 0) {
      this.activeName = 'third'
    }
    this.reloadCurrentTab()
  },
  methods: {
    reloadCurrentTab() {
      switch (this.activeName) {
        case 'first':
          this.dataProvider = {
            load: (page, callback) => {
              getOrderList(page, '', this.currBiz).then(data => {
                callback(data)
              })
            }
          }
          break
        case 'second':
          this.dataProvider = {
            load: (page, callback) => {
              getMyOrderList(page, this.currBiz).then(data => {
                callback(data)
              })
            },
            operations: [
              {
                name: '撤销',
                check: (row) => {
                  return row.order_state === 1
                },
                click: (row) => {
                  this.handleDel(row)
                },
                style: 'color: red'
              }
            ]
          }
          break
        case 'third':
          this.dataProvider = {
            load: (page, callback) => {
              getMyApprovalOrderList(page, this.currBiz).then(data => {
                callback(data)
              })
            },
            operations: [
              {
                name: '审批',
                click: (row) => {
                  this.handleApproval(row)
                }
              }
            ]
          }
          break
        case 'fourth':
          this.dataProvider = {
            load: (page, callback) => {
              getExceptionOrderList(page, this.currBiz).then(data => {
                callback(data)
              })
            }
          }
          break
      }
    },
    handleIconDel() {
      this.search_value = ''
    },
    handleTagClick(tab, event) {
      this.reloadCurrentTab()
    },
    handleSearch() {
    },
    handleApprovalInfo(row) {
      this.$refs.approvalFlow.show(row.id, this.activeName)
    },
    handleApproval(row) {
      this.$refs.approvalDialog.show(row)
    },
    handleDel(row) {
      this.$confirm('确定撤销工单?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async () => {
        if (row.order_state === '撤销') {
          this.$message({
            type: 'warning',
            message: '工单已撤销!'
          })
          return '1'
        }
        const data = deepClone(row)
        data.order_state = 3
        updateOrderList(row.id, data)
          .then(data => {
            this.reloadCurrentTab()
            this.$message({
              type: 'success',
              message: '撤销成功!'
            })
          })
      }).catch(err => {
        console.error(err)
      })
    }

  }
}
</script>

<style>
  .demo-table-expand {
    font-size: 12px;
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

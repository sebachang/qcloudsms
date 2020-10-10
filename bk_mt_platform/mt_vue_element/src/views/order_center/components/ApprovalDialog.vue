<template>
  <el-dialog :visible.sync="visible" title="工单审批">
    <el-form>
      <el-form-item label="审批结果">
        <el-radio v-model="radio" :label="0">同意</el-radio>
        <el-radio v-model="radio" :label="1">拒绝</el-radio>
      </el-form-item>
      <el-form-item v-if="radio===1" label="拒绝原因" prop="remarks">
        <el-input v-model="remark" type="textarea" />
      </el-form-item>
      <div style="text-align:right;">
        <el-button type="danger" @click="visible=false">
          取消
        </el-button>
        <el-button type="primary" @click="handleConfirmApproval">
          确认
        </el-button>
      </div>
    </el-form>
  </el-dialog>
</template>

<script>
import { postApprovalOrder } from '@/api/order_center/order'

export default {
  name: 'ApprovalDialog',
  data() {
    return {
      visible: false,
      radio: null,
      remark: ''
    }
  },
  methods: {
    show(row) {
      this.visible = true
      this.row = row
      this.remark = ''
      this.radio = null
    },
    handleConfirmApproval() {
      this.settingApproval = {}
      this.settingApproval.order_id = this.row.id
      this.settingApproval.approval_step_result = parseInt(this.radio)
      this.settingApproval.approval_step_remark = this.remark
      postApprovalOrder(this.settingApproval).then(data => {
        this.visible = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: ``,
          type: 'success'
        })
        this.$emit('confirm')
      })
    }
  }
}
</script>

<style scoped>

</style>

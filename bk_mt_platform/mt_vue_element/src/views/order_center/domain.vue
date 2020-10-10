<template>
  <div class="app-container">
    <el-tabs>
      <el-tab-pane label="修改域名申请">
        <el-form ref="form" :model="form" :rules="rules" label-width="80px">
          <el-card>
            <el-form-item label="域名" prop="domain">
              <el-input v-model="form.domain" placeholder="mydomain.moonton.net" style="width: 20em" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
              <el-select v-model="form.type" placeholder="请选择申请类型">
                <el-option label="新增域名解析" value="add" />
                <el-option label="修改域名解析" value="update" />
              </el-select>
            </el-form-item>
            <el-form-item label="记录值" prop="value">
              <el-input v-model="form.value" placeholder="记录值，每行一个" style="width: 20em" type="textarea" />
            </el-form-item>
            <el-form-item label="域名用途" prop="purpose">
              <el-input v-model="form.purpose" maxlength="60" placeholder="域名的用途" style="width: 40em" />
            </el-form-item>
            <el-form-item label="审批备注">
              <el-input v-model="form.remark" placeholder="申请的原因&其他特殊要求" style="width: 40em" type="textarea" />
            </el-form-item>
          </el-card>
          <el-form-item style="float: right; padding: 20px">
            <el-button size="small" type="primary" @click="submitForm">提交</el-button>
            <el-button native-type="reset" size="small">重置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'
import { postOrder } from '@/api/order_center/order'

export default {
  name: 'Domain',
  data() {
    return {
      form: {},
      rules: {
        domain: [{ required: true, trigger: 'blur', message: '请输入域名' }],
        type: [{ required: true, trigger: 'blur', message: '请选择申请类型' }],
        value: [{ required: true, trigger: 'blur', message: '请输入记录值' }],
        purpose: [
          { required: true, trigger: 'blur', message: '请输入域名用途' },
          { max: 60, min: 5, message: '长度在5-60个字符之间', trigger: 'blur' }]
      }
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  methods: {
    submitForm() {
      this.$refs.form.validate(async(ok) => {
        if (ok) {
          const order = { sub_order: deepClone(this.form) }
          order.biz_id = this.currBiz
          order.order_type = 'domain'
          const data = await postOrder(order)
          if (data.id) {
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
                  <div>工单 : ${order.order_type}</div>
                `,
              type: 'success'
            })
            this.$router.push('./order')
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style scoped>

</style>

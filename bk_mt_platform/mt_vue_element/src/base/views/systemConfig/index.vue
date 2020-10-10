<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="180px">
      <el-tabs v-model="currModule" @tab-click="handleTab">
        <el-tab-pane v-for="(item, index) in form.module_list" :key="index" :label="item.name" :name="item.name" />
      </el-tabs>

      <el-form-item v-for="(item, key, index) in form.config_dict" v-if="currModule == item.module.name" :key="index" :label="item.key_desc">
        <el-input ref="inputs" v-model="item.value" style="width: 500px;" :data-key="key" />
        <div class="tipBox" style="width: 500px;" v-text="item.value_desc" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getSystemConfig, addSystemConfig, updateSystemConfig } from '@/base/api/systemConfig'
export default {
  data() {
    return {
      form: {
        module_list: [],
        module_dict: {},
        config_dict: {},
        config_db: {}
      },
      currModule: ''
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ])
  },

  created() {
    this.reloadAllInfo()
  },
  methods: {

    reloadAllInfo() {
      this.form.module_list = []
      this.form.config_dict = {}
      this.form.config_db = {}

      getSystemConfig(this.currBiz).then((res) => {
        this.form.config_db = res.config_db

        const module_dict = {}
        for (const index in res.config_dict) {
          module_dict[res.config_dict[index].module.index] = res.config_dict[index].module

          const unique_index = res.config_dict[index].module.index.toString() + res.config_dict[index].cfg_index.toString()
          this.$set(this.form.config_dict, unique_index, res.config_dict[index])
          this.$set(this.form.config_dict[unique_index], 'key', index)

          if (res.config_db.hasOwnProperty(index)) {
            this.$set(this.form.config_dict[unique_index], 'old_value', res.config_db[index])
            this.$set(this.form.config_dict[unique_index], 'value', res.config_db[index])
            this.$set(this.form.config_dict[unique_index], 'presence', '1')
          } else {
            this.$set(this.form.config_dict[unique_index], 'old_value', '')
            this.$set(this.form.config_dict[unique_index], 'value', res.config_dict[index].default)
            this.$set(this.form.config_dict[unique_index], 'presence', '0')
          }
        }

        for (const index in module_dict) {
          if (this.form.module_list.length === 0) {
            this.currModule = module_dict[index].name
          }
          this.form.module_list.push(module_dict[index])
        }
      })
    },

    handleTab(tab) {
      this.currModule = tab.name
    },

    onSubmit() {
      const inputs = this.$refs.inputs
      for (let i = 0; i < inputs.length; i++) {
        const key = inputs[i].$attrs['data-key']
        const data = {
          'biz_id': this.currBiz,
          'config_key': this.form.config_dict[key].key,
          'config_value': this.form.config_dict[key].value
        }

        if (this.form.config_dict[key].value === this.form.config_dict[key].old_value) {
          continue
        }

        if (this.form.config_dict[key].presence === '1') {
          updateSystemConfig(this.form.config_dict[key].key, data, this.currBiz).then(() => {
            this.$message({ message: '更新成功', type: 'success' })
            this.$set(this.form.config_dict[key], 'old_value', this.form.config_dict[key].value)
          })
        } else if (this.form.config_dict[key].presence === '0') {
          console.log(data)
          addSystemConfig(this.currBiz, data).then(() => {
            this.$set(this.form.config_dict[key], 'presence', '1')
            this.$set(this.form.config_dict[key], 'old_value', this.form.config_dict[key].value)
            this.$message({ message: '添加成功', type: 'success' })
          })
        }
      }
    },

    onCancel() {
      const inputs = this.$refs.inputs
      for (let i = 0; i < inputs.length; i++) {
        const key = inputs[i].$attrs['data-key']
        this.$set(this.form.config_dict[key], 'value', this.form.config_dict[key].old_value)
      }

      this.$message({
        message: '重置配置',
        type: 'success'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
  .tipBox{
    border-radius: 4px;
    color: #515a6e;
    font-size: 12px;
    line-height: 16px;
    margin-bottom: 10px;
    margin-left: 50px;
    padding: 8px 48px 8px 16px;
    position: relative;
    background-color: #f0faff;
    border: 1px solid #abdcff;
    display: inline-block;
  }

</style>

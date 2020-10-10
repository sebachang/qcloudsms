<template>
  <el-popover v-model="visible">
    {{ text }}
    <div style="text-align: right; margin: 0">
      <el-button size="mini" type="text" @click="visible = false">取消</el-button>
      <el-button type="primary" size="mini" @click="handleConfirm()">确定</el-button>
    </div>
    <slot slot="reference" name="reference" />
  </el-popover>
</template>

<script>
export default {
  name: 'Popconfirm',
  props: {
    text: {
      type: String,
      default: '是否确定？'
    }
  },
  data() {
    return {
      visible: false
    }
  },
  methods: {
    handleConfirm() {
      this.visible = false
      this.$emit('confirm')
    }
  }
}
</script>

<style scoped>

</style>

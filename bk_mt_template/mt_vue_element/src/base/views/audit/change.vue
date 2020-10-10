<template>
  <el-dialog :visible.sync="visible" title="显示变更">
    <div v-show="additional_data != ''">
      <b>附加信息: </b>{{ additional_data }}
      <br>
    </div>
    <el-table :data="data">
      <el-table-column label="名称" prop="name" />
      <el-table-column label="旧值" prop="oldValue" />
      <el-table-column label="新值" prop="newValue" />
    </el-table>
  </el-dialog>
</template>

<script>
export default {
  name: 'Change',
  data() {
    return {
      data: [],
      visible: false,
      additional_data: null
    }
  },
  methods: {
    show(row) {
      this.visible = true
      this.additional_data = row.additional_data
      const changes = JSON.parse(row.changes)
      this.data = Object.entries(changes).map(o => ({ 'name': o[0], 'oldValue': o[1][0], 'newValue': o[1][1] }))
    }
  }
}
</script>

<style scoped>

</style>

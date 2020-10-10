<template>
  <el-dialog :visible.sync="visible" :close-on-click-modal="false" :close-on-press-escape="false" title="批量执行操作" :show-close="false">
    <el-card style="width: 100%">
      <div style="padding: 10px;">
        <el-tag type="info">总数：{{ total }}</el-tag>
        <el-tag>已完成：{{ finished }}</el-tag>
        <el-tag type="danger">失败：{{ error }}</el-tag>
      </div>
      <div class="logbox">
        <pre style="padding: 10px">{{ message }}</pre>
      </div>
      <div style="width: 100%; padding: 10px" align="center">
        <el-button :disabled="!allFinished" @click="visible=false">完成</el-button>
      </div>
    </el-card>
  </el-dialog>
</template>

<script>
export default {
  name: 'BatchOperation',
  data() {
    return {
      visible: false,
      message: '',
      total: 0,
      finished: 0,
      allFinished: false,
      error: 0,
      tasks: []
    }
  },
  methods: {
    runBatch(executor, tasks) {
      this.tasks = tasks || []
      this.executor = executor
      this.total = tasks.length
      this.finished = 0
      this.error = 0
      this.visible = true
      this.allFinished = false
      this.message = '开始执行\n'
      this.startTask()
    },
    async startTask() {
      while (this.tasks.length > 0) {
        const currentTask = this.tasks[0]
        this.tasks = this.tasks.slice(1)

        const { result, name } = await this.executor(currentTask)
        if (result) {
          this.message += name + '执行成功\n'
          this.finished++
        } else {
          this.message += name + `执行失败\n`
          this.error++
        }
      }
      this.allFinished = true
      this.$emit('finish')
    }

  }
}
</script>

<style scoped>
  .logbox {
    border: solid 1px #f9f9f9;
    background: #3A3A3A;
    color: #00bb00;
    padding: 5px;
    min-height: 300px;
    max-height: 600px;
    overflow-y: auto;
    width: 100%;
  }
</style>

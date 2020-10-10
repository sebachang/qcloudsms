<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">
        <TaskInstance ref="task_details" :modules="task_module" />
      </div>
    </el-card>
  </div>
</template>

<script>
import TaskInstance from '../components/TaskInstance/index'

export default {
  name: 'TaskInstanceModule',
  components: { TaskInstance },
  data() {
    return {
      task_module: ''
    }
  },
  created() {
    this.task_module = this.$route.params && this.$route.params.module
  }
}
</script>

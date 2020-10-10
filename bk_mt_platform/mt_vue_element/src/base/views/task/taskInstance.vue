<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">
        <TaskInstance ref="task_details" />
      </div>
    </el-card>
  </div>
</template>

<script>
import TaskInstance from '../components/TaskInstance/index'

export default {
  name: 'TaskInstanceObj',
  components: { TaskInstance }
}
</script>

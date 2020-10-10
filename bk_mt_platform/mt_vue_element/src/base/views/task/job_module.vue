<template>
  <JobTable ref="job_table" :jobModule="job_module" />
</template>

<script>
import JobTable from './components/JobTable/index'

export default {
  name: 'JobModule',
  components: { JobTable },
  data() {
    return {
      job_module: ''
    }
  },
  created() {
    this.job_module = this.$route.params && this.$route.params.module
  }
}
</script>

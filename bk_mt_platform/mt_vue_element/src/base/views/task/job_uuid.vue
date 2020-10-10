<template>
  <JobTable ref="job_table" :jobUuid="job_uuid" />
</template>

<script>
import JobTable from './components/JobTable/index'

export default {
  name: 'JobUuid',
  components: { JobTable },
  data() {
    return {
      job_uuid: ''
    }
  },
  created() {
    this.job_uuid = this.$route.params && this.$route.params.uuid
  }
}
</script>

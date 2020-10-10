<template>
  <JobTable ref="job_table" />
</template>

<script>
import JobTable from './components/JobTable/index'

export default {
  name: 'Job',
  components: { JobTable }
}
</script>

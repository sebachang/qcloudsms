<template>
  <span :class="classname">{{ data }}</span>
</template>

<script>
export default {
  name: 'InstanceStatus',
  props: {
    data: {
      type: String
    }
  },
  data() {
    return {
      classname: ''
    }
  },
  watch: {
    data(newval) {
      var styles = {
        '配置文件不存在': 'invalid',
        '已停止': 'error',
        '运行中': 'success'
      }
      this.classname = ''
      for (const msg in styles) {
        if (newval.indexOf(msg) !== -1) {
          this.classname = styles[msg]
          break
        }
      }
    }
  }
}
</script>

<style scoped>
  .error {
    color: red;
  }

  .invalid {
    color: darkgray;
  }

  .success {
    color: forestgreen;
  }
</style>

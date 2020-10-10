<template>
  <div class="search">
    <el-button
      circle
      class="rounded-button search-icon"
      icon="el-icon-search"
      size="mini"
      @click="handleShowSearch"
    />
    <el-input
      ref="search_input"
      v-model="currentValue"
      :class="{show:show}"
      class="search-input"
      placeholder="搜索"
      @focusout.native="show=currentValue.length>0"
      @input="handleChange"
      @keyup.enter.native="handleEnter"
    />
  </div>
</template>

<script>
export default {
  name: 'SearchBox',
  model: { prop: 'value', event: 'input' },
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      show: false,
      currentValue: this.value
    }
  },
  watch: {
    value(value) {
      this.currentValue = value
    }
  },
  methods: {
    handleShowSearch() {
      this.show = !this.show
      if (this.show) {
        this.$refs.search_input.focus()
      }
    },
    handleChange(val) {
      this.$emit('input', val)
    },
    handleEnter() {
      this.$emit('enter', this.currentValue)
    }
  }

}
</script>

<style lang="scss" scoped>

  .search {
    color: #949494;
    display: inline-block;

    .search-icon {
      cursor: pointer;
      vertical-align: middle;
      margin-bottom: 6px;
    }

    .search-input {
      transition: width 0.2s;
      width: 0;
      overflow: hidden;
      background: transparent;
      border-radius: 0;
      display: inline-block;
      vertical-align: middle;

      /deep/ .el-input__inner {
        background: transparent;
        border: none;
        border-radius: 0;
        border-bottom: solid 1px #949494;
      }

      &.show {
        width: 200px;
      }

    }

    .rounded-button {
      background: transparent;
      border: none;
    }

  }
</style>

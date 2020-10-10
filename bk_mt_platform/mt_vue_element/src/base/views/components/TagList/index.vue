<template>
  <div style="border: 1px solid #dcdfe6;border-radius: 4px;">
    <div class="filter-select">
      <div ref="tags" class="filter-select__tags">
        <span v-for="value in localValues">
          <el-tag
            class="filter-tag"
            closable
            disable-transitions
            @close="deleteTag($event, value)"
          >
            <span class="filter-select__tags-text">{{ value }}</span>
          </el-tag>
        </span>
      </div>
      <input
        ref="input"
        slot="reference"
        v-model="inputValue"
        class="filter-select__input"
        placeholder="请输入值按回车添加"
        type="text"
        @focusout="selectOption"
        @keydown.enter.prevent="selectOption"
      >
      </input>
    </div>
  </div>
</template>

<script type="text/babel">
export default {
  name: 'TagList',

  props: {
    values: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      inputValue: '',
      localValues: this.values
    }
  },
  methods: {
    deleteTag(event, tag) {
      this.values.splice(this.localValues.indexOf(tag), 1)
      event.stopPropagation()
      this.$emit('change', this.localValues)
    },

    selectOption() {
      var data = this.inputValue.trim()
      if (data !== '' && this.localValues.indexOf(data) === -1) {
        this.localValues.push(data)
      }
      this.inputValue = ''
      this.$emit('change', this.localValues)
    }
  }
}

</script>

<style lang="scss" scoped>
  .el-tag--medium {
    line-height: 28px;
  }

  .filter-select {
    display: inline-flex;
    /*min-width: calc(100% - 80px);*/
    width: 97%;
    vertical-align: middle;
    /*margin-bottom: 5px;*/
  }

  .filter-select__tags {
    display: flex;
    padding-left: 10px;
  }

  .filter-select__input {
    font-size: 12px;
    background-color: transparent;
    position: relative;
    padding: 0;
    border: 0 none;
    outline: none;
    font-weight: 400;
    cursor: text;
    pointer-events: auto;
    width: 100%;
    height: 35px;
  }

  .filter-tag {
    margin-right: 5px;
    height: 28px;
    font-size: 12px;
    border-radius: 290486px;

    & > > > i {
      color: currentColor
    }
  }

  .autosuggest-menu {
    margin: 0;
    left: 0;
    padding: 4px 0;
    width: 100%;
    border: none;
    border-radius: 4px;
    background-color: #36435c;
    -webkit-box-shadow: 0 4px 8px 0 rgba(48, 62, 90, .2);
    box-shadow: 0 4px 8px 0 rgba(48, 62, 90, .2);
    color: #fff;
    line-height: 32px;

    & > li {
      font-size: 12px;
      line-height: 20px;
      padding: 6px 12px;
      cursor: pointer;
      border-radius: 0;
      background-color: #242e42;

      &:hover {
        background-color: #364352;
      }
    }
  }

  .selectClose {
    width: 56px;
    height: 28px;
    margin-right: -10px;
    padding: 6px 20px;
    border-radius: 28px;
    background-color: #eff4f9;
    border: none;
  }

  .el-button:focus, .el-button:hover {
    color: #dcdfe6;
    border-color: #dcdfe6;
    background-color: #eff4f9;
  }

  .table-filter-bar {
    height: 36px;
    border-radius: 18px;
    background-color: #eff4f9;
    transition: all .3s ease-in-out;
    padding: 0 8px 0 6px;
    border: solid 1px transparent;
    margin: 0 24px 0 0;
    width: 100%;
  }

  .table-filter-bar-active {
    height: 36px;
    border-radius: 18px;
    transition: all .3s ease-in-out;
    padding: 0 8px 0 6px;
    margin: 0 24px 0 0;
    width: 100%;
    background-color: #fff;
    border: 1px solid #79879c;
  }
</style>

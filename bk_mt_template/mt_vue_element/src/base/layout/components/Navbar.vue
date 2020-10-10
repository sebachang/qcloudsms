<template>
  <div class="navbar">
    <hamburger :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />

    <breadcrumb class="breadcrumb-container" />

    <div class="right-menu">
      <template v-if="device!=='mobile'">
        <search class="right-menu-item" />

        <error-log class="errLog-container right-menu-item hover-effect" />

        <screenfull class="right-menu-item hover-effect" />

        <el-tooltip content="布局大小" effect="dark" placement="bottom">
          <size-select class="right-menu-item hover-effect" />
        </el-tooltip>

        <lang-select class="right-menu-item hover-effect" />

      </template>

      <div class="name-container right-menu-item hover-effect">
        <div class="name-wrapper">
          {{ name }}
        </div>
      </div>

      <el-select v-model="currBiz" class="bizList-container right-menu-item hover-effect" size="small" filterable placeholder="请选择" auto-complete="new-password" @change="selectBiz">
        <el-option
          v-for="item in bizList"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>

    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/base/components/Breadcrumb'
import Hamburger from '@/base/components/Hamburger'
import ErrorLog from '@/base/components/ErrorLog'
import Screenfull from '@/base/components/Screenfull'
import SizeSelect from '@/base/components/SizeSelect'
import LangSelect from '@/base/components/LangSelect'
import Search from '@/base/components/HeaderSearch'

export default {
  components: {
    Breadcrumb,
    Hamburger,
    ErrorLog,
    Screenfull,
    SizeSelect,
    LangSelect,
    Search
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'name',
      'device',
      'bizList'
    ]),
    currBiz: {
      get: function() {
        return this.$store.getters.currBiz
      },
      set: function() {
      }
    }
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    selectBiz(value) {
      // 当重新选择业务时, 设置cookie并重新加载整个平台
      this.$store.dispatch('bizList/changeCurrBiz', value).then(data => {
        location.reload()
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .errLog-container {
    display: inline-block;
    vertical-align: top;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 5px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .name-container {
      margin-right: 5px;

      .name-wrapper {
        position: relative;

        .user-name {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }
      }
    }

    .BizList-container {
      margin-right: 15px;
      position: relative;
    }
  }
}
</style>

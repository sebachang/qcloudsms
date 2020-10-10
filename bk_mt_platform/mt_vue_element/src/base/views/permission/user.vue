<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">
        <div class="table-head-container">
          <div align="left" style="float:left">
            <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{ currentTotal }}个中
              {{ multipleSelectionCount }} 个被选中</p>
          </div>
          <div align="right" class="right-menu">
            <div :class="{'show':show}" class="header-search">
              <svg-icon class-name="search-icon" icon-class="search" @click.stop="click" />
              <el-input
                ref="headerSearchSelect"
                v-model="search_value"
                placeholder="搜索"
                class="header-search-select"
              />
            </div>
            <el-button icon="el-icon-refresh" class="header-refresh" circle @click="handleRefresh" />
            <el-dropdown :hide-on-click="false" style="bottom: 5px">
              <el-button
                icon="el-icon-more-outline"
                style="transform: rotate(90deg);background: transparent;border-style: none; outline: none; font-size: 18px;"
                circle
              />
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.bk_username">用户名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.chname">中文名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.qq">QQ</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.phone">电话</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.email">邮箱</el-checkbox>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>

        <el-table
          id="datatable"
          ref="releaseTable"
          v-loading="loading"
          border
          :data="userTableData"
          style="width: 100% "
          :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          @sort-change="sortChange"
          @filter-change="handleFilterChange"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="48" />
          <el-table-column v-if="column_rules.bk_username" prop="bk_username" label="用户名" width="180" />
          <el-table-column v-if="column_rules.chname" prop="chname" label="中文名" width="180" />
          <el-table-column v-if="column_rules.qq" prop="qq" label="QQ" width="180" />
          <el-table-column v-if="column_rules.phone" prop="phone" label="手机号" width="180" />
          <el-table-column v-if="column_rules.email" prop="email" label="邮箱" />
        </el-table>
        <div
          style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid"
        >
          <el-pagination
            background
            layout="prev, pager, next, sizes, total, jumper"
            :current-page="currentPage"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pageSize"
            :total="currentTotal"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getAllUserInfo } from '@/base/api/user'

export default {
  name: 'User',
  components: {},
  data() {
    return {
      show: false,
      timeout: null,
      loading: true,

      currentPage: 1,
      pageSize: 10,
      search_value: '',
      order_value: '-id',
      filter_name: '',
      currentTotal: 0,
      multipleSelection: [],
      multipleSelectionCount: 0,

      users: [],
      userTableData: [],

      column_rules: {
        bk_username: true,
        chname: true,
        qq: false,
        phone: true,
        email: true
      }
    }
  },
  watch: {
    // 监听搜索框
    show(value) {
      if (value) {
        document.body.addEventListener('click', this.close)
      } else {
        document.body.removeEventListener('click', this.close)
      }
    },
    // 监听搜索改变
    search_value(curVal, oldVal) {
      // 实现input连续输入，只发一次请求
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.searchUserChange()
      }, 300)
    }
  },
  created() {
    this.getAllUsers()
  },
  methods: {
    // 刷新
    handleRefresh() {
      this.currentPage = 1
      this.getAllUsers()
    },

    // 打开搜索功能
    click() {
      this.show = !this.show
      if (this.show) {
        this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
      }
    },

    // 关闭搜索功能
    close() {
      this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur()
      this.options = []
      this.show = false
    },

    // 数据显示条数改变
    handleSizeChange(val) {
      this.currentPage = 1
      this.pageSize = val
      this.searchUserChange()
    },

    // 当前页码改变
    handleCurrentChange(val) {
      this.currentPage = val
      this.searchUserChange(val)
    },

    // 搜索
    searchChange() {
      this.currentPage = 1
      this.searchUserChange()
    },

    // 多选
    handleSelectionChange(val) {
      this.multipleSelection = val
      this.multipleSelectionCount = this.multipleSelection.length
    },

    // 获取所有用户
    getAllUsers() {
      this.loading = true
      getAllUserInfo().then(data => {
        this.users = data
        this.searchUserChange()
        this.loading = false
      })
    },

    searchUserChange(val = 1) {
      let cache = []
      if (this.search_value !== '') {
        for (const value of this.users) {
          var reg = RegExp(this.search_value)
          if (value.bk_username.match(reg)) {
            cache.push(value)
          }
        }
      } else {
        cache = this.users
      }

      this.userTableData = cache
      this.currentTotal = this.userTableData.length
      this.currentPage = val

      if (this.pageSize * this.currentPage >= this.currentTotal) {
        this.userTableData = this.userTableData.slice((this.currentPage - 1) * this.pageSize, this.currentTotal)
      } else {
        this.userTableData = this.userTableData.slice((this.currentPage - 1) * this.pageSize, this.pageSize * this.currentPage)
      }
    }

  }
}
</script>

<style lang="scss" scoped>
  .input-suffix {
    width: 180px;
  }

  #datatable > > > .el-checkbox__inner {
    width: 18px;
    height: 18px;

    &:after {
      border: 2px solid #fff;
      top: 3px;
      left: 6px;
      border-left: 0;
      border-top: 0;
    }
  }

  #datatable > > > .caret-wrapper {
    height: 20px;

    .sort-caret.ascending {
      top: -2px;
    }

    .sort-caret.descending {
      top: 10px;
      bottom: 0
    }
  }

  #datatable > > > .el-table__column-filter-trigger {
    line-height: 20px;
    float: right;
  }

  .table-head-container {
    background: #f2f2f2;
    height: 50px;
    margin-top: 10px;
    padding: 10px;
    line-height: 22px;
    border-radius: 4px 4px 0 0;
    border-color: #dfe6ec;
    border-width: 1px 1px 0 1px;
    border-style: solid;
  }

  .right-menu {
    float: right;
    height: 100%;

    &:focus {
      outline: none;
    }
  }

  .header-search {
    display: inline-block;
    padding: 0 5px;
    height: 100%;
    color: #949494;
    vertical-align: text-bottom;

    &:hover {
      color: #1890ff
    }

    .search-icon {
      cursor: pointer;
      vertical-align: middle;
      margin-bottom: 6px;
    }

    .header-search-select {
      transition: width 0.2s;
      width: 0;
      overflow: hidden;
      background: transparent;
      border-radius: 0;
      display: inline-block;
      vertical-align: middle;

      /deep/ .el-input__inner {
        border-radius: 0;
        border: 0;
        padding-left: 0;
        padding-right: 0;
        box-shadow: none !important;
        border-bottom: 1px solid #d9d9d9;
        vertical-align: middle;
        background-color: transparent;
      }
    }

    &.show {
      .header-search-select {
        width: 210px;
        margin-left: 10px;
      }
    }
  }

  .header-refresh {
    background: transparent;
    border-style: none;
    outline: none;
    font-size: 20px;
    display: inline-block;
    padding: 0 5px 0 5px;
    height: 100%;
    color: #949494;
    font-weight: bold;
    vertical-align: text-bottom;

    &:hover {
      color: #1890ff
    }
  }

  .header-jump {
    background: transparent;
    border-style: none;
    outline: none;
    font-size: 20px;
    display: inline-block;
    padding: 0;
    height: 100%;
    color: #949494;
    font-weight: bold;
    vertical-align: text-bottom;
    margin-left: 5px;

    &:hover {
      color: #1890ff
    }
  }

  .permission-tree {
    margin-bottom: 30px;
  }
</style>

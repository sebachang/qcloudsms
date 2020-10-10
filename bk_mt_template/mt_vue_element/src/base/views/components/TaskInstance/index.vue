<template>
  <div>
    <div class="table-head-container">
      <div align="left" style="float:left">
        <el-button
          v-if="false"
          icon="el-icon-circle-plus-outline"
          size="mini"
          type="primary"
          plain
          @click="handleAdd"
        >
          注册任务
        </el-button>
        <el-button v-if="false" icon="el-icon-delete" size="mini" type="danger" plain @click="handleMultipleDelete">
          删除
        </el-button>
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
        <el-button
          icon="el-icon-refresh"
          class="header-refresh"
          circle
          @click="handleRefresh"
        />
        <el-dropdown :hide-on-click="false" style="bottom: 5px">
          <el-button
            icon="el-icon-more-outline"
            class="header-outline"
            circle
          />
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.id">ID</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.job_name">任务名</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.name">实例名</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.user">提交者</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.is_finished">完成状态</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.status">执行状态</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.create_time">创建时间</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.start_time">启动时间</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.end_time">完成时间</el-checkbox>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-checkbox v-model="column_rules.total_time">总耗时</el-checkbox>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>

    <el-table
      id="datatable"
      v-loading="loading"
      border
      :data="tableData"
      style="width: 100% "
      :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
      :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
      @sort-change="sortChange"
      @filter-change="handleFilterChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="48" />
      <el-table-column v-if="column_rules.id" sortable prop="id" label="ID" width="70" />
      <el-table-column v-if="column_rules.job_name" prop="job_name" label="任务名" width="140" />
      <el-table-column v-if="column_rules.name" prop="name" label="实例名" width="300" />
      <el-table-column v-if="column_rules.user" prop="user" label="提交者" width="100" />
      <el-table-column
        v-if="column_rules.is_finished"
        prop="is_finished"
        label="完成状态"
        width="90"
        align="center"
      >
        <template scope="scope">
          <span v-if="scope.row.is_finished===false" style="color: green;font-size:150%"><i
            class="el-icon-loading"
          /></span>
          <span v-else>是</span>
        </template>
      </el-table-column>
      <el-table-column
        v-if="column_rules.status"
        :formatter="formatStatus"
        prop="status"
        label="执行状态"
        width="120"
      >
        <template scope="scope">
          <span v-if="scope.row.status===3" style="color: #37B328">执行成功</span>
          <span v-else-if="scope.row.status===1" style="color:#1f33ff">未执行</span>
          <span v-else-if="scope.row.status===2" style="color:#a9ffff">正在执行</span>
          <span v-else-if="scope.row.status===5" style="color:#ff959f">跳过</span>
          <span v-else-if="scope.row.status===6" style="color:#ff4ca9">忽略错误</span>
          <span v-else-if="scope.row.status===7" style="color:#9092ff">等待用户</span>
          <span v-else-if="scope.row.status===8" style="color:#ff782b">手动结束</span>
          <span v-else-if="scope.row.status===9" style="color:#ff3a3d">状态异常</span>
          <span v-else-if="scope.row.status===10" style="color:#ff0c6b">步骤强制终止中</span>
          <span v-else-if="scope.row.status===11" style="color:#c119ff">步骤强制终止成功</span>
          <span v-else-if="scope.row.status===12" style="color:red">步骤强制终止失败</span>
          <span v-else style="color:red">执行失败</span>
        </template>
      </el-table-column>
      <el-table-column v-if="column_rules.create_time" prop="create_time" label="创建时间" width="180" />
      <el-table-column
        v-if="column_rules.start_time"
        prop="start_time"
        label="启动时间"
        width="180"
      />
      <el-table-column
        v-if="column_rules.end_time"
        prop="end_time"
        label="完成时间"
        width="180"
      />
      <el-table-column v-if="column_rules.total_time" prop="total_time" label="总耗时(s)" />
      <el-table-column label="操作" align="center" width="120">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" icon="el-icon-view" @click="handleOpen(scope)">查看详情</el-button>
        </template>
      </el-table-column>
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

    <TaskDetails ref="task_details" :auto-refresh="true" @dataRefresh="handleRefresh" />
  </div>
</template>

<script>
import { getTaskInstances } from '@/base/api/task'
import { deepClone } from '@/base/utils'
import { mapGetters } from 'vuex'
import TaskDetails from '../TaskDetails/index'

export default {
  name: 'TaskInstance',
  components: { TaskDetails },
  props: {
    modules: {
      type: String,
      default: ''
    },
    uuid: {
      type: String,
      default: ''
    },
    pageSize: {
      type: Number,
      default: 10
    },
    autoRefresh: {
      type: Boolean,
      default: true
    },
    refreshInterval: {
      type: Number,
      default: 60000
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'role',
      'currBiz'
    ])
  },
  data() {
    return {
      show: false,
      timeout: null,
      timer: null,

      filter_job_type_vaule: '',

      currentPage: 1,
      // pageSize: 10,
      search_value: '',
      type_value: '',
      order_value: '-id',
      currentTotal: 0,
      multipleSelection: [],
      multipleSelectionCount: 0,
      tableData: [],

      loading: true,

      column_rules: {
        id: true,
        job_name: true,
        name: true,
        user: true,
        is_finished: true,
        status: true,
        create_time: true,
        start_time: true,
        end_time: true,
        total_time: true
      }

    }
  },
  watch: {
    // 监控类型过滤字段改变
    type_value(val) {
      this.currentPage = 1
      this.getDatas()
    },

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
        this.searchChange()
      }, 300)
    }
  },
  created() {
    this.getDatas()

    clearInterval(this.timer)
    this.timer = null
    this.setTimer()
  },
  beforeDestroy() {
    clearInterval(this.timer)
    this.timer = null
  },
  methods: {

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

    setTimer() {
      if (this.timer == null) {
        this.timer = setInterval(() => {
          if (this.autoRefresh) {
            this.getDatas()
          }
        }, this.refreshInterval)
      }
    },

    handleDialogClose() {
      this.hackReset = -1
    },

    // 排序
    sortChange: function(column, prop, order) {
      if (column.order === 'ascending') {
        this.order_value = column.prop
      } else if (column.order === 'descending') {
        this.order_value = '-' + column.prop
      } else {
        this.order_value = ''
      }
      this.currentPage = 1
      this.getDatas()
    },

    // 多选
    handleSelectionChange(val) {
      this.multipleSelection = val
      this.multipleSelectionCount = this.multipleSelection.length
    },

    // 获取模板数据
    getDatas() {
      this.loading = true
      getTaskInstances({
        'page': this.currentPage,
        'page_size': this.pageSize,
        'job__bk_biz': this.currBiz,
        'search': this.search_value,
        'ordering': this.order_value,
        'job__type': this.filter_job_type_vaule,
        'job__module': this.modules,
        'job__job_uuid': this.uuid
      }).then(data => {
        this.currentTotal = data.count
        this.tableData = data.results
        this.loading = false
      })
    },

    // 数据显示条数改变
    handleSizeChange(val) {
      this.currentPage = 1
      this.pageSize = val
      this.getDatas()
    },

    // 当前页码改变
    handleCurrentChange(val) {
      this.currentPage = val
      this.getDatas()
    },

    // 搜索
    searchChange() {
      this.currentPage = 1
      this.getDatas()
    },

    // 查看任务详情
    handleOpen(scope) {
      this.$refs.task_details.show(scope.row.id)
    },

    // boolean字段格式化展示
    formatBoolean: function(row, column, cellValue) {
      var ret = ''
      if (cellValue) {
        ret = '是'
      } else {
        ret = '否'
      }
      return ret
    },

    // start_way字段格式化展示
    formatStartWay: function(row, column, cellValue) {
      var ret = ''
      if (cellValue === 1) {
        ret = '页面启动'
      } else if (cellValue === 2) {
        ret = 'API调用'
      } else if (cellValue === 3) {
        ret = '定时任务'
      }
      return ret
    },

    // 时间戳转时间
    formatDateTime: function(row, column, cellValue) {
      var moment = require('moment')
      if (cellValue !== undefined) {
        return moment(cellValue).format('YYYY-MM-DD HH:mm:ss')
      } else {
        return ''
      }
    },

    // status字段格式化展示
    formatStatus: function(row, column, cellValue) {
      var ret = ''
      if (cellValue === 1) {
        ret = '未执行'
      } else if (cellValue === 2) {
        ret = '正在执行'
      } else if (cellValue === 3) {
        ret = '执行成功'
      } else if (cellValue === 4) {
        ret = '执行失败'
      } else if (cellValue === 5) {
        ret = '跳过'
      } else if (cellValue === 6) {
        ret = '忽略错误'
      } else if (cellValue === 7) {
        ret = '等待用户'
      } else if (cellValue === 8) {
        ret = '手动结束'
      } else if (cellValue === 9) {
        ret = '状态异常'
      } else if (cellValue === 10) {
        ret = '步骤强制终止中'
      } else if (cellValue === 11) {
        ret = '步骤强制终止成功'
      } else if (cellValue === 12) {
        ret = '步骤强制终止失败'
      }

      return ret
    },

    // 手动刷新
    handleRefresh() {
      this.getDatas()
    },

    // 当talbel中任何一列的过滤条件点击确定和覆盖时，都会触发此事件。
    handleFilterChange(filters) {
      for (const i in filters) {
        if (i === 'job_type') {
          if (filters[i].length !== 0) {
            this.filter_job_type_vaule = filters[i][0]
          } else {
            this.filter_job_type_vaule = ''
          }
        }
      }

      this.currentPage = 1
      this.getDatas()
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

  .header-outline {
    transform: rotate(90deg);
    background: transparent;
    border-style: none;
    outline: none;
    font-size: 20px;
    color: #949494;
    padding: 0 5px 0 5px;

    &:hover {
      color: #1890ff
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

  .script_dialog > > > .CodeMirror {
    height: 500px;
  }
</style>


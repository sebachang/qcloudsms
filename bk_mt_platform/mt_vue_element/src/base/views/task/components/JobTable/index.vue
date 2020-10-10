<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">

        <div class="table-head-container">
          <div align="left" style="float:left">
            <el-button icon="el-icon-circle-plus-outline" size="mini" type="primary" plain @click="handleAdd">
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
                  <el-checkbox v-model="column_rules.job_uuid">任务ID</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.title">任务名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.module">模块</el-checkbox>
                </el-dropdown-item>
                <!--<el-dropdown-item>-->
                <!--<el-checkbox v-model="column_rules.exec_ip">执行IP</el-checkbox>-->
                <!--</el-dropdown-item>-->
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.username">执行用户</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.script_name">脚本名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.create_time">创建时间</el-checkbox>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>

        <el-table
          v-loading="loading"
          border
          class="datatable"
          :data="tableData"
          style="width: 100% "
          :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          @sort-change="sortChange"
          @filter-change="handleFilterChange"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="48" />
          <el-table-column v-if="column_rules.id" sortable prop="id" label="ID" width="80" />
          <el-table-column v-if="column_rules.job_uuid" sortable prop="job_uuid" label="任务ID" width="300" />
          <el-table-column v-if="column_rules.title" prop="title" label="任务名" width="300" />
          <el-table-column v-if="column_rules.module" prop="module" label="模块" width="220" />
          <!--<el-table-column v-if="column_rules.exec_ip" prop="exec_ip" label="执行IP" width="150">-->
          <!--</el-table-column>-->
          <el-table-column v-if="column_rules.username" prop="username" label="执行账户" width="100" />
          <el-table-column v-if="column_rules.script_name" prop="script_name" label="脚本名" width="180" />
          <el-table-column v-if="column_rules.create_time" sortable prop="create_time" label="创建时间" />
          <el-table-column label="操作" width="160">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                plain
                @click="handleEdit(scope)"
              >编辑
              </el-button>
              <el-button
                type="info"
                size="mini"
                @click="handleScriptEdit(scope)"
              >
                脚本
              </el-button>
              <el-button
                v-if="false"
                size="mini"
                type="warning"
                plain
                @click="handleDelete(scope)"
              >删除
              </el-button>
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

        <el-dialog class="script_dialog" :close-on-click-modal="false" :visible.sync="dialogScriptVisible" title="脚本编辑">
          <template>
            <codemirror v-model="content" :options="cmOptions" class="CodeMirror" />
          </template>

          <div style="text-align:right;margin-top: 20px">
            <el-button type="danger" @click="dialogScriptVisible=false">
              取消
            </el-button>
            <el-button type="primary" @click="confirmScript">
              确认
            </el-button>
          </div>
        </el-dialog>

      </div>
      <JobEdit ref="job_edit" @dataRefresh="handleRefresh" />
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getJobs, deleteJob, addJob, updateJob, registerJobs } from '@/base/api/task'
import { deepClone } from '@/base/utils'
import JobEdit from '../JobEdit/index'

// 导入组件
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
// 导入使用的语言语法定义文件
require('codemirror/mode/shell/shell.js')
// 导入选中的theme文件
require('codemirror/theme/blackboard.css')
require('codemirror/theme/dracula.css')
// 导入自动提示核心文件及样式
require('codemirror/addon/hint/show-hint.css')
require('codemirror/addon/hint/show-hint.js')

const defaultSettingInfo = {
  job_uuid: '',
  bk_biz: 0,
  title: '',
  // type: 'script',
  module: 'default',
  // bk_job_id: '-1',
  exec_ip: '[]',
  username: '',
  callback: '',
  script_name: '',
  create_time: ''
}

export default {
  name: 'Job',
  computed: {
    ...mapGetters([
      'name',
      'role',
      'currBiz'
    ])
  },
  components: { codemirror, JobEdit },
  props: {
    jobModule: {
      type: String,
      default: ''
    },
    jobUuid: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      show: false,
      timeout: null,

      currentPage: 1,
      pageSize: 10,
      filter_uuid_value: '',
      search_value: '',
      type_value: '',
      order_value: '-create_at',
      currentTotal: 0,
      multipleSelection: [],
      multipleSelectionCount: 0,
      tableData: [],

      dialogScriptVisible: false,
      dialogType: 'new',

      loading: true,

      template_value: [],

      content: '',
      cmOptions: {
        tabSize: 4,
        mode: 'shell', // 识别的语言shell脚本
        theme: 'dracula', // 编辑器的主题
        lineNumbers: true, // 显示行号
        lineWrapping: true,
        lineWiseCopyCut: true,
        highlightDifferences: true,
        smartIndent: true,
        matchBrackets: true,
        extraKeys: { 'Ctrl': 'autocomplete' }, // 自定义快捷键
        indentWithTabs: true,
        line: true
      },

      type_options: [{
        value: 'script',
        label: '快速脚本'
      }, {
        value: 'template',
        label: '作业模板'
      }],

      column_rules: {
        id: true,
        job_uuid: true,
        title: true,
        // type: true,
        module: true,
        // bk_job_id: true,
        // exec_ip: true,
        username: true,
        script_name: false,
        create_time: true
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

    base64Decode(v) {
      const Base64 = require('js-base64').Base64
      return Base64.decode(v)
    },

    base64Encode(v) {
      const Base64 = require('js-base64').Base64
      return Base64.encode(v)
    },

    getDateTime() {
      var moment = require('moment')
      return moment().format('YYYY-MM-DD HH:mm:ss')
    },

    // 获取数据
    getDatas() {
      this.loading = true
      getJobs({
        'page': this.currentPage,
        'page_size': this.pageSize,
        'bk_biz': this.currBiz,
        'search': this.search_value,
        'ordering': this.order_value,
        'job_uuid': this.jobUuid,
        'module': this.jobModule,
        'type': this.filter_job_type_vaule
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

    // 生成uuid
    uuid() {
      var s = []
      var hexDigits = '0123456789abcdef'
      for (var i = 0; i < 36; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1)
      }
      s[14] = '4' // bits 12-15 of the time_hi_and_version field to 0010
      s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1) // bits 6-7 of the clock_seq_hi_and_reserved to 01
      s[8] = s[13] = s[18] = s[23] = '-'

      return s.join('')
    },

    // 添加
    handleAdd() {
      registerJobs({ 'bk_biz': this.currBiz }).then(data => {
        this.currentPage = 1
        this.getDatas()
        this.$message({
          type: 'success',
          message: '注册成功!'
        })
      })
    },

    // 删除规则
    handleDelete({ $index, row }) {
      this.$confirm('确定删除规则?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await deleteJob(row.id)
        this.currentPage = 1
        await this.getDatas()

        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },

    // 批量删除
    handleMultipleDelete() {
      if (this.multipleSelection.length > 0) {
        this.$confirm('确定删除规则?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async() => {
          for (const i of this.multipleSelection) {
            await deleteJob(i.id)
            this.currentPage = 1
            await this.getDatas()
          }

          this.multipleSelection = []

          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }
        ).catch(err => {
          console.error(err)
        })
      } else {
        this.$message('请选择要删除的行.')
      }
    },

    // 编辑规则
    handleEdit(scope) {
      this.$refs.job_edit.show(scope)
    },

    // 脚本编辑
    handleScriptEdit(scope) {
      this.settingInfo = deepClone(scope.row)
      this.content = ''
      if (this.settingInfo.script) {
        this.content = this.base64Decode(this.settingInfo.script)
      }

      this.dialogScriptVisible = true
    },

    async confirmScript() {
      if (this.content !== '') {
        this.settingInfo.script = this.base64Encode(this.content)
      } else {
        this.settingInfo.script = null
      }
      await updateJob(this.settingInfo.id, this.settingInfo)
      const title = this.settingInfo.title
      this.dialogScriptVisible = false
      this.getDatas()
      this.$notify({
        title: 'Success',
        dangerouslyUseHTMLString: true,
        message: `
            <div>更新 :  ${title}</div>
          `,
        type: 'success'
      })
    },

    // 添加 or 更新提交
    async confirmSetting() {
      await addJob(this.settingInfo).then(() => {
        this.currentPage = 1
        this.getDatas()

        const title = this.settingInfo.title
        this.dialogVisible = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>${type} :  ${title}</div>
          `,
          type: 'success'
        })
      })
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

  .datatable > > > .el-table__column-filter-trigger {
    line-height: 20px;
    float: right;
  }

  .datatable > > > .el-checkbox__inner {
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

  .datatable > > > .caret-wrapper {
    height: 20px;

    .sort-caret.ascending {
      top: -2px;
    }

    .sort-caret.descending {
      top: 10px;
      bottom: 0
    }
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


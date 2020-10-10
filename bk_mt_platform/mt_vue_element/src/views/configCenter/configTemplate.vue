<template>
  <div class="app-container">
    <el-card>
      <div class="clearfix datatable-head-container">
        <el-button
          icon="el-icon-circle-plus-outline"
          plain
          size="mini"
          type="primary"
          @click="showCreateForm()"
        >
          创建模板
        </el-button>
        <div style="float: right">
          <search-box v-model="search" />
        </div>
      </div>
      <el-table
        :data="pageData"
        border
        cell-class-name="datatable-cell"
        class="datatable"
        header-cell-class-name="datatable-header"
        style="width: 100% "
      >
        <el-table-column label="配置名" prop="name" />
        <el-table-column label="描述" prop="desc" />
        <el-table-column label="操作">
          <template slot-scope="{row}">
            <el-button-group>
              <el-button plain size="mini" @click="showModifyForm(row.id)">修改</el-button>
              <el-button plain size="mini" @click="render(row.id)">查看配置</el-button>
              <el-button
                v-clipboard="directLink(row.id)"
                v-clipboard:success="handleCopy"
                plain
                size="mini"
                type="primary"
              >复制链接
              </el-button>
              <el-button plain size="mini" type="danger" @click="remove(row.id)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="[5, 10, 15, 20]"
        :total="totalNum"
        background
        layout="prev, pager, next, sizes, total, jumper"
        @current-change="refreshPageData"
        @size-change="refreshPageData"
      />
      <el-dialog :close-on-click-modal="false" :title="create ? '创建配置模板' : '修改配置模板'" :visible.sync="dialogVisible">
        <el-form :model="form" label-position="top" label-width="80px">
          <el-form-item label="配置名">
            <el-input v-model="form.name" placeholder="nginx" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="form.desc" placeholder="描述" />
          </el-form-item>
          <el-form-item>
            <template slot="label">
              <span>配置模板</span>
              <el-tooltip content="内置变量ServerIP">
                <el-icon class="el-icon-info" />
              </el-tooltip>
            </template>
            <codemirror v-model="form.content" :options="cmOptions" class="editor" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveForm">
              <template v-if="create">创建</template>
              <template v-else>保存</template>
            </el-button>
            <el-button type="danger" @click="closeDialog">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-card>
  </div>
</template>

<style scoped>
  .editor {
    line-height: 1em;
  }

</style>

<script>

import { addConfigTemplate, deleteConfigTemplate, getConfigTemplate, updateConfigTemplate } from '@/api/configCenter'
import { mapGetters } from 'vuex'
// 导入组件
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import SearchBox from '@/base/components/SearchBox/index'
import Clipboard from '@/base/directive/clipboard/index'
import { get_download_site } from '@/base/api/appUtil'
// 导入使用的语言语法定义文件
require('codemirror/mode/javascript/javascript')
// 导入选中的theme文件
require('codemirror/theme/dracula.css')
// 导入自动提示核心文件及样式
require('codemirror/addon/hint/show-hint.css')
require('codemirror/addon/hint/show-hint.js')
var url = require('url')

export default {
  components: { SearchBox, codemirror },
  directives: { Clipboard },
  data() {
    return {
      templates: [],
      tableData: [],
      pageData: [],
      dialogVisible: false,
      create: false,
      search: '',
      cmOptions: {
        mode: 'text/javascript',
        theme: 'dracula',
        line: true,
        lineNumbers: true
      },
      form: {
        name: '',
        desc: '',
        content: ''
      },
      currentPage: 1,
      totalNum: 0,
      pageSize: 10,
      downloadSite: ''
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ]),
    routesData() {
      return this.routes
    }
  },
  watch: {
    templates() {
      this.refreshTableData()
    },
    search() {
      this.refreshTableData()
    },
    tableData() {
      this.refreshPageData()
    }
  },
  created() {
    this.reloadTemplate()
    get_download_site().then(d => {
      this.downloadSite = d.site
    })
  },
  methods: {
    refreshPageData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.pageData = this.tableData.slice(start, end)
    },
    refreshTableData() {
      this.tableData = this.templates.filter((tpl) => tpl.name.includes(this.search) || tpl.desc.includes(this.search))
      this.totalNum = this.tableData.length
    },
    reloadTemplate() {
      getConfigTemplate(this.currBiz)
        .then((data) => {
          this.templates = data
        })
    },
    showModifyForm(id) {
      const data = this.getRecordById(id)
      Object.assign(this.form, data)
      this.dialogVisible = true
      this.create = false
    },
    showCreateForm() {
      this.form = {
        name: '',
        desc: '',
        content: ''
      }
      this.dialogVisible = true
      this.create = true
    },
    saveForm() {
      if (this.create) {
        this.form.biz_id = this.currBiz
        addConfigTemplate(this.form)
          .then((data) => {
            this.dialogVisible = false
            this.reloadTemplate()
          })
      } else {
        updateConfigTemplate(this.currBiz, this.form.id, this.form)
          .then((data) => {
            this.dialogVisible = false
            this.reloadTemplate()
          })
      }
    },
    closeDialog() {
      this.dialogVisible = false
    },
    remove(id) {
      const record = this.getRecordById(id)
      this.$confirm(`确定删除${record.name}吗?`)
        .then(() => {
          deleteConfigTemplate(this.currBiz, id)
            .then((data) => {
              this.reloadTemplate()
            })
        })
    },
    getRecordById(id) {
      for (const k in this.templates) {
        if (this.templates[k].id === id) {
          return this.templates[k]
        }
      }
    },
    directLink(id) {
      const base = process.env.VUE_APP_BASE_API
      return url.resolve(this.downloadSite, base + '/config_center/template/render/' + id + '/')
    },
    render(id) {
      window.open(this.directLink(id), '_blank')
    },
    handleCopy() {
      this.$message({ type: 'success', message: '已经复制到剪贴板' })
    }
  }
}
</script>

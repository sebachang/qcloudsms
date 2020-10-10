<template>
  <div class="app-container">
    <el-card>
      <div class="clearfix datatable-head-container">
        <el-button icon="el-icon-circle-plus-outline" plain size="mini" type="primary" @click="showCreateProcess()">添加进程
        </el-button>
        <el-button v-clipboard="searchUrl" v-clipboard:success="handleCopy" plain size="mini">
          复制模糊查找API
        </el-button>
        <search-box v-model="search" style="float: right" />

      </div>
      <el-table
        :data="pageData"
        border
        cell-class-name="datatable-cell"
        header-cell-class-name="datatable-header"
        style="width: 100%"
      >
        <el-table-column label="名称" prop="name" />
        <el-table-column label="绑定的配置模板" prop="template_name" />
        <el-table-column label="配置文件" prop="conf_path" />
        <el-table-column label="启动脚本" prop="start_cmd" />
        <el-table-column label="停止脚本" prop="stop_cmd" />
        <el-table-column label="重启脚本" prop="restart_cmd" />
        <el-table-column label="重载脚本" prop="reload_cmd" />
        <el-table-column label="操作" width="280px">
          <template slot-scope="{row}">
            <el-button v-clipboard:success="handleClipboard" v-clipboard:value="apiUrl(row)" plain size="mini">
              复制api地址
            </el-button>
            <el-button plain size="mini" type="warning" @click="showUpdateProcess(row)">修改</el-button>
            <el-button plain size="mini" type="danger" @click="removeProcess(row)">删除</el-button>
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
      <el-dialog
        :close-on-click-modal="false"
        :title="processCreate ? '添加进程' : '修改进程'"
        :visible.sync="processDialogVisible"
      >
        <el-form ref="form" :model="processForm" label-width="120px">
          <el-form-item label="名称">
            <el-input v-model="processForm.name" />
          </el-form-item>
          <el-form-item label="绑定的配置模板">
            <el-select v-model="processForm.template">
              <el-option v-for="template in templates" :key="template.id" :label="template.name" :value="template.id" />
            </el-select>
            <el-button icon="el-icon-refresh" @click="reloadTemplates()" />
          </el-form-item>
          <el-form-item label="配置文件">
            <el-input v-model="processForm.conf_path" />
          </el-form-item>
          <el-form-item label="启动脚本">
            <el-input v-model="processForm.start_cmd" />
          </el-form-item>
          <el-form-item label="停止脚本">
            <el-input v-model="processForm.stop_cmd" />
          </el-form-item>
          <el-form-item label="重启脚本">
            <el-input v-model="processForm.restart_cmd" />
          </el-form-item>
          <el-form-item label="重载脚本">
            <el-input v-model="processForm.reload_cmd" />
          </el-form-item>
          <el-form-item label="程序包名">
            <el-select v-model="processForm.pack_name">
              <el-option v-for="p in packages" :key="p" :label="p" :value="p" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveProcessForm()">保存</el-button>
            <el-button type="danger" @click="processDialogVisible=false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
const url = require('url')
import { getConfigTemplate } from '@/api/configCenter'
import { addProcess, deleteProcess, getPackageList, getProcesses, updateProcess } from '@/api/processManage'
import { mapGetters } from 'vuex'
import SearchBox from '@/base/components/SearchBox/index'
import { parseString } from 'xml2js'
import Clipboard from '@/base/directive/clipboard/index'
import { get_download_site } from '@/base/api/appUtil'

export default {
  name: 'Process',
  components: { SearchBox },
  directives: { Clipboard },
  data() {
    return {
      processes: [],
      tableData: [],
      pageData: [],
      processDialogVisible: false,
      processCreate: false,
      processForm: {},
      templates: [],
      totalNum: 0,
      pageSize: 10,
      currentPage: 1,
      search: '',
      searchUrl: '',
      packages: [],
      downloadSite: ''
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  watch: {
    processes() {
      this.refreshTableData()
    },
    tableData() {
      this.refreshPageData()
    },
    search() {
      this.refreshTableData()
    }
  },
  created() {
    this.reloadProcesses()
    this.reloadTemplates()
    get_download_site().then(d => {
      this.downloadSite = d.site
      const base = process.env.VUE_APP_BASE_API
      this.searchUrl = url.resolve(d.site, base + `/process_manage/search/${this.currBiz}/{name}`)
    })
    this.reloadPackages()
  },
  methods: {
    refreshTableData() {
      this.tableData = this.processes.filter((p) => p.name.includes(this.search))
      this.totalNum = this.tableData.length
    },
    refreshPageData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.pageData = this.tableData.slice(start, end)
    },
    reloadProcesses() {
      getProcesses(this.currBiz)
        .then((data) => {
          this.processes = data
        })
    },
    reloadPackages() {
      getPackageList(this.currBiz)
        .then(data => {
          parseString(data.content, (err, result) => {
            if (err !== null) {
              this.$message({ type: 'error', message: '获取包列表失败' })
              return
            }
            window.p = result
            this.packages = result.ListBucketResult.Contents.map((f) => f.Key[0]).filter((s) => !s.endsWith('/')).map((s) => s.slice(s.lastIndexOf('/') + 1))
          })
        })
    },
    reloadTemplates() {
      getConfigTemplate(this.currBiz)
        .then((data) => {
          this.templates = data
        })
    },
    showCreateProcess() {
      this.processCreate = true
      this.processForm = {
        biz_id: this.currBiz,
        start_cmd: 'start.sh',
        stop_cmd: 'stop.sh',
        restart_cmd: 'restart.sh',
        reload_cmd: 'reload.sh'
      }
      this.processDialogVisible = true
    },
    showUpdateProcess(row) {
      this.processForm = Object.assign({}, row)
      this.processCreate = false
      this.processDialogVisible = true
    },
    removeProcess(row) {
      this.$confirm(`确定删除进程${row.name}吗?`)
        .then(() => {
          deleteProcess(this.currBiz, row.id)
            .then(() => {
              this.reloadProcesses()
            })
        })
    },
    saveProcessForm() {
      if (this.processCreate) {
        addProcess(this.processForm)
          .then(() => {
            this.processDialogVisible = false
            this.reloadProcesses()
          })
      } else {
        updateProcess(this.currBiz, this.processForm.id, this.processForm)
          .then(() => {
            this.processDialogVisible = false
            this.reloadProcesses()
          })
      }
    },
    apiUrl(row) {
      const base = process.env.VUE_APP_BASE_API
      return url.resolve(this.downloadSite, base + '/process_manage/' + row.id + '/list/')
    },
    handleClipboard() {
      this.$message.success('复制成功')
    },
    handleCopy() {
      this.$message.success('已经复制到剪贴板')
    }
  }
}
</script>

<style scoped>

</style>

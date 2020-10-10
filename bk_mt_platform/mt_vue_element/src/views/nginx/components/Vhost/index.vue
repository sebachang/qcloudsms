<template>
  <div>
    <div class="table-head-container">
      <div align="left" style="float:left">
        <el-button @click="handleAdd" icon="el-icon-circle-plus-outline" size="mini" type="primary" plain>
          添加
        </el-button>
        <el-button @click="handleMultipleDelete" icon="el-icon-delete" size="mini" type="danger" plain>删除
        </el-button>
        <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{currentTotal}}个中
          {{multipleSelectionCount}} 个被选中</p>
      </div>
      <div align="right" class="right-menu">
      </div>
    </div>
    <el-table border id="datatable"
              v-loading="loading"
              ref="releaseTable"
              :data="dataTableData"
              style="width: 100% "
              @sort-change='sortChange'
              @filter-change="handleFilterChange"
              @selection-change="handleSelectionChange"
              :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
              :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}">
      <el-table-column type="selection" width="48">
      </el-table-column>
      <el-table-column prop="id" label="ID" sortable width="80">
      </el-table-column>
      <el-table-column prop="domain_data.name" label="域名" width="220">
      </el-table-column>
      <el-table-column prop="port" label="端口" width="80">
      </el-table-column>
      <el-table-column prop="ssl" label="SSL" width="80" :formatter="handelFormatSSL">
      </el-table-column>
      <el-table-column prop="root" label="Root" width="80">
      </el-table-column>
      <el-table-column label="Index">
        <template slot-scope="scope">
          <el-tag v-for="index in scope.row.index.trim().split(' ')" style="margin-right: 5px;">{{ index }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140">
        <template slot-scope="scope">
          <el-button-group>
            <el-tooltip class="item" effect="dark" content="编辑" placement="top">
              <el-button type="primary" icon="el-icon-edit" @click="handleEdit(scope)"></el-button>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="删除" placement="top">
              <el-button type="primary" icon="el-icon-delete" @click="handleDelete(scope)"></el-button>
            </el-tooltip>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div
      style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        layout="prev, pager, next, sizes, total, jumper"
        :current-page="currentPage"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="pageSize"
        :total="currentTotal"
      >
      </el-pagination>
    </div>

    <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑':'添加'" append-to-body>

      <el-form :model="settingInfo" :rules="rules" ref="ruleForm" label-width="80px" label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="域名" prop="domain">
              <el-select v-model="settingInfo.domain" filterable  placeholder="请选择域名">
                <el-option
                  v-for="item in domain_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="证书" prop="cert">
              <el-select v-model="settingInfo.cert" filterable  placeholder="请选择证书" clearable>
                <el-option
                  v-for="item in cert_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="类型">
              <el-select v-model="vhost_type" filterable  placeholder="虚拟主机类型">
                <el-option
                  v-for="item in vhost_type_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="端口" prop="port">
              <el-input v-model="settingInfo.port" placeholder="端口"/>
            </el-form-item>
          </el-col>
          <el-col :span="8">

            <el-form-item label="SSL" prop="ssl">
              <el-switch v-model="settingInfo.ssl"></el-switch>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Root" prop="root">
              <el-input v-model="settingInfo.root" placeholder="根路径"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Index" prop="index">
              <el-input v-model="settingInfo.index" placeholder="主文件"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <div style="width:100%;height:100%" id="fullscreenvhost">
        <div class="table-head-container">
          <div align="left" style="float:left">
            <el-button @click="handleRendering" icon="el-icon-circle-plus-outline" size="mini" type="primary" plain>
              渲染
            </el-button>
            <el-button @click="handleRenderingClear" icon="el-icon-delete" size="mini" type="danger" plain>清空
            </el-button>
          </div>
          <div align="right" class="right-menu">
            <el-button @click="handleFullCreeen" icon="el-icon-full-screen" class="header-refresh" circle></el-button>
          </div>
        </div>
        <codemirror v-model="settingInfo.content" :options="cmOptions" class="CodeMirror"
                    :style="{height:(isFullscreen?'calc(100% - 50px)':'400px')}" ref="myCmVhost"/>
      </div>
      <div style="text-align:right; padding-top: 5px">
        <el-button type="danger" @click="dialogVisible=false">
          取消
        </el-button>
        <el-button type="primary" @click="confirmSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {
    getVhosts,
    deleteVhost,
    addVhost,
    updateVhost,
    getConfigList,
    getTemplateVhost,
  } from '@/api/nginx'
  import {
    getCertList,
  } from '@/api/certificate'
  import {
    getDomainList,
  } from '@/api/certificate'
  import {deepClone} from '@/base/utils'
  import {mapGetters} from 'vuex'

  // 导入组件
  import {codemirror} from 'vue-codemirror'
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
    config: null,
    cluster: null,
    domain: null,
    cert: null,
    port: 80,
    ssl: false,
    root: 'html',
    index: 'index.html index.htm',
    content: "",
  };

  export default {
    name: "Vhost",
    components: {codemirror},
    computed: {
      ...mapGetters([
        'name',
        'role',
        'currBiz'
      ]),
      codemirror() {
        return this.$refs.myCmVhost.codemirror
      },
      scrollerHeight: function () {
        if (this.isFullscreen) {
          return window.innerHeight + 'px';
        } else {
          return 400 + 'px';
        }

      }
    },
    props: {
      ConfigModule: {
        type: Number,
        default: 0,
      },
      ClusterModule: {
        type: Number,
        default: 0,
      },
    },
    watch: {
      ConfigModule() {
        this.settingInfo.config = this.ConfigModule;
        this.getVhostTableDatas();
      },
      isFullscreen(value) {
        if (value) {
          this.codemirror.setSize('auto', '100%');
        } else {
          this.codemirror.setSize('auto', '400px');
        }
      },
    },
    data() {
      return {
        show: false,
        timeout: null,
        loading: true,
        isFullscreen: false,

        currentPage: 1,
        pageSize: 10,
        search_value: '',
        order_value: '-id',
        currentTotal: 0,
        multipleSelection: [],
        multipleSelectionCount: 0,

        dataTableData: [],
        account_list: [],
        cert_list: [],

        settingInfo: Object.assign({}, defaultSettingInfo),
        dialogVisible: false,
        dialogType: 'new',

        rules: {
          domain: [
            {required: true, message: '请选择域名', trigger: 'change'}
          ],
          port: [
            {required: true, message: '请输入端口', trigger: 'change'}
          ],
          ssl: [
            {required: true, message: '请选择ssl', trigger: 'change'}
          ],
          root: [
            {required: true, message: '请配置根', trigger: 'change'}
          ],
          index: [
            {required: true, message: '请配置默认文档', trigger: 'change'}
          ],
        },

        column_rules: {
          id: true,
          config_name: true,
          domain_name: true,
          port: true,
          ssl: true,
          root: true,
          index: true,
        },

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
          extraKeys: {'Ctrl': 'autocomplete'}, // 自定义快捷键
          indentWithTabs: true,
          line: true,
          fullScreen: this.isFullscreen,
        },

        config_list: [],
        domain_list: [],
        vhost_type: 1,
        vhost_type_list: [{'id': 1, 'name': '基础虚拟主机'}, {'id': 2, 'name': '代理虚拟主机'}, {'id': 3, 'name': '80端口重写'}],
      }
    },
    created() {
      this.getVhostTableDatas();
    },
    methods: {

      handleFullCreeen() {
        let self = this;
        let element = document.getElementById("fullscreenvhost");

        if (this.isFullscreen) {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        } else {
          if (element.requestFullscreen) {
            element.requestFullscreen();
            document.addEventListener("fullscreenchange", function () {
              if (document.fullscreenElement === null) {
                self.isFullscreen = false;
              }
            });
          } else if (element.webkitRequestFullScreen) {
            element.webkitRequestFullScreen();
          } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
          } else if (element.msRequestFullscreen) {
            // IE11
            element.msRequestFullscreen();
          }
        }
        this.isFullscreen = !this.isFullscreen;
      },
      handleRefresh() {
        this.currentPage = 1;
        this.getVhostTableDatas();
      },

      // 获取配置列表
      getConfigListDatas() {
        getConfigList().then(data => {
          this.config_list = data
        })
      },

      // 获取域名列表
      getDomainListDatas() {
        getDomainList().then(data => {
          this.domain_list = data
        })
      },

      // 获取证书列表
      getCertListDatas() {
        getCertList().then(data => {
          this.cert_list = data
        })
      },

      //打开搜索功能
      click() {
        this.show = !this.show
        if (this.show) {
          this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
        }
      },

      //关闭搜索功能
      close() {
        this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur()
        this.options = []
        this.show = false
      },

      handelFormatSSL(row) {
        if (row.ssl) {
          return "是"
        } else {
          return "否"
        }
      },

      // 数据显示条数改变
      handleSizeChange(val) {
        this.currentPage = 1;
        this.pageSize = val;
        this.getVhostTableDatas()
      },

      // 当前页码改变
      handleCurrentChange(val) {
        this.currentPage = val;
        this.getVhostTableDatas()
      },

      // 搜索
      searchChange() {
        this.currentPage = 1;
        this.getVhostTableDatas()
      },

      // 多选
      handleSelectionChange(val) {
        this.multipleSelection = val;
        this.multipleSelectionCount = this.multipleSelection.length;
      },

      // 排序
      sortChange: function (column, prop, order) {
        if (column.order === "ascending") {
          this.order_value = column.prop
        } else if (column.order === "descending") {
          this.order_value = '-' + column.prop
        } else {
          this.order_value = ''
        }
        this.currentPage = 1;
        this.getVhostTableDatas()
      },

      handleRendering() {
        this.$confirm('重新渲染会清理掉原有配置,确定要渲染?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.settingInfo.cluster = this.ClusterModule;
          getTemplateVhost(this.vhost_type, this.settingInfo).then(data => {
            this.settingInfo.content = data.config;
          })

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>渲染 :  ${this.settingInfo.domain_data.name}</div>
          `,
            type: 'success'
          })
        }).catch(err => {
          console.error(err)
        })
      },

      handleRenderingClear() {
        this.$confirm('清空配置会导致原有配置丢失,确定要清空?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.settingInfo.content = '';

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>清空 :  ${this.settingInfo.domain_data.name}</div>
          `,
            type: 'success'
          })
        }).catch(err => {
          console.error(err)
        })
      },

      // 获取证书表格数据
      getVhostTableDatas() {
        if (this.ConfigModule > 0) {
          this.loading = true;
          getVhosts({
            "config": this.ConfigModule,
            "page": this.currentPage,
            "page_size": this.pageSize,
            "search": this.search_value,
            "ordering": this.order_value,
            "bk_biz": this.currBiz
          }).then(data => {
            this.currentTotal = data.count;
            this.dataTableData = data.results;
            this.loading = false;
          })
        }
      },

      //获取当前时间
      getDateTime() {
        var moment = require('moment');
        return moment().format("YYYY-MM-DD HH:mm:ss")
      },

      // 添加
      handleAdd() {
        this.getCertListDatas();
        this.getConfigListDatas();
        this.getDomainListDatas();
        this.settingInfo = Object.assign({}, defaultSettingInfo);
        this.settingInfo.bk_biz = this.currBiz;
        this.settingInfo.config = this.ConfigModule;
        try {
          this.$refs['ruleForm'].resetFields();
        } catch (e) {
        }
        this.dialogType = 'new';
        this.dialogVisible = true
      },

      // 批量删除
      handleMultipleDelete() {
        if (this.multipleSelection.length > 0) {
          this.$confirm('确定删除规则?', '警告', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(async () => {

              for (let i of this.multipleSelection) {
                await deleteVhost(i.id);
                this.currentPage = 1;
                await this.getVhostTableDatas()
              }

              this.multipleSelection = [];

              this.$message({
                type: 'success',
                message: '删除成功!'
              })

            }
          ).catch(err => {
            console.error(err)
          })
        } else {
          this.$message('请选择要删除的行.');
        }
      },

      // 编辑
      handleEdit(scope) {
        this.getCertListDatas();
        this.getConfigListDatas();
        this.getDomainListDatas();
        this.dialogType = 'edit';
        this.radio = 1;
        this.dialogVisible = true;
        this.settingInfo = deepClone(scope.row);
        try {
          this.$refs['ruleForm'].resetFields();
        } catch (e) {
        }
      },

      // 删除
      handleDelete({$index, row}) {
        this.$confirm('确定删除?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          await deleteVhost(row.id);
          this.currentPage = 1;
          await this.getVhostTableDatas();

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>删除 :  ${row.domain_data.name}</div>
          `,
            type: 'success'
          })
        }).catch(err => {
          console.error(err)
        })
      },

      // 添加 or 更新提交
      confirmSetting() {
        this.$refs['ruleForm'].validate(async (valid) => {
          if (valid) {
            const isEdit = this.dialogType === 'edit';
            var type = "添加";
            var title = "虚拟主机"

            if (isEdit) {
              type = "更新";
              await updateVhost(this.settingInfo.id, this.settingInfo)
              title = this.settingInfo.domain_data.name;

            } else {
              await addVhost(this.settingInfo)
            }

            this.currentPage = 1;
            this.getVhostTableDatas();

            this.dialogVisible = false;
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
            <div>${type} :  ${title}</div>
          `,
              type: 'success'
            })
          }
        })
      },

      // 当talbel中任何一列的过滤条件点击确定和覆盖时，都会触发此事件。
      handleFilterChange(filters) {
        console.log(filters)
        // console.log('筛选条件发生变化')
        let row = null
        let val = null
        // 拷贝filters的值。
        for (const i in filters) {
          row = i // 保存 column-key的值，如果事先没有为column-key赋值，系统会自动生成一个唯一且恒定的名称
          val = filters[i]
        }
        const filter = [{
          row: row,
          op: 'contains',
          value: val
        }];
        console.log(filter)
      },
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

  .header-download {
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

  .help-message {
    padding-left: 10px;
    font-size: 12px;
    line-height: 18px;
    margin-bottom: 0;
  }

  .alert-info {
    color: #31708f;
    background-color: #d9edf7;
    border-color: #bce8f1;
  }

  .alert {
    padding: 15px;
    border: 1px solid transparent;
    border-radius: 4px;
  }

  .CodeMirror {
    & > > > .CodeMirror {
      height: 400px;
    }
  }
</style>


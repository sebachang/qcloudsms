<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="alert alert-info help-message">
        集群管理,通过集群功能可以管理nginx集群的部署/发布/更新.
      </div>
      <div class="clearfix">

        <div class="table-head-container">
          <div align="left" style="float:left">
            <el-button icon="el-icon-circle-plus-outline" size="mini" type="primary" plain @click="handleAdd">
              添加
            </el-button>
            <el-button icon="el-icon-delete" size="mini" type="danger" plain @click="handleMultipleDelete">删除
            </el-button>
            <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{ currentTotal }}个中
              {{ multipleSelectionCount }} 个被选中</p>
          </div>
          <div align="right" class="right-menu">
            <div :class="{'show':show}" class="header-search">
              <svg-icon class-name="search-icon" icon-class="search" @click.stop="click"/>
              <el-input
                ref="headerSearchSelect"
                v-model="search_value"
                placeholder="搜索"
                class="header-search-select"
              />
            </div>
            <el-button icon="el-icon-refresh" class="header-refresh" circle @click="handleRefresh"/>
            <el-button icon="el-icon-share" class="header-jump" circle @click="handleJump"/>
            <el-dropdown :hide-on-click="false" style="bottom: 5px">
              <el-button
                icon="el-icon-more-outline"
                style="transform: rotate(90deg);background: transparent;border-style: none; outline: none; font-size: 18px;"
                circle
              />
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.id">ID</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.name">集群名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.config_name">配置名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.package">软件包</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.path">工作路径</el-checkbox>
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
          :data="clusterTableData"
          style="width: 100% "
          :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          @sort-change="sortChange"
          @filter-change="handleFilterChange"
          @selection-change="handleSelectionChange"
          @row-click="handleRowClick"
        >
          <el-table-column type="selection" width="48"/>
          <el-table-column v-if="column_rules.id" prop="id" label="ID" sortable width="80"/>
          <el-table-column v-if="column_rules.name" prop="name" label="集群名" width="180"/>
          <el-table-column v-if="column_rules.config_name" prop="config_name" label="配置名" width="180"/>
          <el-table-column v-if="column_rules.path" prop="path" label="工作路径" width="280"/>
          <el-table-column v-if="column_rules.package" prop="package" label="包"/>
          <el-table-column label="操作" width="220">
            <template slot-scope="scope">
              <el-button-group>
                <el-button @click.stop="handleEdit(scope)" size="mini" type="info" plain>编辑</el-button>
                <el-button @click.stop="handleDelete(scope)" size="mini" type="warning" plain>删除</el-button>
                <el-dropdown size="mini" plain>
                  <el-button size="mini" type="primary" plain @click.stop="">
                    其它<i class="el-icon-arrow-down el-icon--right"></i>
                  </el-button>
                  <el-dropdown-menu slot="dropdown" plain>
                    <el-dropdown-item icon="el-icon-video-play" @click.native="addInstanceOperatorRow(scope,'start')">
                      启动
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-refresh" @click.native="addInstanceOperatorRow(scope,'reload')">重载
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-switch-button" @click.native="addInstanceOperatorRow(scope,'stop')">
                      停止
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-s-help" @click.native="addInstanceOperatorRow(scope,'restart')">重启
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-s-promotion"
                                      @click.native="addInstanceOperatorRow(scope,'publish')">发布
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-edit-outline"
                                      @click.native="addInstanceOperatorRow(scope,'pull_config')">下发配置
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-attract"
                                      @click.native="addInstanceOperatorRow(scope,'pull_config_restart')">下发并重启
                    </el-dropdown-item>
                    <el-dropdown-item icon="el-icon-paperclip"
                                      @click.native="addInstanceOperatorRow(scope,'pull_config_reload')">下发并重载
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </el-button-group>
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

        <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑':'添加'" :close-on-click-modal="false">
          <el-form ref="ruleForm" :model="settingInfo" :rules="rules" label-width="80px" label-position="left">

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="集群名" prop="name">
                  <el-input v-model="settingInfo.name" placeholder="集群名"/>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="配置名" prop="config">
                  <el-select v-model="settingInfo.config" filterable  placeholder="请选择配置">
                    <el-option
                      v-for="item in config_list"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="包" prop="package">
                  <el-select v-model="settingInfo.package" filterable  placeholder="请选择包">
                    <el-option
                      v-for="item in packages"
                      :key="item"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="工作路径" prop="path">
                  <el-input v-model="settingInfo.path" placeholder="工作路径"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="模块路径" prop="module_path">
                  <el-input v-model="settingInfo.module_path" placeholder="模块路径"/>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="日志路径" prop="log_path">
                  <el-input v-model="settingInfo.log_path" placeholder="日志路径"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="证书路径" prop="cert_path">
                  <el-input v-model="settingInfo.cert_path" placeholder="证书路径"/>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="主配置" prop="conf_path">
                  <el-input v-model="settingInfo.conf_path" placeholder="主配置"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="虚拟主机" prop="vhost_path">
                  <el-input v-model="settingInfo.vhost_path" placeholder="虚拟主机"/>
                </el-form-item>
              </el-col>
            </el-row>


          </el-form>
          <IpMultipleSelect ref="ip_multiple_select" :hosts="hosts" v-if="isAlive" @update="handleUpdateHosts"/>
          <div style="text-align:right;">
            <el-button type="danger" @click="dialogVisible=false">
              取消
            </el-button>
            <el-button type="primary" @click="confirmSetting">
              确认
            </el-button>
          </div>
        </el-dialog>

        <el-dialog :visible.sync="dialogInstanceVisible" title="集群实例" :close-on-click-modal="false">
          <HostInstance ref="host_instance" :hosts="host_list" :config_name="active_name" :config="active"
                        @callback="handleCallback"/>
        </el-dialog>

        <div class="tip">
          <p>任务历史</p>
        </div>
        <TaskInstance ref="task_instance" :modules="moduleName" :uuid="job_uuid" :page-size="5"/>

      </div>
      <IpSelect ref="ip_select" @pick="handlePickIp"/>
    </el-card>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import {
    getClusters,
    deleteCluster,
    addCluster,
    updateCluster,
    getConfigList,
    getConfigListById,
    getTemplate,
    getInstance,
    getJobLog,
    addOperator,
  } from '@/api/nginx'
  import {runJob} from '@/base/api/task'
  import {deepClone} from '@/base/utils'
  import TaskInstance from '@/base/views/components/TaskInstance/index'
  import IpSelect from '@/base/views/components/IpSelect/index'
  import IpMultipleSelect from '@/base/views/components/IpMultipleSelect/index'
  import {getPackageList} from '@/api/processManage'
  import {parseString} from 'xml2js'

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

  import HostInstance from './components/Instance/index'

  const defaultSettingInfo = {
    path: '/data/app/openresty-moonton',
    log_path: '/data/applog/openresty',
    conf_path: '/data/app/openresty-moonton/nginx/conf',
    vhost_path: '/data/app/openresty-moonton/nginx/conf/vhost',
    cert_path: '/data/app/openresty-moonton/nginx/conf/ssl',
    module_path: '/data/app/openresty-moonton/nginx/conf/modules',
    name: '',
    config_name: '',
    hosts: ''
  }

  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

  export default {
    name: 'NginxCluster',
    components: {TaskInstance, IpSelect, IpMultipleSelect, codemirror, HostInstance},
    computed: {
      ...mapGetters([
        'name',
        'role',
        'currBiz'
      ])
    },
    data() {
      return {
        moduleName: 'nginx_manage',
        job_uuid: 'cae2a8c5-c537-4637-927d-c5d3a2e42e78',

        show: false,
        timeout: null,
        loading: true,

        currentPage: 1,
        pageSize: 10,
        search_value: '',
        order_value: '-id',
        currentTotal: 0,
        multipleSelection: [],
        multipleSelectionCount: 0,

        clusterTableData: [],
        hosts: [],
        host_list: [],

        settingInfo: Object.assign({}, defaultSettingInfo),
        dialogVisible: false,
        dialogScriptVisible: false,
        dialogInstanceVisible: false,
        content: '',
        dialogType: 'new',
        isAlive: true,
        hostChange: false,
        hostTemp: '',

        rules: {
          name: [
            {required: true, message: '请输入集群名', trigger: 'change'}
          ],
          config: [
            {required: true, message: '请选择配置名', trigger: 'change'}
          ],
          package: [
            {required: true, message: '请选择包', trigger: 'change'}
          ],
          path: [
            {required: true, message: '请输入工作路径', trigger: 'change'}
          ],
          log_path: [
            {required: true, message: '请输入日志路径', trigger: 'change'}
          ],
          conf_path: [
            {required: true, message: '请输入配置路径', trigger: 'change'}
          ],
          vhost_path: [
            {required: true, message: '请输入虚拟主机路径', trigger: 'change'}
          ],
          cert_path: [
            {required: true, message: '请输入证书路径', trigger: 'change'}
          ],
          module_path: [
            {required: true, message: '请输入模块路径', trigger: 'change'}
          ],
        },

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
          line: true
        },

        column_rules: {
          id: true,
          name: true,
          config_name: true,
          package: true,
          path: true,
        },

        config_list: [],
        packages: [],

        active: 0,
        active_name: '',
        timer: null,
        job_id: 0,
      }
    },
    watch: {
      // 监听搜索框
      show(value) {
        if (this.search_value === '') {
          if (value) {
            document.body.addEventListener('click', this.close)
          } else {
            document.body.removeEventListener('click', this.close)
          }
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
      this.getClusterTableDatas();

      clearInterval(this.timer)
      this.timer = null
      this.setTimer()
    },
    methods: {
      setTimer() {
        if (this.timer == null) {
          this.timer = setInterval(() => {
            if (this.active !== 0 && this.dialogInstanceVisible === true) {
              this.getInstanceDatas()
            }
          }, 2000)
        }
      },

      async getInstanceDatas() {
        await getInstance(this.active).then(data => {
          var job_id = data.job_instance_id
          this.getInstanceJobLog(job_id)
        })
      },

      async getInstanceJobLog(job_id) {
        let num = 0;
        for (; ;) {
          await sleep(3000)
          const data = await getJobLog({'bk_biz': this.currBiz, 'job_id': job_id});

          if (data) {
            data[0].step_results[0].ip_logs.forEach((item) => {
              let status = item.log_content;
              status = status.split('!!!!!')[1];
              try {
                let result = status.trim().split('\n');
                if (this.active !== 0 && this.dialogInstanceVisible === true) {
                  this.host_list.filter((inst) => inst.ip === item.ip).forEach((inst) => {
                    inst.status = result[1]
                  })
                }
              } catch {
              }
            });
            this.$refs.host_instance.handleRefresh()
            break
          }
          if (num >= 10) {
            break
          }
          num = num + 1;
        }
      },

      handleRefresh() {
        this.currentPage = 1
        this.getClusterTableDatas()
      },


      handleJump() {
        this.$router.push('/task/job_uuid/' + this.job_uuid)
      },

      // 打开搜索功能
      click() {
        if (this.search_value === '') {
          this.show = !this.show
          if (this.show) {
            this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
          }
        }
      },

      // 关闭搜索功能
      close() {
        if (this.search_value === '') {
          this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur();
          this.show = false
        }
      },

      // 数据显示条数改变
      handleSizeChange(val) {
        this.currentPage = 1
        this.pageSize = val
        this.getClusterTableDatas()
      },

      // 当前页码改变
      handleCurrentChange(val) {
        this.currentPage = val
        this.getClusterTableDatas()
      },

      // 搜索
      searchChange() {
        this.currentPage = 1
        this.getClusterTableDatas()
      },

      // 多选
      handleSelectionChange(val) {
        this.multipleSelection = val
        this.multipleSelectionCount = this.multipleSelection.length
      },

      // 排序
      sortChange: function (column, prop, order) {
        if (column.order === 'ascending') {
          this.order_value = column.prop
        } else if (column.order === 'descending') {
          this.order_value = '-' + column.prop
        } else {
          this.order_value = ''
        }
        this.currentPage = 1
        this.getClusterTableDatas()
      },

      // 获取配置列表
      getConfigListDatas() {
        getConfigList().then(data => {
          this.config_list = data
        })
      },

      // 获取配置列表
      getConfigListByIdDatas(id) {
        getConfigListById(id).then(data => {
          this.config_list = data
        })
      },

      // 获取配置列表
      getPackageListDatas() {
        getPackageList(this.currBiz)
          .then(data => {
            parseString(data.content, (err, result) => {
              if (err !== null) {
                this.$message({type: 'error', message: '获取包列表失败'})
                return
              }
              window.p = result
              this.packages = result.ListBucketResult.Contents.map((f) => f.Key[0]).filter((s) => !s.endsWith('/') && s.search("openresty") != -1).map((s) => s.slice(s.lastIndexOf('/') + 1))
            })
          })
      },

      // 获取集群表格数据
      getClusterTableDatas() {
        this.loading = true
        getClusters({
          'page': this.currentPage,
          'bk_biz': this.currBiz,
          'page_size': this.pageSize,
          'search': this.search_value,
          'ordering': this.order_value
        }).then(data => {
          this.currentTotal = data.count
          this.clusterTableData = data.results
          this.loading = false
        })
      },

      // 获取当前时间
      getDateTime() {
        var moment = require('moment')
        return moment().format('YYYY-MM-DD HH:mm:ss')
      },

      // 脚本编辑
      handleScriptEdit(scope) {
        this.content = ''

        getTemplate(scope.row.id).then(data => {
          this.content = data.config
        })

        this.dialogScriptVisible = true
      },

      // 添加
      handleAdd() {
        this.getConfigListDatas();
        this.getPackageListDatas();
        this.hostChange = false
        this.settingInfo = Object.assign({}, defaultSettingInfo)
        this.settingInfo.bk_biz = this.currBiz
        this.hosts = []
        this.reload()
        try {
          this.$refs['ruleForm'].resetFields()
        } catch (e) {
        }
        this.dialogType = 'new'
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
              for (const i of this.multipleSelection) {
                await deleteCluster(i.id)
                this.currentPage = 1
                await this.getClusterTableDatas()
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

      base64Encode(v) {
        const Base64 = require('js-base64').Base64
        return Base64.encode(v)
      },

      handleRowClick(row) {
        this.host_list = JSON.parse(row.hosts);
        this.host_list.forEach((obj) => obj.status = '未知')
        this.active = row.id;
        this.active_name = row.name;
        this.dialogInstanceVisible = true;
      },

      // 部署证书
      handleDeploy(scope) {
        const obj = deepClone(scope.row)
        getCert(obj.cert).then(data => {
          let title = obj.domain_name
          // const cert_domain=data.domain
          const cert_name = data.name

          if (cert_name) {
            title = cert_name
          }

          let script = obj.script

          if (script !== '') {
            script = this.base64Encode(script)
          }

          runJob(this.job_uuid, {
            'bk_biz': this.currBiz,
            'ip_list': obj.hosts,
            'script_param': title + ' ' + obj.path + ' ' + this.base64Encode(data.crt) + ' ' + this.base64Encode(data.key) + ' ' + script
          }).then(data => {
            this.$refs.task_instance.handleRefresh()

            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
            <div>部署 :  ${title}</div>
          `,
              type: 'success'
            })
          })
        })
      },

      // 编辑
      handleEdit(scope) {
        this.getPackageListDatas();
        this.dialogType = 'edit'
        this.dialogVisible = true
        this.settingInfo = deepClone(scope.row)
        this.getConfigListByIdDatas(this.settingInfo.config);
        this.hostChange = false
        this.hostTemp = this.settingInfo.hosts
        this.hosts = JSON.parse(this.settingInfo.hosts)
        this.reload()
        try {
          this.$refs['ruleForm'].resetFields()
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
          await deleteCluster(row.id)
          this.currentPage = 1
          await this.getClusterTableDatas()

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>删除 :  ${row.domain}</div>
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
            const isEdit = this.dialogType === 'edit'
            var type = '添加'

            if (isEdit) {
              type = '更新'
              await updateCluster(this.settingInfo.id, this.settingInfo).then(() => {
                if (this.settingInfo.hosts !== this.hostTemp) {
                  this.hostChange = true
                }
              })
            } else {
              await addCluster(this.settingInfo).then(() => {
                this.hostChange = true
              })
            }

            this.currentPage = 1
            this.getClusterTableDatas()

            const title = this.settingInfo.name
            this.dialogVisible = false
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
            <div>${type} :  ${title}</div>
          `,
              type: 'success'
            })
            if (this.hostChange) {
              this.host_list = JSON.parse(this.settingInfo.hosts);
              this.host_list.forEach((obj) => obj.status = '未知')
              this.active = this.settingInfo.id;
              this.active_name = this.settingInfo.name;
              this.dialogInstanceVisible = true;
            }
          }
        })
      },

      handleShowIpSelect() {
        this.$refs.ip_select.show()
      },

      handleCallback() {
        this.dialogInstanceVisible = false;
        this.$refs.task_instance.handleRefresh();
      },
      handlePickIp(ip) {
        // this.settingInfo.hosts = ip.map((h) => h.bk_cloud_id === 0 ? h.ip : `${h.bk_cloud_id}:${h.ip}`).join(',')
        this.settingInfo.hosts = JSON.stringify(ip)
      },

      handleUpdateHosts(hosts) {
        this.settingInfo.hosts = JSON.stringify(hosts)
      },

      // 当talbel中任何一列的过滤条件点击确定和覆盖时，都会触发此事件。
      handleFilterChange(filters) {
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
        }]
      },

      reload() {
        this.isAlive = false
        this.$nextTick(() => (this.isAlive = true))
      },

      addInstanceOperatorRow(scop, action) {
        var hosts = JSON.parse(scop.row.hosts);
        addOperator(scop.row.id, {'action': action, 'hosts': hosts}).then(data => {
          this.$refs.task_instance.handleRefresh();

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>${action}: ${scop.row.name}</div>
          `,
            type: 'success'
          })
        })
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

  .tip {
    padding-left: 16px;
    background-color: #f2f2f2;
    /*border-radius: 4px;*/
    border-left: 5px solid #949494;
    margin: -10px 0;
    height: 40px;
    line-height: 40px;
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

  .script_dialog > > > .CodeMirror {
    height: 600px;
  }

  .el-dialog {
    width: 60%;
  }
</style>


<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="alert alert-info help-message">
        集群管理,通过集群的发布功能可以将对应域名的证书发布到集群相关的主机上.
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
                  <el-checkbox v-model="column_rules.domain_name">域名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.cert_domain">证书</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.cert_name">文件名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.script">服务管理</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.path">证书路径</el-checkbox>
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
        >
          <el-table-column type="selection" width="48"/>
          <el-table-column v-if="column_rules.id" prop="id" label="ID" sortable width="80"/>
          <el-table-column v-if="column_rules.name" prop="name" label="集群名" width="180"/>
          <el-table-column v-if="column_rules.domain_name" prop="domain_name" label="域名" width="180"/>
          <el-table-column v-if="column_rules.cert_domain" prop="cert_domain" label="证书" width="180"/>
          <el-table-column v-if="column_rules.cert_name" prop="cert_name" label="文件名" width="180"/>
          <el-table-column v-if="column_rules.script" prop="script" label="服务管理" width="180"/>
          <el-table-column v-if="column_rules.path" prop="path" label="证书路径"/>
          <el-table-column label="操作" width="240">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                plain
                @click="handleEdit(scope)"
              >编辑
              </el-button>
              <el-button
                size="mini"
                type="info"
                plain
                @click="handleDeploy(scope)"
              >部署
              </el-button>
              <el-button
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

        <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑':'添加'">
          <el-form ref="ruleForm" :model="settingInfo" :rules="rules" label-width="80px" label-position="left">

            <el-form-item label="集群名" prop="name">
              <el-input v-model="settingInfo.name" placeholder="集群名"/>
            </el-form-item>
            <el-form-item label="域名" prop="domain">
              <el-select v-model="settingInfo.domain" placeholder="请选择域名">
                <el-option
                  v-for="item in domain_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="证书" prop="cert">
              <el-select v-model="settingInfo.cert" placeholder="请选择证书">
                <el-option
                  v-for="item in cert_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <!--<el-form-item label="主机" prop="hosts">-->
            <!--<el-input v-model="settingInfo.hosts" placeholder="主机"/>-->
            <!--</el-form-item>-->
            <!--<el-form-item label="主机" prop="hosts">-->
            <!--<el-input v-model="settingInfo.hosts" placeholder="主机">-->
            <!--<el-button slot="append" @click="handleShowIpSelect()">选择主机</el-button>-->
            <!--</el-input>-->
            <!--</el-form-item>-->

            <el-form-item label="证书路径" prop="path">
              <el-input v-model="settingInfo.path" placeholder="证书路径"/>
            </el-form-item>
            <el-form-item label="服务管理" prop="script">
              <el-input v-model="settingInfo.script" placeholder="服务管理"/>
            </el-form-item>
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
    getDomainList,
    getCertList,
    getCert
  } from '@/api/certificate'
  import {runJob} from '@/base/api/task'
  import {deepClone} from '@/base/utils'
  import TaskInstance from '@/base/views/components/TaskInstance/index'
  import IpSelect from '@/base/views/components/IpSelect/index'
  import IpMultipleSelect from '@/base/views/components/IpMultipleSelect/index'

  const defaultSettingInfo = {
    name: '',
    bk_biz: null,
    domain: null,
    cert: null,
    script: '',
    path: '',
    hosts: ''
  }

  export default {
    name: 'Cluster',
    components: {TaskInstance, IpSelect, IpMultipleSelect},
    computed: {
      ...mapGetters([
        'name',
        'role',
        'currBiz'
      ])
    },
    data() {
      return {
        moduleName: 'certificate',
        job_uuid: '03a358e1-f32e-425e-9745-de06eecb85c9',

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

        settingInfo: Object.assign({}, defaultSettingInfo),
        dialogVisible: false,
        dialogType: 'new',
        isAlive: true,

        rules: {
          name: [
            {required: true, message: '请输入集群名', trigger: 'change'}
          ],
          domain: [
            {required: true, message: '请选择域名', trigger: 'change'}
          ],
          cert: [
            {required: true, message: '请选择证书', trigger: 'change'}
          ],
          path: [
            {required: true, message: '请输入证书路径', trigger: 'change'}
          ]
        },

        column_rules: {
          id: true,
          name: true,
          domain_name: true,
          cert_domain: true,
          cert_name: true,
          script: false,
          path: true
        },

        domain_list: [],
        cert_list: []

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
          this.searchChange()
        }, 300)
      }
    },
    created() {
      this.getClusterTableDatas()
    },
    methods: {
      handleRefresh() {
        this.currentPage = 1
        this.getClusterTableDatas()
      },
      handleJump() {
        this.$router.push('/task/job_uuid/' + this.job_uuid)
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

      // 获取证书表格数据
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

      // 添加
      handleAdd() {
        this.getDomainListDatas()
        this.getCertListDatas()
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
        this.getDomainListDatas()
        this.getCertListDatas()
        this.dialogType = 'edit'
        this.dialogVisible = true
        this.settingInfo = deepClone(scope.row)
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
              await updateCluster(this.settingInfo.id, this.settingInfo)
            } else {
              await addCluster(this.settingInfo)
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
          }
        })
      },

      handleShowIpSelect() {
        this.$refs.ip_select.show()
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
        }]
        console.log(filter)
      },

      reload() {
        this.isAlive = false
        this.$nextTick(() => (this.isAlive = true))
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
</style>


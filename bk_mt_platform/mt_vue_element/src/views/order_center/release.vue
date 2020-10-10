<template>
  <el-container :style="height">
    <el-aside width="250px" style="border-right:1px solid #C0C0C0">
      <div style="margin: 10px;">
        <el-tree
          ref="tree"
          :data="treeData"
          :props="defaultProps"
          default-expand-all
          :expand-on-click-node="false"
          :render-content="renderContent"
        />
      </div>
    </el-aside>
    <el-main>
      <el-tabs v-model="activeName">
        <el-tab-pane label="阿里云发布申请" name="first">
          <div class="filter-container">
            <el-collapse v-model="activeTab">
              <el-collapse-item title="查询" name="search">
                <template slot="title">
                  <p class="tip">请选择发布列表:</p>
                </template>
                <template>
                  <el-select
                    v-model="server_value"
                    filterable
                    multiple
                    default-first-option
                    style="width:500px"
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in SelectServers"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </template>
                <el-input v-model="division_value" placeholder="请输入division / 组id" style="width: 420px; margin-left: 30px">
                  <template slot="prepend">Division/组 搜索:</template>
                  <el-button slot="append" icon="el-icon-search" @click="searchChange" />
                </el-input>
              </el-collapse-item>
            </el-collapse>
          </div>

          <el-table
            :data="tableData"
            height="320"
            stripe
            highlight-current-row
            style="width: 100%"
            @current-change="handleCurrentChange"
          >
            <!--
            <el-table-column
              type="selection"
              width="40">
            </el-table-column>
            -->
            <el-table-column
              v-if="tableColumn.server"
              prop="server"
              label="Server"
              width="200"
            />
            <el-table-column
              v-if="tableColumn.division"
              prop="division"
              label="Division"
              width="250"
            />
            <el-table-column
              prop="node"
              label="Node"
              width="250"
            />
            <el-table-column
              prop="status"
              label="Status"
              width="150">
              <template slot-scope="scope">
                <span v-if="scope.row.status === 1" style="color:red">停止</span>
                <span v-else-if="scope.row.status === 0" style="color:green">运行</span>
                <span v-else style="color:#FF9900">异常</span>
              </template>

            </el-table-column>
            <el-table-column
              prop="use_agent"
              label="Version"
              width="250"
            />
            <!--
            <el-table-column
              prop="version"
              label="Version"
              width="210"
            >
            </el-table-column>
            <el-table-column
              prop="time"
              label="Time"
              width="210"
            >
            </el-table-column>
            -->
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button type="text" size="small">点击行 添加服务到更新列表</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <el-pagination
        style="margin-top: 2px;"
        small
        layout="prev, pager, next, total"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="currentTotal"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />

      <p class="tip" style="font-size:13px;">请填写发布信息: </p>
      <i class="el-icon-question"
        title="填写信息中不能出现 空格 回车等空字符
  填写信息中不能使用 `!@#$&*及引号等特殊字符
  提交订单必须选择版本 并 填写更新原因
  提交订单必须选择更新服务 或 gm 或 日志
  如果内容提供人不填写 则默认为申请人
  提交前请确认好 更新的版本 和 更新的服务 !"
        ></i>
      <el-form
        ref="refsForm"
        :rules="rules"
        :model="form"
        label-position="left"
        label-width="100px"
        style="width: 100%; margin-left:20px;"
      >
        <el-row>
          <el-col :span="8">
            <el-form-item label="版本" prop="release_version">
              <el-select v-model="form.release_version" placeholder="版本" style="width:250px" filterable>
                <el-option v-for="item in VersionList" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="svn版本" prop="svn_version">
              <el-input v-model="form.svn_version" style="width:250px" maxlength="5" placeholder="" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="内容提供人" prop="contact_user">
              <el-input v-model="form.contact_user" style="width:250px" maxlength="99" placeholder="" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="原因" prop="reason">
              <el-input v-model="form.reason" type="textarea" style="width:250px" placeholder="更新原因,多个原因用分号分隔" maxlength="200"/>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="db脚本" prop="desc">
              <el-input v-model="form.desc" type="textarea" style="width:250px" placeholder="多个脚本文件以逗号分隔" maxlength="200"/>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" style="width:250px" placeholder="描述/说明" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div style="text-align:right;margin-top: 10px;margin-right: 100px">
        <el-checkbox v-model="gm_flag" class="filter-item" style="margin-right:20px; width:120px" border @change="handleShow">GM更新</el-checkbox>
        <el-checkbox v-model="log_flag" class="filter-item" style="margin-right:28px; width:120px" border @change="handleShow">Log更新</el-checkbox>
        <el-checkbox v-model="rollback_flag" class="filter-item" style="margin-right:28px; width:180px;" border @change="handleShow">本次为 回滚 更新</el-checkbox>
        <!--<el-button type="danger" @click="dialogVisible=false">-->
        <!--取消-->
        <!--</el-button>-->
        <el-button type="primary" style="width:120px" @click="confirmSetting('show')">
          提交申请
        </el-button>
      </div>
      </el-tabs>

    </el-main>

    <el-dialog :visible.sync="dialogVisible" title="提交信息核验:" :close-on-click-modal="false">
      <el-container ><el-main style="max-height:520px">
      <el-form
        ref="refsForm"
        :rules="rules"
        :model="form"
        label-position="left"
        label-width="100px"
        style="width: 100%; margin-left:3px; "
      >
      <template slot-scope="props">
        <el-row>
        <el-col :span="15" style="line-height:5px">
          <el-form-item label="版本:" style="color:blue">
            <strong>{{ form.release_version }}</strong>
          </el-form-item>
          <el-form-item v-if="form.svn_version && form.svn_version !== ''" label="svn版本号:">
            {{ form.svn_version }}
          </el-form-item>
          <el-form-item v-else label="svn版本号:">
            /
          </el-form-item>
          <el-form-item v-if="form.contact_user && form.contact_user !== ''" label="内容提供人:">
            <span>{{ form.contact_user }}</span>
          </el-form-item>
          <el-form-item v-else label="内容提供人:">
            <span>{{ name }}</span>
          </el-form-item>
        </el-col>

        <el-col :span="6" style="line-height:5px">
          <el-form-item v-if="release_flag.split(':')[0] === '0'" label="gm更新:" style="color:red">
            <strong>No</strong>
          </el-form-item>
          <el-form-item v-else label="gm更新:" style="color:green">
            <strong>Yes</strong>
          </el-form-item>
          <el-form-item v-if="release_flag.split(':')[1] === '0'" label="日志更新:" style="color:red">
           <strong>No</strong>
          </el-form-item>
          <el-form-item v-else label="日志更新:" style="color:green">
           <strong>Yes</strong>
          </el-form-item>
          <el-form-item v-if="release_flag.split(':')[2] === '0'" label="是否回滚:" style="color:red">
            <strong>No</strong>
          </el-form-item>
          <el-form-item v-else label="是否回滚:" style="color:green">
            <strong>Yes</strong>
          </el-form-item>
        </el-col> 
        </el-row>  
        <p></p>
          <el-form-item v-if="form.desc && form.desc !== ''" label="db脚本:">
            <span>{{ form.desc }}</span>
          </el-form-item>
          <el-form-item v-if="form.remark && form.remark !== ''" label="特殊说明:">
            <span>{{ form.remark }}</span>
          </el-form-item>
          <el-form-item v-if="form.reason && form.reason !== ''" label="更新原因:">
            <span style='white-space:pre-wrap'>{{ form.reason.replace(/;/g,"\n") }}</span>
          </el-form-item>

         <div style="text-align:right;margin-right:50px;" >
            <el-button type="danger" @click="dialogVisible=false">
              取消
            </el-button>
            <el-button type="primary" @click="confirmSetting('commit')">
              提交
            </el-button>
          </div>
        </template>

        </el-form>
        </el-main>

        <el-aside width="280px" style="border-left:3px solid #C0C0C0;max-height:480px">
        <div style="margin:1px;">
          <el-tree
            ref="tree"
            :data="treeData"
            :props="defaultProps"
            default-expand-all
            :expand-on-click-node="false"
            :render-content="renderDialogContent"
          />
        </div>
        </el-aside>

        </el-container>
      </el-dialog>

  </el-container>
</template>

<script>
import { getVersion, getSelectServers, getServer, getSerVersion } from '@/api/order_center/release'
import { postOrder } from '@/api/order_center/order'
import { mapGetters } from 'vuex'
const defaultOrderInfo = {
  order_type: '',
  biz_id: '',
  sub_order: {
    env: '阿里云',
    release_version: '',
    svn_version: '',
    release_flag: '',
    state: 1,
    enable: 1,
    contact_user: '',
    reason: '',
    level: 1,
    servers: '',
    server_list: '',
    remark: '',
    desc: ''
  }
}

let id = 1000
export default {
  data() {
    const treeData = [{ id: 0, name: '发布服务列表 :', children: [] }]
    return {
      settingInfo: Object.assign({}, defaultOrderInfo),
      activeTab: 'search',
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      height: {
        height: window.innerHeight - 86 + 'px'
      },
      activeName: 'first',

      tableData: [],
      currentPage: 1,
      currentTotal: 0,
      pageSize: 20,

      currentUpdatePage: 1,
      currentUpdateTotal: 0,
      pageUpdateSize: 5,
      search_update_value: '',
      order_update_value: 'division',
      app_value: '',
      server_value: [],
      division_value: '',
      order_value: 'division',
      tableColumn: { server: true, division: true },
      multipleSelection: [],

      gm_flag: false,
      log_flag: false,
      rollback_flag: false,
      release_flag: '0:0:0',
      form: {
        release_version: null,
        svn_version: null,
        contact_user: null,
        desc: null,
        reason: null,
        remark: null,
        servers: null,
        server_list: null,
        create_user: null
      },
      VersionList: [],
      SerVersionList: [],
      SelectServers: [],
      currentRow: null,
      alreadyList: [],
      alreadyServerList: [],

      dialogVisible: false,

      treeData: JSON.parse(JSON.stringify(treeData)),
      treeData: JSON.parse(JSON.stringify(treeData)),

      rules: {
        svn_version: [
          { pattern: /^[0-9]+$/, message: '请正确填写svn版本号', trigger: 'change' }
        ],
        release_version: [
          { required: true, message: '请选择发布版本', trigger: 'change' }
        ],
        reason: [
          { required: true, pattern: /^[^\s\#\@\$\!\&\*\`]*$/, message: '请填写正确格式的原因', trigger: 'change' }
        ],
        contact_user: [
          { pattern: /^[^\s\;\#\@\$\!\&\*\`]*$/, message: '请正确填写信息', trigger: 'change' }
        ],
        remark: [
          { pattern: /^[^\s]*$/, message: '请正确填写信息', trigger: 'change' }
        ],
        desc: [
          { pattern: /^([a-zA-Z0-9]+\.sh)?(,[a-zA-Z0-9\.]+\.sh)*$/, message: '请正确填写信息', trigger: 'change' }
        ]
      }

    }
  },

  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz'
    ])
  },
  created() {
    this.getVersionDatas()
    this.getSelectServersDatas()
    this.getSerVersionDatas()
  },
  mounted() {
    this.getDatas()
    window.onresize = () => {
      return (() => {
        this.height.height = window.innerHeight - 86 + 'px'
      })()
    }
  },
  methods: {
    getSelectServersDatas() {
      getSelectServers(this.currBiz).then(data => {
        this.SelectServers = data
      })
    },
    getVersionDatas() {
      getVersion(this.currBiz).then(data => {
        this.VersionList = data
      })
    },
    getSerVersionDatas() {
      getSerVersion(this.currBiz).then(data => {
        this.SerVersionList = JSON.parse(JSON.stringify(data))
      })
    },
    // 获取模板数据
    getDatas() {
      getServer({
        'biz_id': this.currBiz,
        'page': this.currentPage,
        'page_size': this.pageSize,
        'app': this.app_value,
        'server': this.server_value.join(','),
        'division': this.division_value,
        'ordering': this.order_value
      }).then(data => {
        for (const info of data.results) {
          var division_str = info['division']
          if (division_str == ''){
            info['use_agent'] = '/'
          }
          else {
            info['use_agent'] = this.SerVersionList[division_str]
          }
        }
        //console.log(data.results)
        this.currentTotal = data.count
        this.tableData = data.results
      })
    },

    // 数据显示条数改变
    handleSizeChange(val) {
      this.currentPage = 1
      this.pageSize = val
      this.getDatas()
    },

    // 当前页码改变
    handlePageChange(val) {
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
    },

    // 数据显示条数改变
    handleUpdateSizeChange(val) {
      this.currentUpdatePage = 1
      this.pageUpdateSize = val
      this.getUpdateDatas()
    },

    // 当前页码改变
    handleUpdateCurrentChange(val) {
      this.currentUpdatePage = val
      this.getUpdateDatas()
    },

    // 搜索
    searchUpdateChange() {
      this.currentUpdatePage = 1
      this.getUpdateDatas()
    },

    // tree删除
    remove(node, data) {
      const parent = node.parent
      const children = parent.data.children || parent.data
      const index = children.findIndex(d => d.id === data.id)
      children.splice(index, 1)

      if (parent.data.id != 0) {
        var remove_str = parent.data.name + '@' + data.name
        var lindex = this.alreadyList.indexOf(remove_str)
        if (lindex > -1) {
          this.alreadyList.splice(lindex, 1)
        }
      } else {
        for (const c of data.children) {
          var new_remove_str = data.name + '@' + c.name
          var newindex = this.alreadyList.indexOf(new_remove_str)
          if (newindex > -1) {
            this.alreadyList.splice(newindex, 1)
          }
        }
        var sindex = this.alreadyServerList.indexOf(data.name)
        if (sindex > -1) {
          this.alreadyServerList.splice(sindex, 1)
        }
      }

      // console.log(this.alreadyList)
      // console.log(this.alreadyServerList)
      // const b = this.alreadyServerList.filter((item, index, self) => self.indexOf(item) === index)
      // console.log(b)
    },

    renderContent(h, { node, data, store }) {
      const parent = node.parent
      if ( (node.label != '发布服务列表 :' && parent.data.children.length > 1 ) || (node.label != '发布服务列表 :' && parent.data.name == '发布服务列表 :') ) {
        return (
          <span class='custom-tree-node'>
            <span>{node.label}</span>
            <span>
              <el-button size='mini' type='text' on-click={ () => this.remove(node, data) }>Delete</el-button>
            </span>
          </span>)
      } else {
        return (
          <span class='custom-tree-node'>
            <span>{node.label}</span>
          </span>)
      }
    },

    renderDialogContent(h, { node, data, store }) {
      if (node.label != '发布服务列表 :') {
        return (
          <span class='custom-tree-node'>
            <span>{node.label}</span>
          </span>)
      } else {
        return (
          <span class='custom-tree-node'>
            <span>{node.label}</span>
          </span>)
      }
    },

    handleCurrentChange(val) {
      this.currentRow = val
      var write_info = ''
      var flag = 0
      var server_info = this.currentRow['server']
      var division_info = this.currentRow['division']
      var node_info = this.currentRow['node']
      var tree_info = this.treeData[0]['children']
      if (division_info) {
        write_info = division_info
      } else {
        write_info = node_info
      }
      var check_str = server_info + '@' + write_info
      for (const j of this.alreadyList) {
        if (j == check_str) {
          this.$message.error('该服务已存在于更新列表, 不要重复添加!')
          return
        }
      }

      for (const idata of tree_info) {
        if (idata.name == server_info) {
          const newChild = { id: id++, name: write_info, children: [] }
          if (!idata.children) {
            this.$set(idata, 'children', [])
          }
          idata.children.push(newChild)
          flag = 1
          this.alreadyList.push(check_str)
          var index = this.alreadyServerList.indexOf(server_info)
          if (index <= -1) {
            this.alreadyServerList.push(server_info)
          }
        }
      }

      if (flag == 0) {
        var pdata = this.treeData[0]
        const newCChild = { id: id++, name: write_info, children: [] }
        const newPChild = { id: id++, name: server_info, children: [newCChild] }
        if (!pdata.children) {
          this.$set(pdata, 'children', [])
        }
        pdata.children.push(newPChild)
        this.alreadyList.push(check_str)
        var index = this.alreadyServerList.indexOf(server_info)
        if (index <= -1) {
          this.alreadyServerList.push(server_info)
        }
      }
      // console.log(this.alreadyList)
      // console.log(this.alreadyServerList)
    },

    handleShow() {
      // console.log(this.gm_flag)
      // console.log(this.log_flag)
      var gm_str = ''
      var log_str = ''
      var rollback_str = ''
      if (this.gm_flag) {
        gm_str = '1'
      } else {
        gm_str = '0'
      }
      if (this.log_flag) {
        log_str = '1'
      } else {
        log_str = '0'
      }
      if (this.rollback_flag) {
        rollback_str = '1'
      } else {
        rollback_str = '0'
      }
      this.release_flag = gm_str + ':' + log_str + ':' + rollback_str
      // console.log(this.release_flag)
    },

    confirmSetting(etype) {
      if (this.form.release_version == null) {
        this.$message.error('必须选择一个发布版本 !')
        return
      }
      var is_gm = this.release_flag.split(":")[0]
      var is_log = this.release_flag.split(":")[1]
      if (this.alreadyServerList.length == 0 && is_gm == 0 && is_log == 0) {
        this.$message.error('没有添加 或 勾选 发布内容 !')
        return
      }
      if (this.alreadyServerList.length > this.alreadyList.length) {
        this.$message.error('所选更新服务和更新列表数量不匹配 !')
        console.log(this.alreadyServerList.length)
        console.log(this.alreadyList.length)
        return
      }
      this.$refs['refsForm'].validate((valid) => {
        if (valid) {
          this.settingInfo.sub_order.release_version = this.form.release_version
          this.settingInfo.sub_order.reason = this.form.reason
          this.settingInfo.sub_order.release_flag = this.release_flag
          if (this.alreadyServerList.length == 0) {
            this.settingInfo.sub_order.servers = '0'
            this.settingInfo.sub_order.server_list = '0'
          }
          else {
            this.settingInfo.sub_order.servers = this.alreadyServerList.join(';')
            this.settingInfo.sub_order.server_list = this.alreadyList.join(';')
          }

          if (this.form.remark == null || this.form.remark == '') {
            this.settingInfo.sub_order.remark = '无'
          } else {
            this.settingInfo.sub_order.remark = this.form.remark
          }
          if (this.form.desc == null || this.form.desc == '') {
            this.settingInfo.sub_order.desc = '0'
          } else {
            this.settingInfo.sub_order.desc = this.form.desc
          }
          if (this.form.contact_user == null || this.form.contact_user == '') {
            this.settingInfo.sub_order.contact_user = this.name
          } else {
            this.settingInfo.sub_order.contact_user = this.form.contact_user
          }
          if (this.form.svn_version == null || this.form.svn_version == '') {
            this.settingInfo.sub_order.svn_version = 0
          } else {
            this.settingInfo.sub_order.svn_version = this.form.svn_version
          }

          this.settingInfo.biz_id = this.currBiz
          this.settingInfo.order_type = 'release'

          if (etype == 'show'){
            this.dialogVisible = true
          }
          else{
            postOrder(this.settingInfo).then(data => {
              // console.log(data)
            })
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
                    <div>工单 : ${this.settingInfo.order_type}</div>
                  `,
              type: 'success'
            })
            this.$router.push('./order')
            console.log(this.settingInfo)
          }
        } 
        else {
          console.log('error submit!!')
          return false
        }
      })
    }

  }
}
</script>

<style scoped>
  .tip {
    padding-left: 8px;
    /*background-color: #ecf8ff;*/
    /*border-radius: 4px;*/
    border-left: 3px solid #50bfff;
    display: inline-block;
    height: 20px;
    line-height: 20px;
    /*font-weight:bold;*/
  }
</style>

<style>
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
</style>


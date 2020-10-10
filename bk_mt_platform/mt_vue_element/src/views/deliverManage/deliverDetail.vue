<template>
  <el-drawer
    title="交付详情"
    :visible.sync="drawer"
    size="55%"
  >
    <el-container style="height: 900px; border: 1px solid #eee">
      <el-header style="padding-top: 10px;padding-right: 0.25em;padding-bottom: 2ex;background: #f2f2f2;">
        <div align="left" style="float:left">
          <div style="padding-top: 15px;padding-left: 10px;font-size: 13px;color: #999;">{{ multipleSelectionCount }}
            个被选中
          </div>
        </div>
        <div v-if="admin === 0" align="right">
          <el-button-group style="padding-top: 2px;margin-right: 70px">
            <el-tooltip class="item" effect="dark" content="确认交付" placement="bottom-start">
              <el-button type="primary" icon="el-icon-success" @click="handleDeliverInfoUpdate(0)" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="取消交付" placement="bottom">
              <el-button type="primary" icon="el-icon-error" @click="handleDeliverInfoUpdate(1)" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="补单" placement="bottom">
              <el-button type="primary" icon="el-icon-upload" @click="handleDeliverInfoUpload" />
            </el-tooltip>
            <el-tooltip content="添加" class="item" effect="dark" placement="bottom">
              <el-button icon="el-icon-circle-plus" type="primary" @click="handleDeliverInfoAdd" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="编辑" placement="bottom">
              <el-button type="primary" icon="el-icon-edit" @click="handleDeliverInfoEdit" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="刷新" placement="bottom">
              <el-button type="primary" icon="el-icon-refresh" @click="handleDeliverInfoRefresh(1)" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="删除" placement="bottom">
              <el-button type="danger" icon="el-icon-delete" @click="handleDeliverInfoDel" />
            </el-tooltip>
          </el-button-group>
        </div>
        <div v-if="admin === 1" align="right">
          <el-button-group style="padding-top: 2px;">
            <!--              <el-tooltip class="item" effect="dark" content="交付作业" placement="bottom">-->
            <!--                <el-button @click="handleDeliverInfoJobs" type="primary" icon="el-icon-video-play"></el-button>-->
            <!--              </el-tooltip>-->
            <el-tooltip class="item" effect="dark" content="刷新" placement="bottom">
              <el-button type="primary" icon="el-icon-refresh" @click="handleDeliverInfoRefresh(2)" />
            </el-tooltip>
          </el-button-group>
          <el-button-group style="padding-top: 2px;margin-right: 70px">
            <el-tooltip class="item" effect="dark" content="交付作业" placement="bottom">
              <el-dropdown
                size="medium"
                split-button
                type="primary"
                @command="handleCommand"
                @click="handleDeliverInfoJobs"
              >
                <i class="el-icon-video-play el-icon--right" />
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">编辑作业</el-dropdown-item>
                  <el-dropdown-item command="b">查看实例</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-tooltip>
          </el-button-group>
        </div>
      </el-header>
      <el-container>
        <el-aside width="50%">
          <el-card shadow="hover" style="margin-left: 10px;margin-top: 20px">
            <el-table
              ref="multipleTable"
              v-loading="loading"
              size="small"
              border
              highlight-current-row
              :data="tableData"
              tooltip-effect="dark"
              style="width: 100%"
              @current-change="handleCurrentChange"
              @selection-change="handleSelectionChange"
            >
              <el-table-column
                type="selection"
              />
              <el-table-column
                label="内网IP"
              >
                <template slot-scope="scope">{{ scope.row.bk_host_innerip }}</template>
              </el-table-column>
              <el-table-column
                label="外网IP"
              >
                <template slot-scope="scope">{{ scope.row.bk_host_outerip }}</template>
              </el-table-column>
              <el-table-column
                label="国家"
              >
                <template slot-scope="scope">{{ scope.row.server_country }}</template>
              </el-table-column>
              <el-table-column
                prop="detail_flag"
                width="60"
                label="状态"
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.detail_flag=== 0" style="color: #00bb00">已交付</span>
                  <span v-if="scope.row.detail_flag=== 1" style="color: #ff4949">未交付</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              style="margin:10px 0px 0px 0px;"
              background
              :page-size.sync="pageSizeFirstSub"
              :current-page.sync="pageFirstSub"
              layout="prev, pager, next"
              :total="totalFirstSub"
              align="center"
              @current-change="handleCurrentChangeFirstSub"
            />
          </el-card>
        </el-aside>
        <el-main>
          <el-card shadow="hover">
            <el-collapse v-model="activeNames">
              <el-collapse-item title="基础信息" name="1">
                <div style="font-size:12px;">连接ip：<span class="dd-info">{{ tableDataOne.bk_host_innerip }}</span>
                </div>
                <div style="font-size:12px;">内网ip：<span class="dd-info">{{ tableDataOne.bk_host_innerip }}</span>
                </div>
                <div style="font-size:12px;">外网ip：<span class="dd-info">{{ tableDataOne.bk_host_outerip }}</span>
                </div>
                <div style="font-size:12px;">外网ip数量：<span class="dd-info">{{ tableDataOne.bk_host_outerip_2 }}</span>
                </div>
                <div style="font-size:12px;">服务器供应商：<span class="dd-info">{{ tableDataOne.isp }}</span></div>
                <div style="font-size:12px;">国家：<span class="dd-info">{{ tableDataOne.server_country }}</span></div>
                <div style="font-size:12px;">地区：<span class="dd-info">{{ tableDataOne.server_city }}</span></div>
                <div style="font-size:12px;">流量：<span class="dd-info">{{ tableDataOne.bandwidth }}</span></div>
                <div style="font-size:12px;">价格：<span class="dd-info">{{ tableDataOne.price }}</span></div>
                <div style="font-size:12px;">磁盘类型：<span class="dd-info">{{ tableDataOne.disk_type }}</span></div>
                <div style="font-size:12px;">录入时间：<span class="dd-info">{{ tableDataOne.create_time }}</span></div>
                <div style="font-size:12px;">账号：<span class="dd-info">{{ tableDataOne.sl_account }}</span></div>
                <div style="font-size:12px;">密码：<span class="dd-info">{{ tableDataOne.password }}</span></div>
              </el-collapse-item>
              <el-collapse-item title="配置信息" name="2">
                <div style="font-size:12px;">主机名称：<span class="dd-info">{{ tableDataOne.bk_host_name }}</span></div>
                <div style="font-size:12px;">操作系统类型：<span class="dd-info">{{ tableDataOne.bk_os_type }}</span></div>
                <div style="font-size:12px;">操作系统名称：<span class="dd-info">{{ tableDataOne.bk_os_name }}</span></div>
                <div style="font-size:12px;">操作系统版本：<span class="dd-info">{{ tableDataOne.bk_os_version }}</span>
                </div>
                <div style="font-size:12px;">操作系统位数：<span class="dd-info">{{ tableDataOne.bk_os_bit }}</span></div>
                <div style="font-size:12px;">cpu逻辑核心数：<span class="dd-info">{{ tableDataOne.bk_cpu }}</span></div>
                <div style="font-size:12px;">cpu频率：<span class="dd-info">{{ tableDataOne.bk_cpu_mhz }}</span></div>
                <div style="font-size:12px;">cpu型号：<span class="dd-info">{{ tableDataOne.bk_cpu_module }}</span></div>
                <div style="font-size:12px;">内存容量：<span class="dd-info">{{ tableDataOne.bk_mem }}</span></div>
                <div style="font-size:12px;">磁盘容量：<span class="dd-info">{{ tableDataOne.bk_disk }}</span></div>
                <div style="font-size:12px;">内网mac地址：<span class="dd-info">{{ tableDataOne.bk_mac }}</span></div>
                <div style="font-size:12px;">外网mac地址：<span class="dd-info">{{ tableDataOne.bk_outer_mac }}</span>
                </div>
              </el-collapse-item>
              <el-collapse-item title="备注信息" name="3">
                <div style="font-size:12px;">备注：<span class="dd-info">{{ tableDataOne.bk_comment }}</span></div>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
    <div>
      <deliver-info-drawer ref="deliverInfoDrawer" />
      <el-drawer
        size="27.7%"
        title="手动补单"
        :append-to-body="true"
        :before-close="handleClose"
        :visible.sync="uploadDrawer"
      >
        <el-container style="height: 900px; border: 1px solid #eee">
          <el-header style="padding-top: 10px;padding-right: 0.25em;padding-bottom: 2ex;background: #f2f2f2;">
            <div align="left" style="float:left">
              <div style="padding-top: 15px;padding-left: 10px;font-size: 13px;color: #999;">
                {{ multipleSelectionCount }} 个被选中
              </div>
            </div>
            <div align="right">
              <el-button-group style="padding-top: 2px;margin-right: 70px">
                <el-tooltip class="item" effect="dark" content="上传" placement="bottom">
                  <el-button type="primary" icon="el-icon-upload2" @click="submitUpload" />
                </el-tooltip>
                <el-tooltip class="item" effect="dark" content="关闭" placement="bottom">
                  <el-button type="danger" icon="el-icon-circle-close" @click="handleDeliverInfoClose" />
                </el-tooltip>
              </el-button-group>
            </div>
          </el-header>
          <el-container>
            <el-main>
              <el-card>
                <el-upload
                  ref="upload"
                  class="upload-demo"
                  drag
                  :file-list="fileList"
                  action=""
                  :auto-upload="false"
                  :before-upload="handleBeforeUpload"
                  :on-change="handleChangeFile"
                  multiple
                >
                  <i class="el-icon-upload" />
                  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                  <div slot="tip" class="el-upload__tip">
                    只能上传xlsx文件，且不超过500kb
                    <el-button size="mini" @click="handleDownloadTemplate">下载excel模板</el-button>
                  </div>

                </el-upload>
              </el-card>
            </el-main>
          </el-container>
        </el-container>
      </el-drawer>
    </div>
  </el-drawer>
</template>

<script>
import {
  deleteDeliverDetail,
  getDeliverDetailList,
  postDeliverDetailUpload,
  putDeliverDetail
} from '@/api/deliverManage'
import { runJob } from '@/base/api/task'
import DeliverInfoDrawer from '@/views/deliverManage/deliverInfoDrawer'
import { mapGetters } from 'vuex'
import { export_json_to_excel, export_table_to_excel } from '@/base/excel/export2Excel'

export default {
  name: 'DeliverDetail',
  components: { DeliverInfoDrawer },
  data() {
    return {
      multipleSelectionCount: 0,
      admin: 0,
      activeNames: ['1', '2'],
      tableDataOne: {},
      loading: false,
      multipleSelection: [{
        bandwidth: '',
        bk_comment: '',
        bk_cpu: '',
        bk_cpu_mhz: '',
        bk_cpu_module: '',
        bk_disk: '',
        bk_host_innerip: '',
        bk_host_name: '',
        bk_host_outerip: '',
        bk_host_outerip_2: '',
        bk_mac: '',
        bk_mem: '',
        bk_os_bit: '',
        bk_os_name: '',
        bk_os_type: '',
        bk_os_version: '',
        bk_outer_mac: '',
        create_time: '',
        disk_type: '',
        id: '',
        isp: '',
        order_id: '',
        password: '',
        price: '',
        server_city: '',
        server_country: '',
        sl_account: '',
        ssh_ip: ''
      }],
      drawer: false,
      infoDrawer: false,
      uploadDrawer: false,
      totalFirstSub: 0,
      tableData: [],
      pageSizeFirstSub: 10,
      pageFirstSub: 1,
      fileList: [],
      tmpId: 0,
      job_uuid: '09e629d6-44ff-46a3-95a0-19bb3ff4638d'
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  methods: {
    show(id, admin) {
      this.drawer = true
      this.admin = admin
      this.tmpId = id

      this.reloadDeliverDetailList()
    },
    reloadDeliverDetailList() {
      this.tableDataOne = {}
      this.loading = true
      getDeliverDetailList(this.pageFirstSub, this.tmpId, this.admin, this.pageSizeFirstSub).then(data => {
        this.loading = false
        this.totalFirstSub = data.count
        this.tableData = data.results
      })
    },
    handleCurrentChangeFirstSub(val) {
      this.reloadDeliverDetailList()
    },
    handleDeliverInfoUpdate(flag) {
      if (this.multipleSelectionCount === 0) {
        this.$notify({
          title: '警告哦',
          message: '请勾选你要交付完成或取消的对象',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      this.$confirm('确定交付完成或者取消' + this.multipleSelection.length + '个?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        const tmpMultipleSelection = this.multipleSelection
        this.$refs.multipleTable.clearSelection()

        for (let i = 0; i < tmpMultipleSelection.length; i++) {
          tmpMultipleSelection[i].detail_flag = flag
          putDeliverDetail(tmpMultipleSelection[i].id, tmpMultipleSelection[i])
          for (let c = 0; c < this.tableData.length; c++) {
            if (this.tableData[c].id === tmpMultipleSelection[i].id) {
              this.tableData[c].detail_flag = flag
            }
          }
        }
        this.$message({
          type: 'success',
          message: '成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },
    handleDeliverInfoEdit() {
      if (this.multipleSelectionCount === 0) {
        this.$notify({
          title: '警告',
          message: '请勾选你要编辑的对象，只能勾选一条',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      if (this.multipleSelectionCount > 1) {
        this.$notify({
          title: '错了',
          message: '你勾选了多条',
          type: 'error',
          offset: 130,
          duration: 3000
        })
        return ''
      }

      this.$refs.deliverInfoDrawer.show(this.multipleSelection[0], false)
    },
    handleDeliverInfoRefresh(flag) {
      this.pageFirstSub = 1
      this.reloadDeliverDetailList()
    },
    handleDeliverInfoDel() {
      if (this.multipleSelectionCount === 0) {
        this.$notify({
          title: '警告哦',
          message: '请勾选你要删除的对象',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      this.$confirm('确定删除' + this.multipleSelection.length + '个交付详情?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        const tmpMultipleSelection = this.multipleSelection
        this.$refs.multipleTable.clearSelection()

        for (let i = 0; i < tmpMultipleSelection.length; i++) {
          deleteDeliverDetail(tmpMultipleSelection[i].id)
          for (let c = 0; c < this.tableData.length; c++) {
            if (this.tableData[c].id === tmpMultipleSelection[i].id) {
              this.$delete(this.tableData, c)
            }
          }
        }
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },

    handleDeliverInfoClose() {
      this.infoDrawer = false
      this.uploadDrawer = false
    },
    handleClose() {
      if (this.fileList.length !== 0) {
        this.$refs.upload.clearFiles()
      }
      this.uploadDrawer = false
    },
    handleDeliverInfoUpload() {
      this.uploadDrawer = true
    },
    handleDeliverInfoAdd() {
      this.infoDrawer = true
      this.$refs.deliverInfoDrawer.show({ biz_id: this.currBiz, order: this.tmpId }, true)
    },
    handleChangeFile(file, fileList) {
      this.fileList = fileList
    },
    submitUpload() {
      this.$refs.upload.submit()
    },
    handlePreview(file) {
    },
    handleBeforeUpload(file) {
      for (let i = 0; i < this.fileList.length; i++) {
        const fileName = file.name
        let fileExt = fileName.substring(fileName.lastIndexOf('.'), fileName.length)
        fileExt = fileExt.toLowerCase()
        if (fileExt !== '.xls' && fileExt !== '.xlsx') {
          this.$notify({
            title: '错了哦',
            message: '请确认文件格式',
            type: 'error',
            offset: 130,
            duration: 3000
          })
          return false
        }
        if (file.size > 500 << 10) {
          this.$notify({
            title: '错了哦',
            message: '请确认文件大小，是否超过500KB',
            type: 'error',
            offset: 130,
            duration: 3000
          })
          return false
        }
      }
      postDeliverDetailUpload(file, this.tmpId)
        .then(data => {
          this.$message({
            type: 'success',
            message: '成功!'
          })
          this.uploadDrawer = false
          this.reloadDeliverDetailList()
        })
      return false
    },

    handleSelectionChange(val) {
      if (val.length === 0) {
        // this.multipleSelection[0] = this.tableDataOneTmp
        this.multipleSelectionCount = 0
      } else {
        this.multipleSelection = val
        this.multipleSelectionCount = this.multipleSelection.length
      }
    },

    handleCommand(command) {
      if (command === 'a') {
        this.$router.push({ path: '/task/job_module/deliver_check' })
      }
      if (command === 'b') {
        this.$router.push({ path: '/task/taskinstance_module/deliver_check' })
      }
    },
    handleDeliverInfoJobs() {
      if (this.multipleSelectionCount === 0) {
        this.$notify({
          title: '警告',
          message: '请勾选你要执行作业的对象',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      this.$confirm('确定执行作业吗', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        const tmpMultipleSelection = this.multipleSelection
        this.$refs.multipleTable.clearSelection()
        let arg = ''
        for (let i = 0; i < tmpMultipleSelection.length; i++) {
          arg = arg + ' ' + tmpMultipleSelection[i].bk_host_innerip
        }

        runJob(this.job_uuid, {
          'bk_biz': this.currBiz,
          'script_param': arg
        }).then(data => {
          this.$refs.task_details.show(data.task_instance_id)
        })
        this.$message({
          type: 'success',
          message: '成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },
    handleCurrentChange(val) {
      if (val === null) {
        this.tableDataOne = {}
      } else {
        this.tableDataOne = val
      }
    },
    handleDownloadTemplate() {
      const header = [
        'bk_host_innerip', 'bk_host_outerip', 'password', 'bk_comment', 'bk_host_outerip_2',
        'disk_type', 'server_city', 'bandwidth', 'price', 'server_country', 'sl_account',
        'ssh_ip', 'isp', 'bk_host_name', 'bk_os_type', 'bk_os_name', 'bk_os_version',
        'bk_os_bit', 'bk_cpu', 'bk_cpu_mhz', 'bk_cpu_module', 'bk_mem', 'bk_disk',
        'bk_mac', 'bk_outer_mac'
      ]
      const data = []
      const name = 'template'
      export_json_to_excel(header, data, name)
    }
  }
}
</script>

<style lang="scss" scoped>
  .el-upload-dragger {
    background-color: #fff;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    box-sizing: border-box;
    width: 450px;
    height: 180px;
    text-align: center;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
</style>


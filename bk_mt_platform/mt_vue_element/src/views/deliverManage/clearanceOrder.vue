<template>
  <div class="app-container">
    <el-tabs v-model="activeName" @tab-click="handleTagClick">
      <el-tab-pane name="first">
        <span slot="label"><i class="el-icon-s-order" /> 待清退</span>
        <el-card class="box-card">
          <data-table :load="loadClearance(1)">
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-form class="demo-table-expand" inline label-position="left">
                  <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
                    <span style="color: #B00000;font-size:12px;">{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column v-for="f in fields" :label="f.label">
              <template slot-scope="{row}">
                {{ f.formatter && f.formatter(row[f.prop]) || row[f.prop] }}
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button size="small" type="text" @click="handleClearanceInfo(scope.$index, scope.row, 1)">清退详情
                </el-button>
              </template>
            </el-table-column>
          </data-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane name="second">
        <span slot="label"><i class="el-icon-s-order" /> 待确认</span>
        <el-card class="box-card">
          <data-table :load="loadClearance(2)">
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-form class="demo-table-expand" inline label-position="left">
                  <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
                    <span style="color: #B00000;font-size:12px;">{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column v-for="f in fields" :label="f.label">
              <template slot-scope="{row}">
                {{ f.formatter && f.formatter(row[f.prop]) || row[f.prop] }}
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button size="small" type="text" @click="handleClearanceInfo(scope.$index, scope.row, 2)">清退详情
                </el-button>
              </template>
            </el-table-column>
          </data-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane name="third">
        <span slot="label"><i class="el-icon-s-order" /> 已完成</span>
        <el-card class="box-card">
          <data-table
            :load="loadClearance(0)"
          >
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-form class="demo-table-expand" inline label-position="left">
                  <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
                    <span style="color: #B00000;font-size:12px;">{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column v-for="f in fields" :label="f.label">
              <template slot-scope="{row}">
                {{ f.formatter && f.formatter(row[f.prop]) || row[f.prop] }}
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button size="small" type="text" @click="handleClearanceInfo(scope.$index, scope.row, 0)">清退详情
                </el-button>
              </template>
            </el-table-column>
          </data-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane name="fourth">
        <span slot="label"><i class="el-icon-s-order" />  清退历史记录</span>
        <el-container>
          <el-header style="height: 25px">
            <el-date-picker
              v-model="time_value"
              :default-time="['12:00:00', '08:00:00']"
              align="right"
              end-placeholder="结束日期"
              size="small"
              start-placeholder="开始日期"
              type="datetimerange"
              value-format="yyyy-MM-dd HH:mm:ss"
            />
            <el-input v-model="search_value" placeholder="请输入内容" size="small" style="width: 300px;">
              <i slot="suffix" class="el-icon-circle-close el-input__icon" @click="handleIconDel" />
            </el-input>

            <el-button
              icon="el-icon-search"
              size="small"
              style="color: white;background-color: #398ef6"
              @click="handleSearch"
            />
            <el-button
              icon="el-icon-download"
              size="small"
              style="color: white;background-color: #398ef6;"
              type="primary"
              @click="downloadExcel"
            />
          </el-header>
        </el-container>
        <el-container>
          <el-main style="width: 65%">
            <el-card class="box-card">
              <el-table
                id="el-table"
                v-loading="loading4"
                :data="tableDataFourth"
                :highlight-current-row="true"
                size="small"
                style="width: 100%"
                @current-change="handleCurrentChange"
              >
                <el-table-column label="主机ID" prop="bk_host_id" />
                <el-table-column label="清退编号" prop="remove_id" />
                <el-table-column label="内网地址" prop="bk_host_innerip" />
                <el-table-column label="外网地址" prop="bk_host_outerip" />
                <el-table-column label="国家" prop="server_country" />
                <el-table-column label="城市" prop="server_city" />
                <el-table-column label="服务器供应商" prop="isp" />
              </el-table>
            </el-card>
            <div class="block">
              <el-pagination
                :current-page.sync="pageFourth"
                :page-size.sync="pageSizeFourth"
                :page-sizes="[15, 30, 45, 60, 75, 90]"
                :total="totalFourth"
                align="center"
                background
                layout="sizes, prev, pager, next"
                style="margin:10px 0px 0px 0px;"
                @current-change="handleCurrentChangeFourth"
                @size-change="handleSizeChangeFourth"
              />
            </div>
          </el-main>
          <el-main style="width: 35%">
            <el-card>
              <host-detail :data="tableDataOne" />
            </el-card>
          </el-main>
        </el-container>
      </el-tab-pane>
    </el-tabs>

    <el-drawer
      :visible.sync="drawer"
      size="55%"
      title="清退详情"
    >
      <el-container style="height: 900px; border: 1px solid #eee">
        <el-header style="padding-top: 10px;padding-right: 0.25em;padding-bottom: 2ex;background: #f2f2f2;">
          <div align="left" style="float:left">
            <div style="padding-top: 15px;padding-left: 10px;font-size: 13px;color: #999;">{{ selection.length }}
              个被选中
            </div>
          </div>
          <div v-if="clearance_flag === 1" align="right">
            <el-button-group style="padding-top: 2px;margin-right: 70px">
              <el-tooltip class="item" content="确认" effect="dark" placement="bottom">
                <el-button icon="el-icon-success" type="primary" @click="handleClearanceInfoUpdate(2)" />
              </el-tooltip>
              <el-tooltip class="item" content="刷新" effect="dark" placement="bottom">
                <el-button icon="el-icon-refresh" type="primary" @click="handleClearanceInfoRefresh" />
              </el-tooltip>
            </el-button-group>
          </div>
          <div v-if="clearance_flag === 2" align="right">
            <el-button-group style="padding-top: 2px;margin-right: 70px">
              <el-tooltip class="item" content="确认" effect="dark" placement="bottom">
                <el-button icon="el-icon-success" type="primary" @click="handleClearanceInfoUpdate(0)" />
              </el-tooltip>
              <el-tooltip class="item" content="取消" effect="dark" placement="bottom">
                <el-button icon="el-icon-error" type="primary" @click="handleClearanceInfoUpdate(1)" />
              </el-tooltip>
              <el-tooltip class="item" content="刷新" effect="dark" placement="bottom">
                <el-button icon="el-icon-refresh" type="primary" @click="handleClearanceInfoRefresh" />
              </el-tooltip>
            </el-button-group>
          </div>
          <div v-if="clearance_flag === 0" align="right">
            <el-button-group style="padding-top: 2px;margin-right: 70px">
              <!--              <el-tooltip class="item" effect="dark" content="确认" placement="bottom">-->
              <!--                <el-button @click="handleClearanceInfoUpdate(0)" type="primary" icon="el-icon-success"></el-button>-->
              <!--              </el-tooltip>-->
              <!--              <el-tooltip class="item" effect="dark" content="取消" placement="bottom">-->
              <!--                <el-button @click="handleClearanceInfoUpdate(1)" type="primary" icon="el-icon-error"></el-button>-->
              <!--              </el-tooltip>-->
              <el-tooltip class="item" content="刷新" effect="dark" placement="bottom">
                <el-button icon="el-icon-refresh" type="primary" @click="handleClearanceInfoRefresh" />
              </el-tooltip>
            </el-button-group>
          </div>
        </el-header>
        <el-container>
          <el-aside width="50%">
            <el-card shadow="hover" style="margin-left: 10px;margin-top: 20px">
              <el-table
                ref="multipleTable"
                :data="tableData"
                border
                highlight-current-row
                size="small"
                style="width: 100%"
                tooltip-effect="dark"
                @current-change="handleCurrentChange"
                @selection-change="handleSelectionChange"
              >
                <el-table-column type="selection" />
                <el-table-column label="内网IP" prop="bk_host_innerip" />
                <el-table-column label="外网IP" prop="bk_host_outerip" />
                <el-table-column label="国家" prop="server_country" />
                <el-table-column label="状态" prop="detail_flag" width="60">
                  <template slot-scope="scope">
                    <span v-if="scope.row.clearance_flag=== 0" style="color: #00bb00">已完成</span>
                    <span v-if="scope.row.clearance_flag=== 1" style="color: #ff4949">待清退</span>
                    <span v-if="scope.row.clearance_flag=== 2" style="color: #ffce00">待确认</span>
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination
                :current-page="pageFirstSub"
                :page-size="pageSizeFirstSub"
                :total="totalFirstSub"
                align="center"
                background
                layout="prev, pager, next"
                style="margin:10px 0px 0px 0px;"
                @current-change="handleCurrentChangeFirstSub"
              />
            </el-card>
          </el-aside>
          <el-main>
            <el-card shadow="hover">
              <host-detail :data="tableDataOne" />
            </el-card>
          </el-main>
        </el-container>
      </el-container>
      <div />
    </el-drawer>
  </div>
</template>
<script>

import {
  getClearanceOrderList,
  getClearanceDetailList,
  putClearanceDetail,
  getSearchClearanceDetail
} from '@/api/deliverManage'
import { getSuborder } from '@/api/order_center/order'
import { mapGetters } from 'vuex'
import { runJob } from '@/base/api/task'
import DataTable from '../../base/components/DataTable/index'
import HostDetail from './clearance/HostDetail'

var orderState = { 0: '审批完成', 1: '待审批', 2: '审批拒绝', 3: '撤销', 4: '无效' }

export default {
  components: { HostDetail, DataTable },
  data() {
    return {
      fields: [
        { label: '工单号', prop: 'id' },
        { label: '工单类型', prop: 'order_type' },
        { label: '类型名称', prop: 'order_name' },
        { label: '提单人', prop: 'submitter' },
        { label: '提单时间', prop: 'create_time' },
        { label: '工单状态', prop: 'order_state', formatter: (s) => orderState[s] },
        { label: '当前步骤', prop: 'current_approval_step' }
      ],
      detailFields: [
        { label: '基础信息', name: '1', children: [
          { 'label': '连接ip', prop: 'bk_host_innerip' },
          { 'label': '内网ip', prop: 'bk_host_innerip' },
          { 'label': '外网ip', prop: 'bk_host_outerip' },
          { 'label': '外网ip数量', prop: 'bk_host_outerip_2' },
          { 'label': '服务器供应商', prop: 'isp' },
          { 'label': '国家', prop: 'server_country' },
          { 'label': '地区', prop: 'server_city' },
          { 'label': '流量', prop: 'bandwidth' },
          { 'label': '价格', prop: 'price' },
          { 'label': '磁盘类型', prop: 'disk_type' },
          { 'label': '录入时间', prop: 'create_time' },
          { 'label': '账号', prop: 'sl_account' },
          { 'label': '密码', prop: 'password' }
        ] },
        { label: '配置信息', name: '2', children: [
          { label: '主机名称', prop: 'bk_host_name' },
          { label: '操作系统类型', prop: 'bk_os_type' },
          { label: '操作系统名称', prop: 'bk_os_name' },
          { label: '操作系统版本', prop: 'bk_os_version' },
          { label: '操作系统位数', prop: 'bk_os_bit' },
          { label: 'cpu逻辑核心数', prop: 'bk_cpu' },
          { label: 'cpu频率', prop: 'bk_cpu_mhz' },
          { label: 'cpu型号', prop: 'bk_cpu_module' },
          { label: '内存容量', prop: 'bk_mem' },
          { label: '磁盘容量', prop: 'bk_disk' },
          { label: '内网mac地址', prop: 'bk_mac' },
          { label: '外网mac地址', prop: 'bk_outer_mac' }
        ] },
        { label: '备注信息', name: '3', children: [
          { label: '备注', prop: 'bk_comment' }
        ] }
      ],
      activeName: 'first',
      loading1: true,
      loading2: true,
      loading3: true,
      loading4: true,
      clearance_flag: 0,
      tmp: [],
      tmpRow: {},
      tableDataSecond: [],
      tableDataThird: [],
      tableDataFourth: [],
      searchFourth: 0,
      selection: [],
      pageFirst: 1,
      pageSizeFirst: 10,
      totalFirst: 0,
      pageSecond: 1,
      pageSizeSecond: 10,
      totalSecond: 0,
      pageThird: 1,
      pageSizeThird: 10,
      totalThird: 0,
      pageFourth: 1,
      pageSizeFourth: 15,
      totalFourth: 0,
      search_value: '',
      time_value: ['', ''],
      drawer: false,
      limit: 1,
      fileList: [],
      currentTotal: 0,
      tableData: [],
      tableDataOne: {},
      pageFirstSub: 1,
      pageSizeFirstSub: 15,
      totalFirstSub: 0,
      activeNames: ['1', '2'],
      activeNames1: ['1'],
      tmpId: 0,
      tmpPageFirstSub: 1,

      job_uuid: '09e629d6-44ff-46a3-95a0-19bb3ff4638d'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz'
    ])
  },
  watch: {
    'search_value': function(val) {
      if (!val) {
        this.loading4 = true
        this.pageFourth = 1

        getSearchClearanceDetail({
          'page': this.pageFourth,
          'page_size': this.pageSizeFourth,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalFourth = data.count
          this.tableDataFourth = data.results
          this.loading4 = false
        })
      }
    },
    'time_value': function(val) {
      if (!val) {
        this.loading4 = true
        this.pageFourth = 1
        this.time_value = ['', '']
        getSearchClearanceDetail({
          'page': this.pageFourth,
          'page_size': this.pageSizeFourth,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalFourth = data.count
          this.tableDataFourth = data.results
          this.loading4 = false
        })
      }
    }
  },
  methods: {
    loadClearance(type) {
      return async(options) => {
        let { count, results } = await getClearanceOrderList(options.page, this.currBiz, type)
        results = await Promise.all(results.map(async(o) => { o.suborderobj = await getSuborder(o.id); return o }))
        return { count, results }
      }
    },
    handleIconDel() {
      this.search_value = ''
    },
    handleTagClick(tab, event) {
      if (tab.index === '3') {
        this.loading4 = true
        this.pageFourth = 1
        getSearchClearanceDetail({
          'page': this.pageFourth,
          'page_size': this.pageSizeFourth,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalFourth = data.count
          this.tableDataFourth = data.results
          this.loading4 = false
        })
      }
    },
    handleCurrentChangeFirst(val) {
      getClearanceOrderList(val, this.currBiz, 1).then(data => {
        this.totalFirst = data.count
        this.tableDataFirst = data.results
        for (var i = 0; i < this.tableDataFirst.length; i++) {
          this.tableDataFirst[i].order_state = orderState[this.tableDataFirst[i].order_state]
          const tmpi = i
          getSuborder(this.tableDataFirst[i].id).then(data => {
            this.$set(this.tableDataFirst[tmpi], 'suborderobj', data)
          })
          this.tableDataFirst[i].create_time = this.tableDataFirst[i].create_time.split('.')[0].replace('T', ' ')
        }
      })
    },
    handleCurrentChangeSecond(val) {
      getClearanceOrderList(val, this.currBiz, 2).then(data => {
        this.totalSecond = data.count
        this.tableDataSecond = data.results
        for (var i = 0; i < this.tableDataSecond.length; i++) {
          this.tableDataSecond[i].order_state = orderState[this.tableDataSecond[i].order_state]
          const tmpi = i
          getSuborder(this.tableDataSecond[i].id).then(data => {
            this.$set(this.tableDataSecond[tmpi], 'suborderobj', data)
          })
          this.tableDataSecond[i].create_time = this.tableDataSecond[i].create_time.split('.')[0].replace('T', ' ')
        }
      })
    },
    handleCurrentChangeThird(val) {
      getClearanceOrderList(val, this.currBiz, 0).then(data => {
        this.totalThird = data.count
        this.tableDataThird = data.results
        for (var i = 0; i < this.tableDataThird.length; i++) {
          this.tableDataThird[i].order_state = orderState[this.tableDataThird[i].order_state]
          const tmpi = i
          getSuborder(this.tableDataThird[i].id).then(data => {
            this.$set(this.tableDataThird[tmpi], 'suborderobj', data)
          })
          this.tableDataThird[i].create_time = this.tableDataThird[i].create_time.split('.')[0].replace('T', ' ')
        }
      })
    },
    handleCurrentChangeFourth(val) {
      this.loading4 = true
      getSearchClearanceDetail({
        'page': val,
        'page_size': this.pageSizeFourth,
        'biz_id': this.currBiz,
        'search': this.search_value,
        // "ordering": this.order_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalFourth = data.count
        this.tableDataFourth = data.results
        this.loading4 = false
      })
    },
    handleSizeChangeFourth(val) {
      this.loading4 = true
      this.pageFourth = 1
      this.pageSizeFourth = val
      getSearchClearanceDetail({
        'page': this.pageFourth,
        'page_size': this.pageSizeFourth,
        'biz_id': this.currBiz,
        'search': this.search_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalFourth = data.count
        this.tableDataFourth = data.results
        this.loading4 = false
      })
    },
    handleSearch() {
      this.pageFourth = 1
      this.loading4 = true
      getSearchClearanceDetail({
        'page': this.pageFourth,
        'biz_id': this.currBiz,
        'search': this.search_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalFourth = data.count
        this.tableDataFourth = data.results
        this.loading4 = false
      })
    },
    handleClearanceInfo(index, row, flag) {
      this.tmpId = row.id
      this.clearance_flag = flag
      getClearanceDetailList(1, this.pageSizeFirstSub, row.id, this.currBiz, flag).then(data => {
        this.totalFirstSub = data.count
        this.tableData = data.results
      })
      this.drawer = true
    },
    handleCurrentChange(val) {
      if (val === null) {
        this.tableDataOne = this.tableDataOneTmp
      } else {
        this.tableDataOne = val
      }
    },
    handleSelectionChange(selection) {
      if (selection === undefined) {
        this.selection = []
      } else {
        this.selection = selection
      }
    },
    handleCurrentChangeFirstSub(val) {
      this.tmpPageFirstSub = val
      getClearanceDetailList(val, this.pageSizeFirstSub, this.tmpId, this.currBiz, this.clearance_flag).then(data => {
        this.totalFirstSub = data.count
        this.tableData = data.results
      })
    },
    handleClearanceInfoUpdate(flag) {
      if (this.selection.length === 0) {
        this.$notify({
          title: '警告',
          message: '请勾选你要待确认的对象',
          type: 'warning',
          offset: 130,
          duration: 3000
        })
        return ''
      }
      this.$confirm('确定或者取消' + this.selection.length + '个?', '警告', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(async() => {
        var tmpMultipleSelection = this.selection
        this.$refs.multipleTable.clearSelection()

        for (var i = 0; i < tmpMultipleSelection.length; i++) {
          tmpMultipleSelection[i].clearance_flag = flag
          putClearanceDetail(tmpMultipleSelection[i].id, tmpMultipleSelection[i])
          for (var c = 0; c < this.tableData.length; c++) {
            if (this.tableData[c].id === tmpMultipleSelection[i].id) {
              this.$delete(this.tableData, c)
            }
          }
        }
        getClearanceDetailList(1, this.pageSizeThird, this.tmpId, this.currBiz, this.clearance_flag).then(data => {
          if (data.count === 0) {
            if (this.clearance_flag === 0) {
              for (var c = 0; c < this.tableDataThird.length; c++) {
                if (this.tableDataThird[c].id === this.tmpId) {
                  this.$delete(this.tableDataThird, c)
                }
              }
            }
            if (this.clearance_flag === 1) {
              for (var i = 0; i < this.tableDataFirst.length; i++) {
                if (this.tableDataFirst[i].id === this.tmpId) {
                  this.$delete(this.tableDataFirst, i)
                }
              }
            }
            if (this.clearance_flag === 2) {
              for (var v = 0; v < this.tableDataSecond.length; v++) {
                if (this.tableDataSecond[v].id === this.tmpId) {
                  this.$delete(this.tableDataSecond, v)
                }
              }
            }
          }
        })
        this.$message({
          type: 'success',
          message: '成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },
    handleClearanceInfoRefresh() {
      getClearanceDetailList(this.tmpPageFirstSub, this.pageSizeFirstSub, this.tmpId, this.currBiz, this.clearance_flag).then(data => {
        this.totalFirstSub = data.count
        this.tableData = data.results
        this.$message({
          type: 'success',
          message: '成功!'
        })
        return true
      })
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
        var tmpMultipleSelection = this.multipleSelection
        this.$refs.multipleTable.clearSelection()
        var arg = ''
        for (var i = 0; i < tmpMultipleSelection.length; i++) {
          arg = arg + ' ' + tmpMultipleSelection[i].bk_host_innerip
        }

        runJob(this.job_uuid, {
          'bk_biz': this.currBiz,
          'script_param': arg
        })
        this.$message({
          type: 'success',
          message: '成功!'
        })
      }).catch(err => {
        console.error(err)
      })
    },
    downloadExcel() {
      this.$confirm('确定下载列表文件?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.excelData = this.tableDataFourth
        this.export2Excel()
      }).catch(() => {
      })
    },
    export2Excel() {
      var that = this
      require.ensure([], () => {
        const { export_json_to_excel } = require('@/base/excel/export2Excel')
        const tHeader = []
        Object.keys(this.tableDataFourth[0]).forEach(function(key) {
          tHeader.push(key)
        })
        const filterVal = tHeader
        const list = that.excelData
        const data = that.formatJson(filterVal, list)
        const time = new Date()
        export_json_to_excel(tHeader, data, `${time.getTime()}.xlsx`)
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    }
  }
}
</script>

<style>
  .demo-table-expand {
    font-size: 12px;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
    font-size: 12px;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
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
  }

  .dd-info {
    font-size: 12px;
    color: #1890ff;
  }
</style>
<style lang="scss">
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

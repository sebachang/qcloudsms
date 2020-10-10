<template>
  <div class="app-container">
    <el-tabs v-model="activeName" @tab-click="handleTagClick">
      <el-tab-pane name="first">
        <span slot="label"><i class="el-icon-s-order" /> 交付工单</span>
        <el-card class="box-card">
          <el-table
            v-loading="loading1"
            size="small"
            :data="tableDataFirst"
            style="width: 100%"
            :highlight-current-row="true"
          >
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
                    <span style="color: #B00000;font-size:12px;">{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="工单号" prop="id" />
            <el-table-column label="工单类型" prop="order_type" />
            <el-table-column label="类型名称" prop="order_name" />
            <el-table-column label="提单人" prop="submitter" />
            <el-table-column label="提单时间" prop="create_time" />
            <el-table-column label="工单状态" prop="order_state" />
            <el-table-column label="当前步骤" prop="current_approval_step" />
            <el-table-column label="交付状态">
              <template slot-scope="{row}">
                <span v-if="row.deliver_finish" style="color: green">已交付</span>
                <span v-else style="color: red">未交付</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="handleDeliverInfo(scope.$index, scope.row, 1)">交付详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        <div>
          <el-pagination
            style="margin:10px 0px 0px 0px;"
            background
            :page-size="pageSizeFirst"
            :current-page.sync="pageFirst"
            layout="prev, pager, next"
            :total="totalFirst"
            align="center"
            @current-change="handleCurrentChangeFirst"
          />
        </div>
      </el-tab-pane>

      <el-tab-pane name="second">
        <span slot="label"><i class="el-icon-s-order" /> 我的交付工单</span>
        <el-card class="box-card">
          <el-table
            v-loading="loading2"
            size="small"
            :data="tableDataSecond"
            style="width: 100%"
            :highlight-current-row="true"
          >
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item v-for="(value, key) in scope.row.suborderobj" :label="key">
                    <span style="color: #B00000;font-size:12px;">{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="工单号" prop="id" />
            <el-table-column label="工单类型" prop="order_type" />
            <el-table-column label="类型名称" prop="order_name" />
            <el-table-column label="提单人" prop="submitter" />
            <el-table-column label="提单时间" prop="create_time" />
            <el-table-column label="工单状态" prop="order_state" />
            <el-table-column label="当前步骤" prop="current_approval_step" />
            <el-table-column label="交付状态">
              <template slot-scope="{row}">
                <span v-if="row.deliver_finish" style="color: green">已交付</span>
                <span v-else style="color: red">未交付</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="handleDeliverInfo(scope.$index, scope.row, 2)">交付详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        <div>
          <el-pagination
            style="margin:10px 0px 0px 0px;"
            background
            :page-size="pageSizeSecond"
            :current-page="pageSecond"
            layout="prev, pager, next"
            :total="totalSecond"
            align="center"
            @current-change="handleCurrentChangeSecond"
          />
        </div>
      </el-tab-pane>

      <el-tab-pane name="third">
        <span slot="label"><i class="el-icon-s-order" />  交付历史记录</span>
        <el-container>
          <el-header style="height: 25px">
            <el-date-picker
              v-model="time_value"
              size="small"
              type="datetimerange"
              value-format="yyyy-MM-dd HH:mm:ss"
              align="right"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :default-time="['12:00:00', '08:00:00']"
            />
            <el-input v-model="search_value" size="small" placeholder="请输入内容" style="width: 300px;">
              <el-button
                slot="append"
                size="small"
                style="color: white;background-color: #398ef6"
                icon="el-icon-search"
                @click="handleSearch"
              />
              <el-button
                slot="append"
                size="small"
                style="color: white;background-color: #398ef6;"
                type="primary"
                icon="el-icon-download"
                @click="downloadExcel"
              />
              <i slot="suffix" class="el-icon-circle-close el-input__icon" @click="handleIconDel" />
            </el-input>
          </el-header>
        </el-container>
        <el-container>
          <el-main style="width: 65%">
            <el-card class="box-card">
              <el-table
                id="el-table"
                v-loading="loading3"
                size="small"
                :data="tableDataThird"
                style="width: 100%"
                :highlight-current-row="true"
                @current-change="handleCurrentChange"
              >
                <el-table-column prop="order" label="订单号" />
                <el-table-column prop="bk_host_innerip" label="内网地址" />
                <el-table-column prop="bk_host_outerip" label="外网地址" />
                <el-table-column prop="server_country" label="国家" />
                <el-table-column prop="server_city" label="城市" />
                <el-table-column prop="isp" label="服务器供应商" />
                <el-table-column prop="submitter" label="提单人" />
                <el-table-column prop="detail_flag" label="状态">
                  <template slot-scope="scope">
                    <span v-if="scope.row.detail_flag=== 0" style="color: #00bb00">已交付</span>
                    <span v-if="scope.row.detail_flag=== 1" style="color: #ff4949">未交付</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
            <div class="block">
              <el-pagination
                style="margin:10px 0px 0px 0px;"
                background
                :page-size.sync="pageSizeThird"
                :current-page.sync="pageThird"
                layout="sizes, prev, pager, next"
                :total="totalThird"
                :page-sizes="[15, 30, 45, 60, 75, 90]"
                align="center"
                @current-change="handleCurrentChangeThird"
                @size-change="handleSizeChangeThird"
              />
            </div>
          </el-main>
          <el-main style="width: 35%">
            <el-card>
              <el-collapse v-model="activeNames2">
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
      </el-tab-pane>

    </el-tabs>
    <deliver-detail ref="deliverDetail" />
    <TaskDetails ref="task_details" :auto-refresh="true" :refresh-interval="2000" />
  </div>
</template>
<script>

import { getDeliverOrderList, getMyDeliverOrderList, getSearchDeliverDetail } from '@/api/deliverManage'
import { getSuborder } from '@/api/order_center/order'
import { mapGetters } from 'vuex'
import TaskDetails from '@/base/views/components/TaskDetails/index'
import DeliverDetail from '@/views/deliverManage/deliverDetail'

var orderState = { 0: '审批完成', 1: '待审批', 2: '审批拒绝', 3: '撤销', 4: '无效' }

export default {
  components: { DeliverDetail, TaskDetails },
  data() {
    return {
      activeName: 'second',
      time_value: ['', ''],
      loading1: true,
      loading2: true,
      loading3: true,
      tmp: [],
      tableDataFirst: [],
      tableDataSecond: [],
      tableDataThird: [],
      pageFirst: 1,
      pageSizeFirst: 10,
      totalFirst: 0,
      pageSecond: 1,
      pageSizeSecond: 10,
      totalSecond: 0,
      pageThird: 1,
      pageSizeThird: 15,
      totalThird: 0,
      // dialogVisible: false,
      dialogVisible1: false,

      search_value: '',
      admin: 1,
      drawer: false,
      innerDrawer1: false,
      innerDrawer2: false,
      limit: 1,
      fileList: [],
      currentTotal: 0,
      tableData: [],
      tableDataOne: {},
      tableDataOneTmp: {
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
      },
      totalFirstSub: 0,
      activeNames: ['1', '2'],
      activeNames1: '',
      activeNames2: ['1'],
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
    'search_value': function (val) {
      if (!val) {
        this.loading3 = true
        this.pageThird = 1

        getSearchDeliverDetail({
          'page': this.pageThird,
          'page_size': this.pageSizeThird,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalThird = data.count
          this.tableDataThird = data.results
          this.loading3 = false
        })
      }
    },
    'time_value': function (val) {
      if (!val) {
        this.loading3 = true
        this.pageThird = 1
        this.time_value = ['', '']
        getSearchDeliverDetail({
          'page': this.pageThird,
          'page_size': this.pageSizeThird,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalThird = data.count
          this.tableDataThird = data.results
          this.loading3 = false
        })
      }
    }
  },
  created() {
    this.getOrderLists()
  },
  methods: {
    getOrderLists() {
      getMyDeliverOrderList(this.pageSecond, this.currBiz).then(data => {
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
        this.loading2 = false
      })
    },
    handleIconDel() {
      this.search_value = ''
    },
    handleTagClick(tab, event) {
      if (tab.index === '0' && this.tableDataFirst.length === 0) {
        getDeliverOrderList(this.pageFirst, this.currBiz).then(data => {
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
          this.loading1 = false
        })
      }

      if (tab.index === '2') {
        this.loading3 = true
        this.pageThird = 1
        getSearchDeliverDetail({
          'page': this.pageThird,
          'page_size': this.pageSizeThird,
          'biz_id': this.currBiz,
          'search': this.search_value,
          // "ordering": this.order_value,
          'start_time': this.time_value[0],
          'end_time': this.time_value[1]
        }).then(data => {
          this.totalThird = data.count
          this.tableDataThird = data.results
          this.loading3 = false
        })
      }
    },
    handleCurrentChangeFirst(val) {
      getDeliverOrderList(val, this.currBiz).then(data => {
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
      getMyDeliverOrderList(val, this.currBiz).then(data => {
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
      this.loading3 = true
      getSearchDeliverDetail({
        'page': val,
        'page_size': this.pageSizeThird,
        'biz_id': this.currBiz,
        'search': this.search_value,
        // "ordering": this.order_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalThird = data.count
        this.tableDataThird = data.results
        this.loading3 = false
      })
    },
    handleSizeChangeThird(val) {
      this.loading3 = true
      this.pageThird = 1
      this.pageSizeThird = val
      getSearchDeliverDetail({
        'page': this.pageThird,
        'page_size': this.pageSizeThird,
        'biz_id': this.currBiz,
        'search': this.search_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalThird = data.count
        this.tableDataThird = data.results
        this.loading3 = false
      })
    },
    handleSearch() {
      this.pageThird = 1
      this.loading3 = true
      getSearchDeliverDetail({
        'page': this.pageThird,
        'biz_id': this.currBiz,
        'search': this.search_value,
        'start_time': this.time_value[0],
        'end_time': this.time_value[1]
      }).then(data => {
        this.totalThird = data.count
        this.tableDataThird = data.results
        this.loading3 = false
      })
    },
    handleDeliverInfo(index, row, flag) {
      if (flag === 1) {
        this.admin = 0
      } else {
        this.admin = 1
      }
      // this.drawer = true
      this.$refs.deliverDetail.show(row.id, this.admin)
    },
    handleCurrentChange(val) {
      if (val === null) {
        this.tableDataOne = this.tableDataOneTmp
      } else {
        this.tableDataOne = val
      }
    },

    handleRemove(file, fileList) {
    },

    downloadExcel() {
      this.$confirm('确定下载列表文件?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.excelData = this.tableDataThird
        this.export2Excel()
      }).catch(() => {
      })
    },
    export2Excel() {
      var that = this
      require.ensure([], () => {
        const { export_json_to_excel } = require('@/base/excel/export2Excel')
        const tHeader = []
        Object.keys(this.tableDataThird[0]).forEach(function (key) {
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
    },
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

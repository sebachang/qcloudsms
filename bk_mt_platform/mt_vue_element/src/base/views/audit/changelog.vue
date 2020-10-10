<template>
  <div class="app-container">
    <el-card>
      <div class="header-box">
        <el-date-picker
          v-model="daterange"
          :picker-options="pickerOptions"
          type="daterange"
          value-format="yyyy-MM-dd"
        />
        <el-button @click="reloadLogEntries">查询历史</el-button>
      </div>
      <el-table :data="pageData" border cell-class-name="datatable-cell" header-cell-class-name="datatable-header">
        <el-table-column label="日期" prop="timestamp">
          <template slot-scope="{row}">
            {{ formatTime(row['timestamp']) }}
          </template>
        </el-table-column>
        <el-table-column label="操作者" prop="actor" />
        <el-table-column label="对象" prop="object_repr" />
        <el-table-column label="类型" prop="action">
          <template slot-scope="{row}">
            {{ translateAction(row.action) }}
          </template>
        </el-table-column>
        <el-table-column label="变更" prop="changes">
          <template slot-scope="{row}">
            <el-button icon="el-icon-view" @click="showChange(row)" />
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
    </el-card>
    <change ref="change" />
  </div>
</template>

<style>
  .old-value {
    color: darkblue;
  }

  .new-value {
    color: green;
  }
</style>

<script>
import { getChangelog } from '@/base/api/audit'
import { getDateRange } from '@/base/utils/datetime'
import { mapGetters } from 'vuex'
import Change from '@/base/views/audit/change'

const moment = require('moment')

export default {
  components: { Change },
  data() {
    return {
      log_entries: [],
      pageData: [],
      totalNum: 0,
      currentPage: 1,
      pageSize: 10,
      daterange: [],
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', getDateRange(0))
          }
        }, {
          text: '近三天',
          onClick(picker) {
            picker.$emit('pick', getDateRange(3))
          }
        }, {
          text: '近七天',
          onClick(picker) {
            picker.$emit('pick', getDateRange(7))
          }
        }, {
          text: '近一个月',
          onClick(picker) {
            picker.$emit('pick', getDateRange('1 month'))
          }
        }]
      }
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  watch: {
    log_entries() {
      this.refreshPageData()
    }
  },
  created() {
    const weekago = moment().subtract(7, 'd').format('YYYY-MM-DD')
    const now = moment().format('YYYY-MM-DD')
    this.daterange = [weekago, now]
    this.reloadLogEntries()
  },
  methods: {
    reloadLogEntries() {
      const end = moment(this.daterange[1]).add(1, 'd').format('YYYY-MM-DD')
      getChangelog(this.currBiz, this.daterange[0], end)
        .then((data) => {
          this.log_entries = data
          this.totalNum = this.log_entries.length
        })
    },
    refreshPageData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.pageData = this.log_entries.slice(start, end)
    },
    formatTime(ts) {
      return moment(ts).format('YYYY-MM-DD HH:mm:ss')
    },
    translateAction(act) {
      const text = { 'create': '创建', 'delete': '删除', 'update': '更新' }
      return text[act]
    },
    showChange(row) {
      this.$refs.change.show(row)
    }
  }
}
</script>

<style lang="scss" scoped>
  .header-box {
    background: #f2f2f2;
    padding: 7px;
  }
</style>

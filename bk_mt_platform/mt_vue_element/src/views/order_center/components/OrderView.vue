<template>
  <el-card>
    <order-table v-loading="loading" :data="tableData">
      <template slot-scope="{row}">
        <el-button type="text" @click="handleDetail(row)">详情</el-button>
        <template v-for="btn in dataProvider.operations">
          <el-button
            v-if="!btn.check || btn.check(row)"
            type="text"
            @click="btn.click(row)"
            :style="btn.style"
          >{{ btn.name }}
          </el-button>
        </template>
      </template>
    </order-table>
    <div>
      <el-pagination
        style="margin:10px 0px 0px 0px;"
        layout="prev, pager, next"
        background
        :current-page.sync="currentPage"
        :page-size="pageSize"
        :total="totalNum"
        align="center"
        @current-change="handlePageChange"
      />
    </div>
  </el-card>
</template>

<script>
import OrderTable from '@/views/order_center/components/OrderTable'
import { getSuborder } from '@/api/order_center/order'

export default {
  name: 'OrderView',
  components: { OrderTable },
  props: {
    dataProvider: {
      type: Object,
      default: Object
    }
  },
  data() {
    return {
      currentPage: 1,
      totalNum: 0,
      pageSize: 10,
      loading: false,
      tableData: []
    }
  },
  watch: {
    dataProvider() {
      this.currentPage = 1
      this.reload()
    }
  },
  created() {
    this.reload()
  },
  methods: {
    reload() {
      if (this.dataProvider.load === undefined) {
        return
      }
      this.loading = true
      this.dataProvider.load(this.currentPage, (data) => {
        this.totalNum = data.count
        this.tableData = data.results
        for (var i = 0; i < this.tableData.length; i++) {
          const tmpi = i
          getSuborder(this.tableData[i].id).then(data => {
            Object.keys(data).forEach(function(key) {
              data[key].replace(/;;/gm, '<br/>')
            })
            this.$set(this.tableData[tmpi], 'suborderobj', data)
          })
          this.tableData[i].create_time = this.tableData[i].create_time.split('.')[0].replace('T', ' ')
        }
        this.loading = false
      })
    },
    handlePageChange(val) {
      this.reload()
    },
    handleDetail(row) {
      this.$emit('detail', row)
    }
  }
}
</script>

<style scoped>

</style>

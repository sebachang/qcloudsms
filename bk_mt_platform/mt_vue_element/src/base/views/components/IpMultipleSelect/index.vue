<template>
  <div>
    <div class="table-head-container">
      <div align="left" style="float:left">
        <el-button
          icon="el-icon-circle-plus-outline"
          size="mini"
          type="primary"
          plain
          @click="handleAddHost"
        >
          添加主机
        </el-button>
      </div>
      <div align="right" class="right-menu">
        <el-input
          v-model="searchHost"
          size="mini"
          placeholder="输入关键字搜索"
        />
      </div>
    </div>
    <el-table
      border
      :data="hostTableData"
      style="width: 100%"
      :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
      :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
    >
      <el-table-column
        prop="bk_cloud_id"
        label="区域ID"
        width="180"
      />
      <el-table-column
        prop="ip"
        label="IP地址"
      />
      <el-table-column label="操作" width="160">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            plain
            @click="handleHostDelete(scope)"
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
        :current-page="currentHostPage"
        :page-sizes="[5]"
        :page-size="pageHostSize"
        :total="currentHostTotal"
        @current-change="handleHostCurrentChange"
      />
      <IpSelect ref="ip_select" append-to-body="true" @pick="handlePickIp" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'
import IpSelect from '@/base/views/components/IpSelect/index'

export default {
  name: 'IpMultipleSelect',
  props: {
    hosts: {
      hosts: Object,
      default: function() {
        return []
      }
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  components: { IpSelect },
  data() {
    return {
      hostTableData: [],
      currentHostPage: 1,
      pageHostSize: 5,
      currentHostTotal: 0,

      searchHost: ''
    }
  },
  watch: {
    // 监听搜索改变
    searchHost(curVal, oldVal) {
      // 实现input连续输入，只发一次请求
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.searchHostChange()
      }, 300)
    }
  },
  mounted: function() {
    this.searchHost = ''
    this.searchHostChange()
  },
  methods: {
    searchHostChange(val = 1) {
      let cache = []
      if (this.searchHost !== '') {
        for (const value of this.hosts) {
          var reg = RegExp(this.searchHost)
          if (value.ip.match(reg)) {
            cache.push(value)
          }
        }
      } else {
        cache = this.hosts
      }

      this.hostTableData = cache
      this.currentHostTotal = this.hostTableData.length
      this.currentHostPage = val

      if (this.pageHostSize * this.currentHostPage >= this.currentHostTotal) {
        this.hostTableData = this.hostTableData.slice((this.currentHostPage - 1) * this.pageHostSize, this.currentHostTotal)
      } else {
        this.hostTableData = this.hostTableData.slice((this.currentHostPage - 1) * this.pageHostSize, this.pageHostSize * this.currentHostPage)
      }
    },

    handleHostCurrentChange(val) {
      this.searchHostChange(val)
    },

    // 删除主机
    handleHostDelete({ $index, row }) {
      const obj = this.hosts.find(c => c.bk_cloud_id === row.bk_cloud_id && c.ip === row.ip)
      let dl_index = null

      this.hosts.find(function(value, index) {
        if (value.bk_cloud_id === row.bk_cloud_id && value.ip === row.ip) {
          dl_index = index
        }
      })

      this.hosts.splice(dl_index, 1)
      this.$emit('update', this.hosts)
      if (this.currentHostPage > 1 && this.hostTableData.length >= 2) {
        this.searchHostChange(this.currentHostPage)
      } else if (this.currentHostPage > 1 && this.hostTableData.length === 1) {
        this.searchHostChange(this.currentHostPage - 1)
      } else {
        this.searchHostChange()
      }
    },

    handleAddHost() {
      this.$refs.ip_select.show()
    },

    SetHosts(arr) {
      for (const t of arr) {
        // 检查缓存中是否已经存在
        if (this.hosts.find(c => c.bk_cloud_id === t.bk_cloud_id && c.ip === t.ip)) {
          // 已经存在说明以前记录过，现在这个就是多余的，直接忽略
          continue
        }
        // 不存在就说明以前没遇到过，把它记录下来
        this.hosts.push(t)
      }
      this.$emit('update', this.hosts)
    },

    handlePickIp(ip) {
      this.SetHosts(ip)
      this.searchHostChange()
    }

  }
}
</script>

<style lang="scss" scoped>
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
</style>

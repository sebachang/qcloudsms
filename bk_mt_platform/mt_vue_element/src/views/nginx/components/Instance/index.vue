<template>
  <div>
    <div class="table-head-container">
      <div align="left" style="float:left">
        <el-dropdown size="mini">
          <el-button type="primary" size="mini" :disabled="multipleButton">
            批量操作<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item icon="el-icon-video-play" @click.native="addInstanceOperator('start')">启动
            </el-dropdown-item>
            <el-dropdown-item icon="el-icon-refresh" @click.native="addInstanceOperator('reload')">重载</el-dropdown-item>
            <el-dropdown-item icon="el-icon-switch-button" @click.native="addInstanceOperator('stop')">停止
            </el-dropdown-item>
            <el-dropdown-item icon="el-icon-s-help" @click.native="addInstanceOperator('restart')">重启</el-dropdown-item>
            <el-dropdown-item icon="el-icon-s-promotion" @click.native="addInstanceOperator('publish')">发布
            </el-dropdown-item>
            <el-dropdown-item icon="el-icon-edit-outline" @click.native="addInstanceOperator('pull_config')">下发配置
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{ currentHostTotal }}个中
          {{ multipleSelectionCount }} 个被选中</p>
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
      @selection-change="handleSelectionChange"
      style="width: 100%"
      :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
      :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
    >
      <el-table-column type="selection" width="48"/>
      <el-table-column
        prop="bk_cloud_id"
        label="区域ID"
        width="80"
      />
      <el-table-column
        prop="ip"
        label="IP地址"
        width="180"
      />
      <el-table-column
        prop="status"
        label="状态"
      >
        <InstanceStatus slot-scope="{row}" :data="row.status"/>
      </el-table-column>
      <el-table-column label="操作" width="60">
        <template slot-scope="scope">
          <el-dropdown size="mini">
            <span class="el-dropdown-link">
              <i class="el-icon-more el-icon--right" style="transform: rotate(90deg);"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-video-play" @click.native="addInstanceOperatorRow(scope,'start')">启动
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-refresh" @click.native="addInstanceOperatorRow(scope,'reload')">重载
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-switch-button" @click.native="addInstanceOperatorRow(scope,'stop')">停止
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-s-help" @click.native="addInstanceOperatorRow(scope,'restart')">重启
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-s-promotion" @click.native="addInstanceOperatorRow(scope,'publish')">发布
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-edit-outline" @click.native="addInstanceOperatorRow(scope,'pull_config')">
                下发配置
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-attract"
                                @click.native="addInstanceOperatorRow(scope,'pull_config_restart')">下发并重启
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-paperclip"
                                @click.native="addInstanceOperatorRow(scope,'pull_config_reload')">下发并重载
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
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
    </div>
  </div>
</template>

<script>
  import InstanceStatus from '@/views/processManage/components/InstanceStatus'
  import {mapGetters} from 'vuex'
  import {
    addOperator,
  } from '@/api/nginx'

  export default {
    name: "Instance",
    components: {InstanceStatus},
    computed: {
      ...mapGetters([
        'name',
        'role',
        'currBiz'
      ])
    },
    props: {
      config: {
        type: Number,
        default: 0,
      },
      config_name: {
        type: String,
        default: '',
      },
      hosts: {
        type: Object,
        default: function () {
          return []
        }
      }
    },
    data() {
      return {
        hostTableData: [],
        currentHostPage: 1,
        pageHostSize: 5,
        currentHostTotal: 0,

        searchHost: '',
        multipleSelection: [],
        multipleSelectionCount: 0,

        multipleButton: true,
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
      },

      multipleSelectionCount() {
        if (this.multipleSelectionCount > 0) {
          this.multipleButton = false
        } else {
          this.multipleButton = true
        }
      },

      hosts() {
        this.searchHostChange()
      }
    },
    mounted: function () {
      this.searchHost = ''
      this.searchHostChange()
    },
    methods: {
      // 手动刷新
      handleRefresh() {
        // this.searchHostChange()
        this.$forceUpdate()
      },

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

      // 多选
      handleSelectionChange(val) {
        this.multipleSelection = val
        this.multipleSelectionCount = this.multipleSelection.length
      },


      // 删除主机
      handleHostDelete({$index, row}) {
        const obj = this.hosts.find(c => c.bk_cloud_id === row.bk_cloud_id && c.ip === row.ip)
        let dl_index = null

        this.hosts.find(function (value, index) {
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
      },

      addInstanceOperator(action) {
        addOperator(this.config, {'action': action, 'hosts': this.multipleSelection}).then(data => {
          this.$emit('callback');

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>${action}: ${this.config_name}</div>
          `,
            type: 'success'
          })
        })
      },

      addInstanceOperatorRow(scop, action) {
        var hosts = [{'bk_cloud_id': scop.row.bk_cloud_id, 'ip': scop.row.ip}]
        addOperator(this.config, {'action': action, 'hosts': hosts}).then(data => {
          this.$emit('callback');

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>${action}: ${this.config_name}</div>
          `,
            type: 'success'
          })
        })
      },

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

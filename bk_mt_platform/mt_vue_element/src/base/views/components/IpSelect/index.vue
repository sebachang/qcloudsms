<template>
  <el-dialog
    :append-to-body="appendToBody"
    :close-on-click-modal="false"
    :visible.sync="visible"
    title="选择服务器"
    @open="handleOpen()"
  >
    <el-tabs v-model="currentTab">
      <el-tab-pane label="通过IP选择" name="ip">
        <div class="datatable-head-container" style="margin: 0">
          <el-button plain size="mini" @click="selectAll">跨页全选</el-button>
          <el-button plain size="mini" @click="clearSelection">取消选择</el-button>
          总共 {{ totalNum }} 个服务器，已选择 {{ selection.length }}
          <search-box v-model="search" style="float: right" @enter="handleSearch" />
        </div>
        <el-table
          ref="table"
          v-loading="loading"
          :data="ipList"
          border
          header-cell-class-name="datatable-header"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column label="主机名" prop="host.bk_host_name" />
          <el-table-column label="内网IP" prop="host.bk_host_innerip" />
          <el-table-column label="外网IP" prop="host.bk_host_outerip" />
          <el-table-column label="云区域" prop="host.bk_cloud_id[0].bk_inst_name" />
        </el-table>
        <el-pagination
          :current-page.sync="currentPage"
          :page-size.sync="pageSize"
          :page-sizes="[2, 10, 20, 30, 40, 50, 100]"
          :total="totalNum"
          background
          layout="prev, pager, next, sizes, total, jumper"
        />
      </el-tab-pane>
      <el-tab-pane label="配置平台" lazy name="topo">
        <el-tree
          ref="topoTree"
          :default-expanded-keys="defaultExpandKeys"
          :load="loadNode"
          :props=" { children: 'child', label: 'bk_inst_name' }"
          lazy
          node-key="bk_inst_id"
          show-checkbox
        />
      </el-tab-pane>
      <el-tab-pane label="手动添加" lazy name="input">
        云区域名称:
        <el-select v-model="bk_cloud_id">
          <el-option v-for="c in bk_clouds" :key="c.bk_inst_id" :label="c.bk_inst_name" :value="c.bk_inst_id" />
        </el-select>
        <el-input v-model="ipStr" placeholder="请填写IP，每行一个" type="textarea" />
      </el-tab-pane>
    </el-tabs>
    <div style="padding: 10px 0 0 10px">
      <el-button type="primary" @click="handleSubmit">确定</el-button>
      <el-button type="danger" @click="visible=false">取消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { mapGetters } from 'vuex'
import { searchBizInstTopo, searchHost, searchHost2 } from '@/base/api/cmdb'
import SearchBox from '@/base/components/SearchBox/index'

export default {
  name: 'IpSelect',
  components: { SearchBox },
  props: {
    bizId: {
      type: Number,
      default: 0
    },
    appendToBody: {
      type: Boolean,
      default: false
    },
    limit: {
      type: Number,
      default: -1
    }
  },
  computed: {
    ...mapGetters(['currBiz']),
    pageStart() {
      return (this.currentPage - 1) * this.pageSize
    }
  },
  watch: {
    ipList() {
      this.buildCloud()
    },
    pageSize() {
      if (this.currentPage === 1) {
        this.loadIPList()
      } else {
        this.currentPage = 1
      }
    },
    currentPage() {
      this.loadIPList()
    }
  },
  created() {
    searchBizInstTopo(this.currBiz)
      .then((d) => {
        this.defaultExpandKeys = []
        let nodes = [].concat(d)
        while (nodes.length > 0) {
          const node = nodes[0]
          nodes = nodes.slice(1)
          this.defaultExpandKeys.push(node.bk_inst_id)
          if (node.child && node.bk_obj_id !== 'app') {
            nodes = nodes.concat(node.child)
          }
        }
        console.log(d, this.defaultExpandKeys)
      })
  },
  data() {
    return {
      loading: true,
      visible: false,
      ipStr: '',
      ipList: [],
      selection: [],
      currentTab: 'ip',
      currentPage: 1,
      totalNum: 0,
      pageSize: 10,
      bk_clouds: [],
      bk_cloud_id: -1,
      search: '',
      currentSearch: '',
      defaultExpandKeys: []
    }
  },
  methods: {
    show() {
      this.visible = true
    },
    handleOpen() {
      this.loadIPList()
    },
    loadIPList() {
      searchHost(this.currBiz, {
        ip: this.currentSearch,
        pageSize: this.pageSize,
        pageStart: this.pageStart
      })
        .then((data) => {
          this.loading = false
          this.totalNum = data.count
          this.ipList = data.info
        })
    },
    buildCloud() {
      var clouds = []
      clouds.push({ 'bk_inst_name': '自动', 'bk_inst_id': -1 })
      for (var i = 0; i < this.ipList.length; ++i) {
        const host = this.ipList[i]
        const cloud = host['host']['bk_cloud_id'][0]
        const currentCloud = clouds.find((c) => c.bk_inst_id === cloud.bk_inst_id)
        if (currentCloud === undefined) {
          clouds.push(cloud)
        }
      }
      this.bk_clouds = clouds
    },
    handleSelectionChange(selection) {
      this.selection = selection
    },
    getSelection(callback) {
      let hosts = []
      switch (this.currentTab) {
        case 'ip':
          hosts = this.selection
          callback(hosts)
          return
        case 'topo':
          var nodes = this.$refs.topoTree.getCheckedNodes()
          var modules = new Set()
          while (nodes.length > 0) {
            var node = nodes.shift()
            if (node.bk_obj_id === 'module') {
              modules.add(node.bk_inst_id)
            }
            nodes = nodes.concat(node.child)
          }
          searchHost2(this.currBiz, {
            condition: [{
              'bk_obj_id': 'module',
              condition: [{
                'field': 'bk_module_id',
                'operator': '$in',
                'value': Array.from(modules)
              }]
            }]
          }).then(d => {
            var hostSet = new Set()
            hosts = this.$refs.topoTree.getCheckedNodes().filter((n) => n['is_host'] === true)
            hosts.forEach(o => {
              hostSet.add(o.host.bk_cloud_id[0].id + ':' + o.host.bk_host_innerip)
            })
            d.info.forEach(o => {
              if (!hostSet.has(o.host.bk_cloud_id[0].id + ':' + o.host.bk_host_innerip)) {
                hosts.push(o)
              }
            })
            callback(hosts)
          })
          return
        case 'input':
          const ips = this.ipStr.trim().split('\n')
          searchHost2(this.currBiz, {
            'ip': {
              'data': ips,
              'exact': 1,
              'flag': 'bk_host_innerip|bk_host_outerip'
            },
            condition: [{
              'bk_obj_id': 'biz',
              condition: [{
                'field': 'bk_biz_id',
                'operator': '$eq',
                'value': parseInt(this.currBiz)
              }]
            }]
          }).then(d => {
            var allIps = new Set()
            var dupIps = []
            var missIps = []

            var addIp = function(ip) {
              if (allIps.has(ip)) {
                dupIps.push(ip)
              } else {
                allIps.add(ip)
              }
            }
            var checkExists = function(ip) {
              if (!allIps.has(ip)) {
                missIps.push(ip)
              }
            }
            var resIps = d.info.map(o => {
              if (o.host.bk_host_innerip !== '') {
                addIp(o.host.bk_host_innerip)
              }
              if (o.host.bk_host_outerip !== '') {
                addIp(o.host.bk_host_outerip)
              }
            })
            ips.forEach(i => checkExists(i))

            if (dupIps.length > 0 || missIps.length > 0) {
              let error = ''
              if (dupIps.length > 0) {
                error += `重复的IP: ${dupIps.join(',')}\n`
              }
              if (missIps.length > 0) {
                error += `未找到的IP: ${missIps.join(',')}\n`
              }
              this.$message.error(error)
            } else {
              callback(d.info)
            }
          })
          return
      }
    },
    handleSubmit() {
      this.getSelection(selection => {
        if (selection !== undefined) {
          if (this.limit > 0) {
            if (selection.length > this.limit) {
              this.$message({ message: `最多选择${this.limit}个IP, 请重新输入`, type: 'error' })
              return undefined
            }
          }

          this.$emit('pickDetail', selection)
          const hosts = selection.map((h) => {
            return {
              'bk_cloud_id': h.host.bk_cloud_id[0].bk_inst_id,
              'ip': h.host.bk_host_innerip
            }
          })
          this.$emit('pick', hosts)
          this.visible = false
        }
      })
    },
    selectAll() {
      this.loading = true
      this.$refs.table.clearSelection()
      this.$refs.table.toggleAllSelection()
      searchHost(this.currBiz, {
        ip: this.currentSearch,
        pageSize: 0,
        pageStart: 0
      })
        .then((d) => {
          this.loading = false
          this.selection = d.info
        })
    },
    clearSelection() {
      this.$refs.table.clearSelection()
    },
    handleSearch() {
      this.currentSearch = this.search
      this.loadIPList()
    },
    loadNode(node, resolve) {
      if (node.data === undefined) {
        searchBizInstTopo(this.currBiz)
          .then((d) => {
            resolve(d)
          })
      } else if (node.data.isLeaf) {
        resolve([])
      } else if (node.data.bk_obj_id !== 'module') {
        resolve(node.data.child)
      } else {
        searchHost(this.currBiz, {
          'condition': [{
            'bk_obj_id': 'module',
            'condition': [{
              field: 'bk_module_id',
              operator: '$eq',
              value: node.data.bk_module_id
            }]
          }]
        }).then(d => resolve(d.info.map(o => ({
          bk_inst_name: `${o.host.bk_host_name}[${o.host.bk_host_innerip}]`,
          is_host: true,
          isLeaf: true,
          ...o
        }))))
      }
    }
  }
}
</script>

<style scoped>

</style>

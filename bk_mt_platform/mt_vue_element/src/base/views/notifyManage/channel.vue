<template>
  <div class="app-container">
    <el-card>
      <div class="datatable-head-container">
        <el-button icon="el-icon-circle-plus-outline" size="mini" type="primary" plain @click="handleCreate">添加通道</el-button>
        <div style="float:right">
          <el-button icon="el-icon-refresh" style="background: none; border: none" circle @click="reloadData" />
        </div>
      </div>
      <el-table v-loading="loading" :data="channels" header-cell-class-name="datatable-header" cell-class-name="datatable-cell" border>
        <el-table-column label="名称" prop="name" />
        <el-table-column label="类型" prop="type" />
        <el-table-column label="是否启用" prop="enabled" :formatter="enabledFormatter" />
        <el-table-column label="操作">
          <template slot-scope="{row}">
            <el-button size="mini" type="primary" plain @click="showModifyDialog(row)">编辑</el-button>
            <popconfirm text="确定要删除吗？" @confirm="handleDelete(row.id)">
              <el-button slot="reference" size="mini" type="danger" plain>删除</el-button>
            </popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <channel-detail-dialog ref="channelDetailDialog" @confirm="reloadData" />
  </div>
</template>

<script>
import ChannelDetailDialog from '@/base/views/notifyManage/components/ChannelDetailDialog'
import { deleteChannel, getChannels } from '@/base/api/notifyManage'
import { mapGetters } from 'vuex'
import Popconfirm from '@/base/views/components/Popconfirm/index'

export default {
  name: 'NotifyChannel',
  components: { Popconfirm, ChannelDetailDialog },
  data() {
    return {
      channels: [],
      loading: false
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  created() {
    this.reloadData()
  },
  methods: {
    reloadData() {
      this.loading = true
      getChannels(this.currBiz)
        .then(data => {
          this.loading = false
          this.channels = data
        })
    },
    enabledFormatter(row, column) {
      return row.enabled ? '是' : '否'
    },
    handleCreate() {
      this.$refs.channelDetailDialog.show()
    },
    handleDelete(id) {
      deleteChannel(this.currBiz, id)
        .then(() => {
          this.reloadData()
        })
    },
    showModifyDialog(row) {
      this.$refs.channelDetailDialog.show(row)
    }
  }
}
</script>

<style scoped>

</style>

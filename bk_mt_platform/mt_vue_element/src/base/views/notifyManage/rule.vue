<template>
  <div class="app-container">
    <el-card>
      <div class="datatable-head-container">
        <el-button icon="el-icon-circle-plus-outline" type="primary" size="mini" plain @click="handleCreate">添加规则
        </el-button>
        <div style="float:right">
          <el-button icon="el-icon-refresh" style="background: none; border: none" circle @click="reloadData" />
        </div>
      </div>
      <el-table
        v-loading="loading"
        :data="rules"
        header-cell-class-name="datatable-header"
        cell-class-name="datatable-cell"
        border
      >
        <el-table-column label="名称" prop="name" />
        <el-table-column label="tags">
          <template slot-scope="{row}">
            <el-tag v-for="t in row.tags" :key="t">{{ getTagName(t) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="消息类型">
          <template slot-scope="{row}">
            <el-tag v-for="t in row.types" :key="t">{{ getTypeName(t) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="通道">
          <template slot-scope="{row}">
            <el-tag v-for="c in row.dest_name" :key="c">{{ c }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="{row}">
            <el-button size="mini" type="primary" plain @click="showModifyDialog(row)">编辑</el-button>
            <popconfirm text="确定删除吗？" @confirm="handleDelete(row.id)">
              <el-button slot="reference" size="mini" type="danger" plain>删除</el-button>
            </popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <rule-detail-dialog ref="ruleDetailDialog" @confirm="reloadData" />
  </div>
</template>

<script>
import RuleDetailDialog from '@/base/views/notifyManage/components/RuleDetailDialog'
import { deleteRule, getRules, getTags } from '@/base/api/notifyManage'
import { mapGetters } from 'vuex'
import Popconfirm from '@/base/views/components/Popconfirm/index'

export default {
  name: 'NotifyRule',
  components: { Popconfirm, RuleDetailDialog },
  data() {
    return {
      loading: false,
      rules: [],
      types: [{
        name: '通知',
        id: 1
      }, {
        name: '警告',
        id: 2
      }],
      tags: []
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  created() {
    this.reloadData()
  },
  methods: {
    getTypeName(t) {
      const res = this.types.find(o => o.id === t)
      return res === undefined ? '' : res.name
    },
    getTagName(t) {
      const res = this.tags.find(o => o.key === t)
      return res === undefined ? '' : res.name
    },
    handleCreate() {
      this.$refs.ruleDetailDialog.show()
    },
    reloadData() {
      this.loading = true
      getRules(this.currBiz)
        .then((data) => {
          this.loading = false
          this.rules = data
        })
      getTags(this.currBiz)
        .then((data) => {
          this.tags = data
        })
    },
    showModifyDialog(row) {
      this.$refs.ruleDetailDialog.show(row)
    },
    handleDelete(id) {
      deleteRule(this.currBiz, id)
        .then(() => {
          this.reloadData()
        })
    }
  }
}
</script>

<style scoped>

</style>

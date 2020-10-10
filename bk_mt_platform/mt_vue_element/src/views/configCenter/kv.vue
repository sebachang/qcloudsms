<template>
  <div class="app-container">
    <el-card>
      <div class="clearfix datatable-head-container">
        <el-button
          icon="el-icon-circle-plus-outline"
          plain
          size="mini"
          type="primary"
          @click="showCreateForm()"
        >
          创建配置项
        </el-button>
        <span style="float: right">
          <search-box v-model="search" />
        </span>
      </div>
      <el-table
        :data="pageData"
        border
        cell-class-name="datatable-cell"
        class="grid-content"
        header-cell-class-name="datatable-header"
      >
        <el-table-column label="键名" prop="key" />
        <el-table-column label="配置值" prop="value">
          <span slot-scope="{row}">
            <el-row v-if="row.edit">
              <el-col :span="20">
                <el-input v-model="row.value" size="mini" placeholder="配置值" />
              </el-col>
              <el-col :span="4">
                <el-button plain size="mini" type="warning" @click="handleCancel(row)">取消</el-button>
              </el-col>
            </el-row>
            <span v-else>{{ row.value }}</span>
          </span>
        </el-table-column>
        <el-table-column label="操作">
          <span slot-scope="{row}">
            <el-button v-if="!row.edit" plain size="mini" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-else plain size="mini" type="success" :disabled="row.value === row.oldValue" @click="updateKV(row)">保存</el-button>
            <el-button plain size="mini" type="danger" @click="remove(row)">删除</el-button>
          </span>
        </el-table-column>
      </el-table>
      <div
        style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid"
      >
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
      </div>
      <el-dialog :close-on-click-modal="false" :title="create ? '创建' : '编辑'" :visible.sync="visible">
        <el-form>
          <el-form-item label="键名">
            <el-input v-model="form.key" />
          </el-form-item>
          <el-form-item label="配置值">
            <el-input v-model="form.value" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveForm()">保存</el-button>
            <el-button type="danger" @click="visible=false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import { addConfigKV, deleteConfigKV, getConfigKV, updateConfigKV } from '@/api/configCenter'
import { mapGetters } from 'vuex'
import SearchBox from '@/base/components/SearchBox/index'

export default {
  components: { SearchBox },
  data() {
    return {
      kv: [],
      tableData: [],
      pageData: [],
      create: true,
      visible: false,
      show: false,
      form: {},
      search: '',
      currentPage: 1,
      pageSize: 10,
      totalNum: 0
    }
  },
  computed: {
    ...mapGetters([
      'currBiz'
    ]),
    routesData() {
      return this.routes
    }
  },
  watch: {
    search() {
      this.refreshTableData()
    }
  },
  created() {
    this.reloadKV()
  },
  methods: {
    refreshTableData() {
      this.tableData = this.kv.filter((kv) => kv.key.includes(this.search) || kv.value.includes(this.search))
      this.totalNum = this.tableData.length
      this.refreshPageData()
    },
    refreshPageData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.pageData = this.tableData.slice(start, end)
    },
    reloadKV() {
      getConfigKV(this.currBiz)
        .then((data) => {
          this.kv = data.map(o => (o.edit = false, o))
          this.refreshTableData()
        })
    },
    showCreateForm() {
      this.create = true
      this.visible = true
      this.form = {}
    },
    saveForm() {
      var data = this.form
      data.biz_id = this.currBiz
      addConfigKV(data)
        .then(() => {
          this.visible = false
          this.reloadKV()
        })
    },
    updateKV(row) {
      updateConfigKV(this.currBiz, row.id, row)
        .then(() => {
          this.$message({ message: '更新成功', type: 'success' })
          this.reloadKV()
        })
    },
    remove(row) {
      this.$confirm(`确定要删除${row.key}吗？`)
        .then(() => {
          deleteConfigKV(this.currBiz, row.id)
            .then(() => {
              this.reloadKV()
            })
        })
    },
    handleEdit(row) {
      row.edit = true
      row.oldValue = row.value
    },
    handleCancel(row) {
      row.edit = false
      row.value = row.oldValue
    }
  }
}
</script>

<style lang="scss" scoped>
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }

</style>

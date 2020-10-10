<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">
        <div class="table-head-container">
          <div align="left" style="float:left">
            <el-button icon="el-icon-circle-plus-outline" size="mini" type="primary" plain @click="handleAdd">
              添加
            </el-button>
            <el-button icon="el-icon-delete" size="mini" type="danger" plain @click="handleMultipleDelete">删除
            </el-button>
            <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{ currentTotal }}个中
              {{ multipleSelectionCount }} 个被选中</p>
          </div>
          <div align="right" class="right-menu">
            <div :class="{'show':show}" class="header-search">
              <svg-icon class-name="search-icon" icon-class="search" @click.stop="click" />
              <el-input
                ref="headerSearchSelect"
                v-model="search_value"
                placeholder="搜索"
                class="header-search-select"
              />
            </div>
            <el-button icon="el-icon-refresh" class="header-refresh" circle @click="handleRefresh" />
            <el-dropdown :hide-on-click="false" style="bottom: 5px">
              <el-button
                icon="el-icon-more-outline"
                style="transform: rotate(90deg);background: transparent;border-style: none; outline: none; font-size: 18px;"
                circle
              />
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.id">ID</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.name">组名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.users">用户</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.description">描述</el-checkbox>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>

        <el-table
          id="datatable"
          ref="releaseTable"
          v-loading="loading"
          border
          :data="groupTableData"
          style="width: 100% "
          :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}"
          @sort-change="sortChange"
          @filter-change="handleFilterChange"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="48" />
          <el-table-column v-if="column_rules.id" prop="id" label="ID" sortable width="80" />
          <el-table-column v-if="column_rules.name" prop="name" label="组名" width="120" />
          <el-table-column v-if="column_rules.users" prop="user_list" label="用户">
            <template slot-scope="scope">
              <el-tag v-for="user in scope.row.user_list" style="margin-right: 5px;">{{ user }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="column_rules.description" prop="description" label="描述" width="200" />
          <el-table-column label="操作" width="180">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                plain
                @click="handleEdit(scope)"
              >编辑
              </el-button>
              <el-button
                size="mini"
                type="warning"
                plain
                @click="handleDelete(scope)"
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
            :current-page="currentPage"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pageSize"
            :total="currentTotal"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>
    <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑':'新增'" :close-on-click-modal="false">
      <el-form ref="ruleForm" :model="settingInfo" :rules="rules" label-width="80px" label-position="left">
        <el-form-item label="组名" prop="name">
          <el-input v-model="settingInfo.name" placeholder="组名" />
        </el-form-item>
        <el-form-item label="用户">
          <el-select
            v-model="settingInfo.users"
            style="width: 100%"
            multiple
            filterable
            default-first-option
            placeholder="请输入用户名"
          >
            <el-option
              v-for="item in users"
              :key="item.bk_username"
              :label="item.bk_username"
              :value="item.bk_username"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="settingInfo.description"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
            placeholder="组描述"
          />
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogVisible=false">
          取消
        </el-button>
        <el-button type="primary" @click="confirmSetting">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'
import { addGroup, deleteGroup, getGroups, updateGroup } from '@/base/api/roleSetting'
import { getAllUserInfo } from '@/base/api/user'

const defaultSettingInfo = {
  id: 0,
  biz_id: 0,
  name: '',
  users: '',
  user_list: [],
  description: ''
}

export default {
  name: 'Role',
  components: {},
  computed: {
    ...mapGetters([
      'name',
      'role',
      'currBiz'
    ])
  },
  data() {
    return {
      show: false,
      timeout: null,
      loading: true,

      currentPage: 1,
      pageSize: 10,
      search_value: '',
      order_value: '-id',
      filter_name: '',
      currentTotal: 0,
      multipleSelection: [],
      multipleSelectionCount: 0,

      groupTableData: [],
      permissionObj: {},

      settingInfo: Object.assign({}, defaultSettingInfo),
      users: [],
      routes: [],
      roleSettings: [],
      dialogVisible: false,
      dialogType: 'new',
      checkStrictly: false,

      defaultProps: {
        children: 'children',
        label: 'title'
      },

      rules: {
        name: [
          { required: true, message: '请输入角色名', trigger: 'change' }
        ]
      },

      column_rules: {
        id: true,
        name: true,
        users: true,
        description: true
      }
    }
  },
  watch: {
    // 监听搜索框
    show(value) {
      if (value) {
        document.body.addEventListener('click', this.close)
      } else {
        document.body.removeEventListener('click', this.close)
      }
    },
    // 监听搜索改变
    search_value(curVal, oldVal) {
      // 实现input连续输入，只发一次请求
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.searchChange()
      }, 300)
    }
  },
  created() {
    this.getGroupTableDatas()
    this.getAllUsers()
  },
  methods: {
    // 刷新
    handleRefresh() {
      this.currentPage = 1
      this.getGroupTableDatas()
    },

    // 打开搜索功能
    click() {
      this.show = !this.show
      if (this.show) {
        this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
      }
    },

    // 关闭搜索功能
    close() {
      this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur()
      this.show = false
    },

    // 数据显示条数改变
    handleSizeChange(val) {
      this.currentPage = 1
      this.pageSize = val
      this.getGroupTableDatas()
    },

    // 当前页码改变
    handleCurrentChange(val) {
      this.currentPage = val
      this.getGroupTableDatas()
    },

    // 搜索
    searchChange() {
      this.currentPage = 1
      this.getGroupTableDatas()
    },

    // 多选
    handleSelectionChange(val) {
      this.multipleSelection = val
      this.multipleSelectionCount = this.multipleSelection.length
    },

    // 排序
    sortChange: function(column, prop, order) {
      if (column.order === 'ascending') {
        this.order_value = column.prop
      } else if (column.order === 'descending') {
        this.order_value = '-' + column.prop
      } else {
        this.order_value = ''
      }
      this.currentPage = 1
      this.getGroupTableDatas()
    },

    // 获取规则列表
    getGroupTableDatas() {
      this.loading = true
      getGroups({
        'page': this.currentPage,
        'page_size': this.pageSize,
        'search': this.search_value,
        'ordering': this.order_value,
        'biz_id': this.currBiz,
        'name': this.filter_name
      }).then(data => {
        this.currentTotal = data.count
        this.groupTableData = data.results
        this.loading = false
      })
    },

    // 根据DB设置, 生成用户select
    generateUsers(setting) {
      const genUsers = []
      if (setting) {
        JSON.parse(setting).forEach(user => {
          genUsers.push({
            bk_username: user
          })
        })
      }

      return genUsers
    },

    handleAdd() {
      this.settingInfo = Object.assign({}, defaultSettingInfo)
      try {
        this.$refs['ruleForm'].resetFields()
      } catch (e) {
      }
      this.dialogType = 'new'
      this.dialogVisible = true
    },

    handleEdit(scope) {
      this.dialogType = 'edit'
      this.dialogVisible = true
      this.settingInfo = deepClone(scope.row)
      this.settingInfo.users = JSON.parse(this.settingInfo.users)
    },

    // 删除
    handleDelete({ $index, row }) {
      this.$confirm('确定删除?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await deleteGroup(row.id)
        this.currentPage = 1
        await this.getGroupTableDatas()

        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
            <div>删除 :  ${row.name}</div>
          `,
          type: 'success'
        })
      }).catch(err => {
        console.error(err)
      })
    },

    // 批量删除
    handleMultipleDelete() {
      if (this.multipleSelection.length > 0) {
        this.$confirm('确定删除规则?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async() => {
          for (const i of this.multipleSelection) {
            await deleteGroup(i.id)
            this.currentPage = 1
            await this.getGroupTableDatas()
          }

          this.multipleSelection = []

          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }
        ).catch(err => {
          console.error(err)
        })
      } else {
        this.$message('请选择要删除的行.')
      }
    },

    async confirmSetting() {
      this.$refs['ruleForm'].validate(async(valid) => {
        var type = '添加'
        const isEdit = this.dialogType === 'edit'
        this.settingInfo.users = JSON.stringify(this.settingInfo.users)

        if (isEdit) {
          type = '更新'
          await updateGroup(this.settingInfo.id, this.settingInfo)
        } else {
          this.settingInfo.biz_id = this.currBiz
          await addGroup(this.settingInfo)
        }

        this.currentPage = 1
        this.getGroupTableDatas()

        const name = this.settingInfo.name
        this.dialogVisible = false
        this.$notify({
          title: 'Success',
          dangerouslyUseHTMLString: true,
          message: `
             <div>${type} :  ${name}</div>
          `,
          type: 'success'
        })
      })
    },

    getAllUsers() {
      getAllUserInfo().then(data => {
        this.users = data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .input-suffix {
    width: 180px;
  }

  #datatable > > > .el-checkbox__inner {
    width: 18px;
    height: 18px;

    &:after {
      border: 2px solid #fff;
      top: 3px;
      left: 6px;
      border-left: 0;
      border-top: 0;
    }
  }

  #datatable > > > .caret-wrapper {
    height: 20px;

    .sort-caret.ascending {
      top: -2px;
    }

    .sort-caret.descending {
      top: 10px;
      bottom: 0
    }
  }

  #datatable > > > .el-table__column-filter-trigger {
    line-height: 20px;
    float: right;
  }

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

  .header-search {
    display: inline-block;
    padding: 0 5px;
    height: 100%;
    color: #949494;
    vertical-align: text-bottom;

    &:hover {
      color: #1890ff
    }

    .search-icon {
      cursor: pointer;
      vertical-align: middle;
      margin-bottom: 6px;
    }

    .header-search-select {
      transition: width 0.2s;
      width: 0;
      overflow: hidden;
      background: transparent;
      border-radius: 0;
      display: inline-block;
      vertical-align: middle;

      /deep/ .el-input__inner {
        border-radius: 0;
        border: 0;
        padding-left: 0;
        padding-right: 0;
        box-shadow: none !important;
        border-bottom: 1px solid #d9d9d9;
        vertical-align: middle;
        background-color: transparent;
      }
    }

    &.show {
      .header-search-select {
        width: 210px;
        margin-left: 10px;
      }
    }
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

    &:hover {
      color: #1890ff
    }
  }

  .header-jump {
    background: transparent;
    border-style: none;
    outline: none;
    font-size: 20px;
    display: inline-block;
    padding: 0;
    height: 100%;
    color: #949494;
    font-weight: bold;
    vertical-align: text-bottom;
    margin-left: 5px;

    &:hover {
      color: #1890ff
    }
  }

  .permission-tree {
    margin-bottom: 30px;
  }
</style>

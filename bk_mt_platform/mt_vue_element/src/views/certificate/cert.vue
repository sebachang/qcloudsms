<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="alert alert-info help-message">
        创建或者更新证书,证书可以手动填写,也可以在选择自动生成.
      </div>
      <div class="clearfix">

        <div class="table-head-container">
          <div align="left" style="float:left">
            <el-button @click="handleAdd" icon="el-icon-circle-plus-outline" size="mini" type="primary" plain>
              添加
            </el-button>
            <el-button @click="handleMultipleDelete" icon="el-icon-delete" size="mini" type="danger" plain>删除
            </el-button>
            <p style="padding-left: 20px;display: inline;font-size: 13px;color: #999;">{{currentTotal}}个中
              {{multipleSelectionCount}} 个被选中</p>
          </div>
          <div align="right" class="right-menu">
            <div :class="{'show':show}" class="header-search">
              <svg-icon class-name="search-icon" icon-class="search" @click.stop="click"/>
              <el-input
                ref="headerSearchSelect"
                v-model="search_value"
                placeholder="搜索"
                class="header-search-select"
              >
              </el-input>
            </div>
            <el-button icon="el-icon-refresh" class="header-refresh" @click="handleRefresh" circle></el-button>
            <el-dropdown :hide-on-click="false" style="bottom: 5px">
              <el-button icon="el-icon-more-outline"
                         style="transform: rotate(90deg);background: transparent;border-style: none; outline: none; font-size: 18px;"
                         circle></el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.id">ID</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.domain">域名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.name">文件名</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.create_time">创建时间</el-checkbox>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-checkbox v-model="column_rules.expired_time">过期时间</el-checkbox>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>

        <el-table border id="datatable"
                  v-loading="loading"
                  ref="releaseTable"
                  :data="certTableData"
                  style="width: 100% "
                  @sort-change='sortChange'
                  @filter-change="handleFilterChange"
                  @selection-change="handleSelectionChange"
                  :header-cell-style="{background:'#f2f2f2',padding:'10px 0 10px 5px',color: '#666','font-size': '14px','font-weight': 400}"
                  :cell-style="{padding:'7px 0 7px 5px',color: '#666','font-size': '14px','font-weight': 400}">
          <el-table-column type="selection" width="48">
          </el-table-column>
          <el-table-column v-if="column_rules.id" prop="id" label="ID" sortable width="80">
          </el-table-column>
          <el-table-column v-if="column_rules.domain" prop="domain" label="域名" width="180">
          </el-table-column>
          <el-table-column v-if="column_rules.name" prop="name" label="文件名">
          </el-table-column>
          <el-table-column v-if="column_rules.create_time" prop="create_time" label="创建时间" sortable width="180">
          </el-table-column>
          <el-table-column v-if="column_rules.expired_time" prop="expired_time" label="过期时间" sortable  width="180"
                           column-key="expired_time">
          </el-table-column>
          <el-table-column label="操作" width="260">
            <template slot-scope="scope">
              <el-button plain size="mini" type="info" v-clipboard:success="handleClipboard"
                         v-clipboard:value="downloadUrl(scope)">
                下载连接
              </el-button>
              <el-button @click="handleEdit(scope)"
                         size="mini" type="primary" plain>编辑
              </el-button>
              <el-button @click="handleDelete(scope)"
                         size="mini"
                         type="warning" plain>删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div
          style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid">
          <el-pagination
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            layout="prev, pager, next, sizes, total, jumper"
            :current-page="currentPage"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pageSize"
            :total="currentTotal"
          >
          </el-pagination>
        </div>

        <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑':'添加'">

          <el-form :model="settingInfo" :rules="rules" ref="ruleForm" label-width="80px" label-position="left">

            <el-form-item label="方式">
              <el-radio-group v-model="radio">
                <el-radio :label="1">自动生成</el-radio>
                <el-radio :label="2">手动填写</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="域名" prop="domain">
              <el-input v-model="settingInfo.domain" placeholder="域名" v-if="radio_status===true">
                <el-button v-if="register_status===true" slot="append" icon="el-icon-loading" disabled>生成证书</el-button>
                <el-button v-else slot="append" icon="el-icon-edit" @click="handleRegistarCheck">生成证书</el-button>
              </el-input>
              <el-input v-model="settingInfo.domain" placeholder="域名" v-else></el-input>
            </el-form-item>

            <el-form-item label="文件名" prop="name">
              <el-input v-model="settingInfo.name" placeholder="集群发布时生成文件的名字"/>
            </el-form-item>

            <el-form-item label="创建时间" prop="create_time">
              <el-date-picker v-model="settingInfo.create_time" type="datetime" placeholder="选择创建时间"
                              :disabled="radio_status"></el-date-picker>
            </el-form-item>

            <el-form-item label="过期时间" prop="expired_time">
              <el-date-picker v-model="settingInfo.expired_time" type="datetime" placeholder="选择过期时间"
                              :disabled="radio_status"></el-date-picker>
            </el-form-item>

            <el-form-item label="CA证书" prop="ca">
              <el-input v-model="settingInfo.ca" type="textarea" :rows="4" placeholder="CA证书" :disabled="radio_status"/>
            </el-form-item>

            <el-form-item label="证书" prop="crt">
              <el-input v-model="settingInfo.crt" type="textarea" :rows="4" placeholder="证书" :disabled="radio_status"/>
            </el-form-item>

            <el-form-item label="秘钥" prop="key">
              <el-input v-model="settingInfo.key" type="textarea" :rows="4" placeholder="秘钥" :disabled="radio_status"/>
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
    </el-card>
  </div>
</template>

<script>
  const url = require('url');
  import {
    getCerts,
    deleteCert,
    addCert,
    updateCert,
    downloadCert,
    getAccountList,
    registerCert
  } from '@/api/certificate'
  import {get_download_site} from '@/base/api/appUtil'
  import {deepClone} from '@/base/utils'
  import Clipboard from '@/base/directive/clipboard/index'
  import {mapGetters} from 'vuex'

  const defaultSettingInfo = {
    bk_biz:0,
    domain: '',
    name: '',
    create_time: '',
    expired_time: '',
    ca: '',
    crt: '',
    key: '',
  };

  export default {
    name: "cert",
    components: {},
    directives: {Clipboard},
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

        register_status: false,
        radio: 1,
        radio_status: true,

        currentPage: 1,
        pageSize: 10,
        search_value: '',
        order_value: '-id',
        currentTotal: 0,
        multipleSelection: [],
        multipleSelectionCount: 0,

        certTableData: [],
        account_list: [],

        settingInfo: Object.assign({}, defaultSettingInfo),
        dialogVisible: false,
        dialogType: 'new',

        downloadSite: '',

        rules: {
          domain: [
            {required: true, message: '请输入域名', trigger: 'change'}
          ],
          create_time: [
            {required: true, message: '请输入创建时间', trigger: 'change'}
          ],
          expired_time: [
            {required: true, message: '请输入过期时间', trigger: 'change'}
          ],
          crt: [
            {required: true, message: '请输入证书', trigger: 'change'}
          ],
          key: [
            {required: true, message: '请输入秘钥', trigger: 'change'}
          ]
        },

        column_rules: {
          id: true,
          domain: true,
          name: true,
          create_time: true,
          expired_time: true
        },

      }
    },
    created() {
      this.getCertTableDatas();
      get_download_site().then(d => {
        this.downloadSite = d.site
      })
    },
    watch: {
      //监听搜索框
      show(value) {
        if (value) {
          document.body.addEventListener('click', this.close)
        } else {
          document.body.removeEventListener('click', this.close)
        }
      },

      radio(curVal, oldVal) {
        if (curVal === 2) {
          this.radio_status = false
        } else {
          this.radio_status = true
        }
      },

      //监听搜索改变
      search_value(curVal, oldVal) {
        // 实现input连续输入，只发一次请求
        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          this.searchChange();
        }, 300);
      }
    },
    methods: {
      handleRefresh() {
        this.currentPage = 1;
        this.getCertTableDatas();
      },

      // 获取账户列表
      getAccountListDatas() {
        getAccountList().then(data => {
          this.account_list = data
        })
      },

      //打开搜索功能
      click() {
        this.show = !this.show
        if (this.show) {
          this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
        }
      },

      //关闭搜索功能
      close() {
        this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur()
        this.options = []
        this.show = false
      },

      // 数据显示条数改变
      handleSizeChange(val) {
        this.currentPage = 1;
        this.pageSize = val;
        this.getCertTableDatas()
      },

      // 当前页码改变
      handleCurrentChange(val) {
        this.currentPage = val;
        this.getCertTableDatas()
      },

      // 搜索
      searchChange() {
        this.currentPage = 1;
        this.getCertTableDatas()
      },

      // 多选
      handleSelectionChange(val) {
        this.multipleSelection = val;
        this.multipleSelectionCount = this.multipleSelection.length;
      },

      // 排序
      sortChange: function (column, prop, order) {
        if (column.order === "ascending") {
          this.order_value = column.prop
        } else if (column.order === "descending") {
          this.order_value = '-' + column.prop
        } else {
          this.order_value = ''
        }
        this.currentPage = 1;
        this.getCertTableDatas()
      },

      // 获取证书表格数据
      getCertTableDatas() {
        this.loading = true;
        getCerts({
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.search_value,
          "ordering": this.order_value,
          "bk_biz": this.currBiz
        }).then(data => {
          this.currentTotal = data.count;
          this.certTableData = data.results;
          this.loading = false;
        })
      },

      //获取当前时间
      getDateTime() {
        var moment = require('moment');
        return moment().format("YYYY-MM-DD HH:mm:ss")
      },

      // 添加
      handleAdd() {
        this.settingInfo = Object.assign({}, defaultSettingInfo);
        this.settingInfo.bk_biz=this.currBiz;
        this.settingInfo.create_time = this.getDateTime();
        this.settingInfo.expired_time = this.getDateTime();
        try {
          this.$refs['ruleForm'].resetFields();
        } catch (e) {
        }
        this.dialogType = 'new';
        this.dialogVisible = true
      },

      // 批量删除
      handleMultipleDelete() {
        if (this.multipleSelection.length > 0) {
          this.$confirm('确定删除规则?', '警告', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(async () => {

              for (let i of this.multipleSelection) {
                await deleteCert(i.id);
                this.currentPage = 1;
                await this.getCertTableDatas()
              }

              this.multipleSelection = [];

              this.$message({
                type: 'success',
                message: '删除成功!'
              })

            }
          ).catch(err => {
            console.error(err)
          })
        } else {
          this.$message('请选择要删除的行.');
        }
      },

      // 编辑
      handleEdit(scope) {
        this.dialogType = 'edit';
        this.radio = 1;
        this.dialogVisible = true;
        this.settingInfo = deepClone(scope.row);
        try {
          this.$refs['ruleForm'].resetFields();
        } catch (e) {
        }
      },

      // 删除
      handleDelete({$index, row}) {
        this.$confirm('确定删除?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          await deleteCert(row.id);
          this.currentPage = 1;
          await this.getCertTableDatas();

          this.$notify({
            title: 'Success',
            dangerouslyUseHTMLString: true,
            message: `
            <div>删除 :  ${row.domain}</div>
          `,
            type: 'success'
          })
        }).catch(err => {
          console.error(err)
        })
      },

      // 添加 or 更新提交
      confirmSetting() {
        this.$refs['ruleForm'].validate(async (valid) => {
          if (valid) {
            const isEdit = this.dialogType === 'edit';
            var type = "添加";

            if (isEdit) {
              type = "更新";
              await updateCert(this.settingInfo.id, this.settingInfo)

            } else {
              await addCert(this.settingInfo)
            }

            this.currentPage = 1;
            this.getCertTableDatas();

            const title = this.settingInfo.domain;
            this.dialogVisible = false;
            this.$notify({
              title: 'Success',
              dangerouslyUseHTMLString: true,
              message: `
            <div>${type} :  ${title}</div>
          `,
              type: 'success'
            })
          }
        })
      },

      // 当talbel中任何一列的过滤条件点击确定和覆盖时，都会触发此事件。
      handleFilterChange(filters) {
        console.log(filters)
        // console.log('筛选条件发生变化')
        let row = null
        let val = null
        // 拷贝filters的值。
        for (const i in filters) {
          row = i // 保存 column-key的值，如果事先没有为column-key赋值，系统会自动生成一个唯一且恒定的名称
          val = filters[i]
        }
        const filter = [{
          row: row,
          op: 'contains',
          value: val
        }];
        console.log(filter)
      },

      async handleRegistarCheck() {
        if (this.settingInfo.domain) {
          this.register_status = true
          await registerCert({'domain': this.settingInfo.domain}).then(data => {
            if (data.result) {
              let cert = data.data
              this.settingInfo.crt = cert.crt
              this.settingInfo.key = cert.key
              this.settingInfo.create_time = cert.created
              this.settingInfo.expired_time = cert.expired
              this.$message({
                type: 'success',
                message: '证书生成成功!'
              })
              this.register_status = false
            } else {
              this.$message(data.message);
              this.register_status = false
            }
          })
        } else {
          this.$message('域名不能为空!.');
        }
      },

      downloadUrl(scope) {
        const base = process.env.VUE_APP_BASE_API
        let zipfile=scope.row.domain
        if (scope.row.name){
          zipfile=scope.row.name
        }
        return url.resolve(this.downloadSite, base + '/certificate/download/' + scope.row.id + '/'+zipfile+'.zip')
      },
      handleClipboard() {
        this.$message.success('已成功复制到剪贴板')
      },

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

  .header-download {
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

  .help-message {
    padding-left: 10px;
    font-size: 12px;
    line-height: 18px;
    margin-bottom: 0;
  }

  .alert-info {
    color: #31708f;
    background-color: #d9edf7;
    border-color: #bce8f1;
  }

  .alert {
    padding: 15px;
    border: 1px solid transparent;
    border-radius: 4px;
  }
</style>

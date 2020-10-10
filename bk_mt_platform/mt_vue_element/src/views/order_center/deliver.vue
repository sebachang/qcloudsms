<template>
  <div class="app-container">
    <el-tabs v-model="activeName">
      <el-tab-pane name="first"><span slot="label"><i class="el-icon-s-platform" /> 交付申请</span></el-tab-pane>
    </el-tabs>
    <el-form ref="form" :model="form" :rules="rules" label-width="60px">
      <el-card class="box-card">
        <el-form-item label="平台" prop="platform">
          <el-select v-model="form.platform" placeholder="请选择平台" size="small">
            <el-option
              v-for="item in form.userPlatformList"
              :key="item.id"
              :label="item.platform_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="机型" prop="host" size="small">
          <el-radio-group v-model="form.host">
            <el-radio-button
              v-for="btn of form.userPlatformHostList"
              :key="btn.id"
              :label="btn.id"
              @click.native="handleGetUserHostProfile(btn.id, btn.host_name)"
            >{{ btn.host_name }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="">
          <el-table
            :data="form.userHostList"
            size="small"
            style="width: 100%"
          >
            <el-table-column
              label="核心数"
              prop="cpu"
            />
            <el-table-column
              label="内存数"
              prop="mem"
            />
            <el-table-column
              label="系统盘"
              prop="sdisk"
            />
            <el-table-column
              label="机械硬盘"
              prop="disk"
            />
            <el-table-column
              label="固态硬盘"
              prop="ssd"
            />
            <el-table-column
              label="带宽"
              prop="net"
            />
            <el-table-column
              label="预估价格"
              prop="price"
            />
          </el-table>
        </el-form-item>
        <el-form-item label="机房" prop="center" size="small">
          <el-radio-group v-model="form.center">
            <el-radio-button
              v-for="btn1 of form.userPlatformCenterList"
              :key="btn1.id"
              :label="btn1.id"
              @click.native="handleGetUserCenter(btn1.id, btn1.center_name)"
            >{{ btn1.center_name }}
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
        <!--        <el-form-item label="网络">-->
        <!--        </el-form-item>-->
        <el-form-item label="系统" prop="system" size="small">
          <el-select v-model="form.system" placeholder="请选择系统">
            <el-option
              v-for="item in form.systemInfo"
              :key="item.value"
              :label="item.label"
              :value="item.label"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数量" size="small">
          <el-input-number v-model="form.num" :max="200" :min="1" label="描述文字" size="small" />
        </el-form-item>
        <el-form-item label="原因" prop="desc" size="small">
          <el-input v-model="form.desc" placeholder="请输入申请原因" size="small" style="width: 600px" />
        </el-form-item>
        <el-form-item label="备注" prop="remark" size="small">
          <el-input v-model="form.remark" type="textarea" :autosize="{ minRows: 2, maxRows: 6 }" placeholder="机器备注" size="small" style="width: 600px" />
        </el-form-item>
      </el-card>
      <div style="text-align:right;">
        <p />
        <el-form-item>
          <el-button size="small" type="primary" @click="submitForm('form')">立即创建</el-button>
          <el-button size="small" @click="resetForm('form')">重置</el-button>
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script>
import { getPlatformList } from '@/api/deliverManage'
import { getPlatfromHostList, getPlatfromCenterList } from '@/api/order_center/deliver'
import { postOrder } from '@/api/order_center/order'
import { mapGetters } from 'vuex'

const defaultOrderInfo = {
  order_type: '',
  biz_id: '',
  sub_order: {
    platform_id: '',
    host_id: '',
    center_id: '',
    vlan: '',
    system: '',
    amount: 1,
    desc: '',
    remark: ''
  }
}

export default {
  data() {
    return {
      activeName: 'first',
      settingInfo: Object.assign({}, defaultOrderInfo),
      form: {
        userPlatformList: [],
        userPlatformHostLists: {},
        userPlatformHostList: [],
        userHostList: [],
        userPlatformCenterLists: {},
        userPlatformCenterList: [],
        args: '',
        num: 1,
        platform: '',
        host: '',
        center: '',
        system: '',
        systemInfo: [{
          value: '1',
          label: 'CentOS 6'
        },
        {
          value: '2',
          label: 'CentOS 7'
        }],
        desc: '',
        remark: ''
      },
      tableData: [{
        cpu: '',
        mem: '',
        sdisk: '',
        disk: '',
        ssd: '',
        net: '',
        price: ''
      }],
      rules: {
        platform: [
          { required: true, message: '请选择平台', trigger: 'change' }
        ],
        host: [
          { required: true, message: '请选择机型', trigger: 'change' }
        ],
        center: [
          { required: true, message: '请选择机房', trigger: 'change' }
        ],
        system: [
          { required: true, message: '请选择系统', trigger: 'change' }
        ],
        desc: [
          { required: true, message: '请填写申请原因', trigger: 'blur' },
          { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
        ],
        remark: [
          { required: true, message: '请填写备注', trigger: 'blur' },
          { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'bizList',
      'currBiz'
    ])
  },
  watch: {
    'form.platform': function(val) {
      this.form.host = ''
      this.form.center = ''
      this.settingInfo.sub_order.platform_id = val
      this.form.userPlatformHostList = this.form.userPlatformHostLists[val]
      this.form.userHostList = this.tableData
      this.form.userPlatformCenterList = this.form.userPlatformCenterLists[val]
    }
  },
  created() {
    this.getUserPlatformLists()
  },
  methods: {
    getUserPlatformLists() {
      this.form.userHostList = this.tableData
      getPlatformList(this.currBiz).then(data => {
        for (var i = 0; i < data.length; i++) {
          if (data[i].state === 0) {
            this.form.userPlatformList.push(data[i])
          }
        }
        if (this.form.userPlatformList.length > 0) {
          for (var c = 0; c < this.form.userPlatformList.length; c++) {
            if (c === 0) {
              this.form.args = '?pid=' + this.form.userPlatformList[c].id + '&'
              continue
            }
            if (c === this.form.userPlatformList.length - 1) {
              this.form.args = this.form.args + 'pid=' + this.form.userPlatformList[c].id
            } else {
              this.form.args = this.form.args + 'pid=' + this.form.userPlatformList[c].id + '&'
            }
          }
          getPlatfromHostList(this.form.args).then(data => {
            this.form.userPlatformHostLists = data
          })
          getPlatfromCenterList(this.form.args).then(data1 => {
            this.form.userPlatformCenterLists = data1
          })
        }
      })
    },
    handleGetUserHostProfile(hid) {
      this.settingInfo.sub_order.host_id = hid
      for (var i = 0; i < this.form.userPlatformHostList.length; i++) {
        if (this.form.userPlatformHostList[i].id === hid) {
          this.form.userHostList = []
          this.form.userHostList.push(this.form.userPlatformHostList[i])
        }
      }
    },
    handleGetUserCenter(cid) {
      this.settingInfo.sub_order.center_id = cid
    },
    submitForm(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          this.settingInfo.sub_order.platform_id = this.form.platform
          this.settingInfo.sub_order.system = this.form.system
          this.settingInfo.sub_order.amount = this.form.num
          this.settingInfo.sub_order.desc = this.form.desc
          this.settingInfo.sub_order.remark = this.form.remark
          this.settingInfo.biz_id = this.currBiz
          this.settingInfo.order_type = 'deliver'
          postOrder(this.settingInfo).then(data => {
            if (data.id) {
              this.$notify({
                title: 'Success',
                dangerouslyUseHTMLString: true,
                message: `
                    <div>工单 : ${this.settingInfo.order_type}</div>
                  `,
                type: 'success'
              })
              this.$router.push('./order')
            }
          })
          // console.log(this.settingInfo)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(form) {
      for (var c = 0; c < this.form.userPlatformHostList.length; c++) {
        this.$delete(this.form.userPlatformHostList[c], 'isChange')
      }
      for (var i = 0; i < this.form.userPlatformCenterList.length; i++) {
        this.$delete(this.form.userPlatformCenterList[i], 'isChange1')
      }
      this.form.host = ''
      this.form.center = ''
      this.$refs[form].resetFields()
      this.form.userPlatformHostList = []
      this.form.userPlatformCenterList = []
      this.form.userHostList = this.tableData
      this.form.num = 1
    }
  }
}
</script>

<style lang="scss" scoped>
  .app-container {
    .roles-table {
      margin-top: 30px;
    }

    .permission-tree {
      margin-bottom: 30px;
    }
  }
</style>

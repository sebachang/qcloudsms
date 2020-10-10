<template>
  <el-drawer
    size="27.7%"
    :title="create ? '添加交付机器' : '编辑信息'"
    :append-to-body="true"
    :visible.sync="visible"
  >
    <el-container style="height: 900px; border: 1px solid #eee">
      <el-header style="padding-top: 10px;padding-right: 0.25em;padding-bottom: 2ex;background: #f2f2f2;">
        <div align="right">
          <el-button-group style="padding-top: 2px;margin-right: 70px">
            <el-tooltip class="item" effect="dark" content="提交" placement="bottom">
              <el-button type="primary" icon="el-icon-finished" @click="handleDeliverInfoCommit" />
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="关闭" placement="bottom">
              <el-button type="danger" icon="el-icon-circle-close" @click="handleClose" />
            </el-tooltip>
          </el-button-group>
        </div>
      </el-header>
      <el-container>
        <el-main>
          <el-card>
            <el-collapse v-model="activeNames1" accordion>
              <el-collapse-item title="基础信息" name="1">
                <el-input v-model="current.bk_host_innerip" size="mini">
                  <template slot="prepend">连接ip：</template>
                </el-input>
                <el-input v-model="current.bk_host_innerip" size="mini">
                  <template slot="prepend">内网ip：</template>
                </el-input>
                <el-input v-model="current.bk_host_outerip" size="mini">
                  <template slot="prepend">外网ip：</template>
                </el-input>
                <el-input v-model="current.password" size="mini">
                  <template slot="prepend">密码：</template>
                </el-input>
                <el-input v-model="current.bk_host_outerip_2" size="mini">
                  <template slot="prepend">外网ip数量：</template>
                </el-input>
                <el-input v-model="current.isp" size="mini">
                  <template slot="prepend">服务器供应商：</template>
                </el-input>
                <el-input v-model="current.server_country" size="mini">
                  <template slot="prepend">国家：</template>
                </el-input>
                <el-input v-model="current.server_city" size="mini">
                  <template slot="prepend">地区：</template>
                </el-input>
                <el-input v-model="current.bandwidth" size="mini">
                  <template slot="prepend">流量：</template>
                </el-input>
                <el-input v-model="current.price" size="mini">
                  <template slot="prepend">价格：</template>
                </el-input>
                <el-input v-model="current.disk_type" size="mini">
                  <template slot="prepend">磁盘类型：</template>
                </el-input>
                <el-input v-model="current.sl_account" size="mini">
                  <template slot="prepend">账号：</template>
                </el-input>
              </el-collapse-item>
              <el-collapse-item title="配置信息" name="2">
                <el-input v-model="current.bk_host_name" size="mini">
                  <template slot="prepend">主机名称：</template>
                </el-input>
                <el-input v-model="current.bk_os_type" size="mini">
                  <template slot="prepend">操作系统类型：</template>
                </el-input>
                <el-input v-model="current.bk_os_name" size="mini">
                  <template slot="prepend">操作系统名称：</template>
                </el-input>
                <el-input v-model="current.bk_os_version" size="mini">
                  <template slot="prepend">操作系统版本：</template>
                </el-input>
                <el-input v-model="current.bk_os_bit" size="mini">
                  <template slot="prepend">操作系统位数：</template>
                </el-input>
                <el-input v-model="current.bk_cpu" size="mini">
                  <template slot="prepend">cpu逻辑核心数：</template>
                </el-input>
                <el-input v-model="current.bk_cpu_mhz" size="mini">
                  <template slot="prepend">cpu频率：</template>
                </el-input>
                <el-input v-model="current.bk_cpu_module" size="mini">
                  <template slot="prepend">cpu型号：</template>
                </el-input>
                <el-input v-model="current.bk_mem" size="mini">
                  <template slot="prepend">内存容量：</template>
                </el-input>
                <el-input v-model="current.bk_disk" size="mini">
                  <template slot="prepend">磁盘容量：</template>
                </el-input>
                <el-input v-model="current.bk_mac" size="mini">
                  <template slot="prepend">内网mac地址：</template>
                </el-input>
                <el-input v-model="current.bk_outer_mac" size="mini">
                  <template slot="prepend">外网mac地址：</template>
                </el-input>
              </el-collapse-item>
              <el-collapse-item title="备注信息" name="3">
                <el-input v-model="current.bk_comment" size="mini">
                  <template slot="prepend">备注：</template>
                </el-input>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </el-drawer>
</template>

<script>
  import { addDeliverDetail, putDeliverDetail } from '@/api/deliverManage'

export default {
  name: 'DeliverInfoDrawer',
  data() {
    return {
      visible: false,
      current: {},
      activeNames1: '',
      create: false,
    }
  },
  methods: {
    show(current, create) {
      this.current = current
      this.visible = true
      this.create = create
    },
    handleDeliverInfoCommit() {
      if (this.create) {
        addDeliverDetail(this.current)
          .then(data => {
            this.$message({
              type: 'success',
              message: '成功!'
            })
            this.visible = false
          })
      } else {
        putDeliverDetail(this.current.id, this.current).then(data => {
          if (this.current.id === data.id) {
            this.$message({
              type: 'success',
              message: '成功!'
            })
            this.visible = false
          }
        })
      }
    },
    handleClose() {
      this.visible = false
    }
  }
}
</script>

<style scoped>

</style>

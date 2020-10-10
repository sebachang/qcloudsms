<template>
  <el-collapse v-model="activeName">
    <el-collapse-item v-for="item in detailFields" :name="item.name" :title="item.label">
      <div v-for="field in item.children" style="font-size:12px;">
        {{ field.label }}：<span class="dd-info" v-if="data !== undefined">{{ data && data[field.prop] }}</span>
      </div>
    </el-collapse-item>
  </el-collapse>
</template>

<script>
export default {
  name: 'HostDetail',
  props: {
    data: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return  {
      activeName: "1",
      detailFields: [
        { label: '基础信息', name: '1', children: [
          { 'label': '连接ip', prop: 'bk_host_innerip' },
          { 'label': '内网ip', prop: 'bk_host_innerip' },
          { 'label': '外网ip', prop: 'bk_host_outerip' },
          { 'label': '外网ip数量', prop: 'bk_host_outerip_2' },
          { 'label': '服务器供应商', prop: 'isp' },
          { 'label': '国家', prop: 'server_country' },
          { 'label': '地区', prop: 'server_city' },
          { 'label': '流量', prop: 'bandwidth' },
          { 'label': '价格', prop: 'price' },
          { 'label': '磁盘类型', prop: 'disk_type' },
          { 'label': '录入时间', prop: 'create_time' },
          { 'label': '账号', prop: 'sl_account' },
          { 'label': '密码', prop: 'password' }
        ] },
        { label: '配置信息', name: '2', children: [
          { label: '主机名称', prop: 'bk_host_name' },
          { label: '操作系统类型', prop: 'bk_os_type' },
          { label: '操作系统名称', prop: 'bk_os_name' },
          { label: '操作系统版本', prop: 'bk_os_version' },
          { label: '操作系统位数', prop: 'bk_os_bit' },
          { label: 'cpu逻辑核心数', prop: 'bk_cpu' },
          { label: 'cpu频率', prop: 'bk_cpu_mhz' },
          { label: 'cpu型号', prop: 'bk_cpu_module' },
          { label: '内存容量', prop: 'bk_mem' },
          { label: '磁盘容量', prop: 'bk_disk' },
          { label: '内网mac地址', prop: 'bk_mac' },
          { label: '外网mac地址', prop: 'bk_outer_mac' }
        ] },
        { label: '备注信息', name: '3', children: [
          { label: '备注', prop: 'bk_comment' }
        ] }
      ],

    }
  },
  mounted() {
    this.activeName = "1"
  }
}
</script>

<style scoped>

</style>

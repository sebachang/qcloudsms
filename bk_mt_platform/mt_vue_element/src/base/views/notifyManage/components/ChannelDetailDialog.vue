<template>
  <el-dialog :append-to-body="appendToBody" :visible.sync="visible" title="创建通道" width="600px">
    <el-form label-position="left">
      <el-form-item label="名称" label-width="100px">
        <el-input v-model="record.name" />
      </el-form-item>
      <el-form-item label="类型" label-width="100px">
        <el-select v-model="record.type">
          <el-option label="钉钉" value="dingtalk" />
        </el-select>
      </el-form-item>
      <el-form-item label="钉钉token" label-width="100px">
        <el-input v-model="record.params.token" :disabled="record.type !== 'dingtalk'" />
      </el-form-item>
      <el-form-item label="钉钉关键词" label-width="100px">
        <el-input
          v-model="record.params.keyword"
          :disabled="record.type !== 'dingtalk'"
          placeholder="钉钉机器人关键词，会被插入到每条消息的开头"
        />
      </el-form-item>
      <el-form-item label="是否开启" label-width="100px">
        <el-switch v-model="record.enabled" />
      </el-form-item>
      <el-form-item>
        <div style="float: right">
          <el-button type="danger" @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleConfirm">确定</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { addChannel, updateChannel } from '@/base/api/notifyManage'
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'

export default {
  name: 'ChannelDetailDialog',
  props: {
    appendToBody: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      visible: false,
      create: false,
      record: { params: {}}
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  methods: {
    show(data) {
      if (data) {
        this.create = false
        this.record = deepClone(data)
      } else {
        this.create = true
        this.record = { biz_id: this.currBiz, params: {}, enabled: false }
      }
      this.visible = true
    },
    handleCancel() {
      this.visible = false
    },
    handleConfirm() {
      if (this.create) {
        addChannel(this.record)
          .then(data => {
            this.visible = false
            this.$emit('confirm')
          })
      } else {
        updateChannel(this.currBiz, this.record.id, this.record)
          .then(() => {
            this.visible = false
            this.$emit('confirm')
          })
      }
    }
  }
}
</script>

<style scoped>

</style>

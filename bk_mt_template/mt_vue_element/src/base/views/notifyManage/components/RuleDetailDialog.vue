<template>
  <el-dialog :append-to-body="appendToBody" :visible.sync="visible" title="创建规则" width="40em">
    <el-form label-position="left">
      <el-form-item label="名称" label-width="100px">
        <el-input v-model="record.name" />
      </el-form-item>
      <el-form-item label="包含tags" label-width="100px">
        <el-select v-model="record.tags" multiple style="width: 100%">
          <el-option v-for="tag in tags" :key="tag.key" :label="tag.name" :value="tag.key" />
        </el-select>
      </el-form-item>
      <el-form-item label="消息类型" label-width="100px">
        <el-select v-model="record.types" multiple style="width: 100%">
          <el-option
            v-for="t in types"
            :key="t.id"
            :label="t.name"
            :value="t.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="目标通道" label-width="100px">
        <el-select v-model="record.destination" multiple style="width: 100%">
          <el-option v-for="channel in channels" :key="channel.id" :label="channel.name" :value="channel.id" />
        </el-select>
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
import { addRule, getChannels, getTags, updateRule } from '@/base/api/notifyManage'
import { mapGetters } from 'vuex'
import { deepClone } from '@/base/utils'

export default {
  name: 'RuleDetailDialog',
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
      record: {},
      tags: [],
      channels: [],
      types: [{
        name: '通知',
        id: 1
      }, {
        name: '警告',
        id: 2
      }]
    }
  },
  computed: {
    ...mapGetters(['currBiz'])
  },
  methods: {
    show(data) {
      if (data) {
        this.record = deepClone(data)
        this.create = false
      } else {
        this.record = { biz_id: this.currBiz, tags: [], types: [], destination: [] }
        this.create = true
      }
      this.visible = true
      this.reloadData()
    },
    reloadData() {
      getChannels(this.currBiz)
        .then(data => {
          this.channels = data
        })
      getTags()
        .then(data => {
          this.tags = data
        })
    },
    handleCancel() {
      this.visible = false
    },
    handleConfirm() {
      this.record.tags.sort()
      this.record.types.sort()
      this.record.destination.sort()
      if (this.create) {
        addRule(this.record)
          .then(data => {
            this.visible = false
            this.$emit('confirm')
          })
      } else {
        updateRule(this.currBiz, this.record.id, this.record)
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

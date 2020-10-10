<template>
  <div class="app-container">
    <el-card>
      <div class="datatable-head-container">
        <el-button icon="el-icon-upload" plain size="mini" type="primary" @click="showUploadForm()">上传程序包</el-button>
        <div style="float: right">
          <el-button circle class="el-icon-refresh rounded-button" @click="reloadPackages" />
        </div>
      </div>
      <el-table :data="packages" border cell-class-name="datatable-cell" header-cell-class-name="datatable-header">
        <el-table-column label="包名" prop="Key" />
        <el-table-column label="大小" prop="Size" />
        <el-table-column label="上传日期" prop="LastModified" />
        <el-table-column label="操作">
          <template slot="header" />
          <template slot-scope="{row}">
            <el-button plain size="mini" @click="download(row)">下载</el-button>
            <el-button plain size="mini" type="danger" @click="removeFile(row)">删除</el-button>
          </template>

        </el-table-column>
      </el-table>

      <el-dialog :close-on-click-modal="false" :visible.sync="uploadVisible" title="上传程序包">
        <el-form>
          <el-form-item label="选择文件">
            <input ref="file" type="file" @change="handleFileChange">
          </el-form-item>
          <el-form-item label="文件名">
            <el-input v-model="uploadForm.filename" />
          </el-form-item>
          <el-form-item>
            <el-button @click="handleUpload">上传</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'
import { parseString } from 'xml2js'
import { numberFormatter } from '@/base/filters'
import { deletePackage, getPackageList, uploadPackage } from '@/api/processManage'
import { downloadPackage } from '../../api/processManage'
import saveAs from 'file-saver'

export default {
  name: 'Package',
  data() {
    return {
      files: [],
      uploadVisible: false,
      filename: '',
      uploadForm: {
        filename: ''
      }
    }
  },
  computed: {
    ...mapGetters(['currBiz']),
    packages() {
      return this.files.filter((s) => !String(s.Key).endsWith('/')).map((s) => {
        s.Size = numberFormatter(s.Size, 2)
        const parts = String.prototype.split.call(s.Key, ['/'])
        s.Key = parts[parts.length - 1]
        return s
      })
    }
  },
  created() {
    this.reloadPackages()
  },
  methods: {
    reloadPackages() {
      getPackageList(this.currBiz)
        .then((res) => {
          parseString(res.content, (err, result) => {
            if (err !== null) {
              this.$message({ type: 'error', message: '获取包列表失败' })
              return
            }
            this.files = result.ListBucketResult.Contents || []
          })
        })
    },
    download(row) {
      downloadPackage(this.currBiz, row.Key)
        .then((data) => {
          window.open(data, '_blank')
        })
    },
    removeFile(row) {
      this.$confirm(`确定删除程序包${row.Key}吗？`)
        .then(() => {
          deletePackage(this.currBiz, row.Key).then((res) => {
            this.$message({ 'message': '成功删除文件', type: 'success' })
            this.reloadPackages()
          })
        })
    },
    showUploadForm() {
      this.uploadVisible = true
    },
    handleUpload() {
      const f = new FormData()
      f.append('file', this.$refs.file.files[0])
      f.append('key', this.$refs.file.files[0].name)
      uploadPackage(this.currBiz, f)
        .then(() => {
          this.uploadVisible = false
          this.reloadPackages()
        })
    },
    handleFileChange() {
      this.uploadForm.filename = this.$refs.file.files[0].name
    }
  }
}
</script>

<style lang="scss" scoped>
  .rounded-button {
    outline: none;
    border: none;
    background: transparent;
  }
</style>

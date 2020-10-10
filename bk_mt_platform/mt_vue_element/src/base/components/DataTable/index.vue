<template>
  <div>
    <div>
      <div class="datatable-head-container">
        <div align="left" style="display: inline-block">
          <slot name="header" />
        </div>
        <div style="display: inline-block; float: right">
          <search-box @enter="handleSearch" />
          <el-button circle class="plain-button" icon="el-icon-refresh" @click="reload()" />
        </div>
      </div>
    </div>
    <el-table
      ref="table"
      v-loading="loading"
      :data="rows"
      border
      cell-class-name="datatable-cell"
      header-cell-class-name="datatable-header"
      @selection-change="$emit('selection-change', $event)"
    >
      <slot />
    </el-table>
    <div
      style="height: 50px; margin-bottom: 10px; padding: 10px;line-height: 22px;border-radius: 0 0 4px 4px;border-color: #dfe6ec;border-width:0 1px 1px 1px;border-style:solid"
    >
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="[5, 10, 15, 20]"
        :total="currentTotal"
        background
        layout="prev, pager, next, sizes, total, jumper"
        @current-change="reload()"
        @size-change="reload()"
      />
    </div>
  </div>
</template>

<script>
import SearchBox from '@/base/components/SearchBox/index'

export default {
  name: 'DataTable',
  components: { SearchBox },
  props: {
    load: {
      type: Function,
      default: null
    },
    disableSearch: {
      type: Boolean,
      default: false
    },
    disablePagination: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loading: false,
      rows: [],
      show: false,
      currentTotal: 0,
      currentPage: 1,
      search: '',
      pageSize: 10
    }
  },
  watch: {
    load() {
      this.reload()
    }
  },
  async created() {
    await this.reload()
  },
  methods: {
    async reload(page) {
      if (!Number.isInteger(page)) {
        page = this.currentPage
      }
      if (this.load) {
        this.loading = true
        const options = {
          page: page,
          page_size: this.pageSize
        }
        if (!this.disableSearch) {
          options.search = this.search
        }

        const { results, count } = await this.load(options)
        this.loading = false
        this.currentTotal = count
        this.rows = results
      }
    },
    handleSearch(keyword) {
      this.search = keyword
      this.reload(1)
    }
  }
}
</script>

<style lang="scss">
  .plain-button {
    background: none;
    border: none;

    &:hover {
      background: none;
    }
  }
</style>

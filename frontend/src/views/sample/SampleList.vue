<template>
  <div class="sample-list-container">
    <div class="toolbar" style="margin-bottom: 20px;">
      <el-input v-model="search" placeholder="Search content..." style="width: 200px; margin-right: 10px;" />
      <el-button type="primary" icon="Search" @click="fetchSamples(1)">Search</el-button>
      <el-button type="success" icon="Plus" @click="handleAdd">Add Sample</el-button>
    </div>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="content" label="Content" show-overflow-tooltip />
      <el-table-column prop="source" label="Source" width="120" />
      <el-table-column prop="language" label="Lang" width="80" />
      <el-table-column prop="label" label="Label" width="100">
        <template #default="{ row }">
          <el-tag>{{ row.label }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 20px;"
      layout="prev, pager, next"
      :total="total"
      :current-page="page"
      :page-size="pageSize"
      @current-change="fetchSamples"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { sampleService } from '@/services/modules'

const search = ref('')
const tableData = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const fetchSamples = async (p = page.value) => {
  page.value = p
  try {
    const res: any = await sampleService.getSamples({
      page: page.value,
      limit: pageSize.value,
      query: search.value
    })
    const data = res?.data?.data || res?.data
    tableData.value = data.items || data.samples || []
    total.value = data.total || 0
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

const handleDelete = async (row: any) => {
  try {
    await sampleService.deleteSample(row.id)
    ElMessage.success('删除成功')
    await fetchSamples(1)
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑样本 #${row.id} 尚未实现`)
}

const handleAdd = () => {
  ElMessage.info('新增样本尚未实现')
}

onMounted(() => {
  fetchSamples(1)
})
</script>

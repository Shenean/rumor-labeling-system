<template>
  <div class="review-task-list">
    <el-card header="待审核任务">
      <el-button type="primary" style="margin-bottom: 16px;" @click="fetchTasks" :loading="loading">
        刷新
      </el-button>
      <el-table :data="tasks" border>
        <el-table-column prop="id" label="任务ID" width="90" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="status" label="状态" width="140" />
        <el-table-column prop="completed" label="已标注" width="120" />
        <el-table-column prop="total" label="总数" width="120" />
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="goDetail(row)">审核</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/services/api'

const router = useRouter()
const loading = ref(false)
const tasks = ref<any[]>([])

const fetchTasks = async () => {
  loading.value = true
  try {
    const res: any = await api.get('/review/tasks', { params: { page: 1, limit: 50 } })
    const data = res?.data?.data || res?.data
    tasks.value = data.items || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const goDetail = (row: any) => {
  router.push(`/review/tasks/${row.id}`)
}

onMounted(() => {
  fetchTasks()
})
</script>


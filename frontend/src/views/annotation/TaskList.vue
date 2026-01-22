<template>
  <div class="task-list-container">
    <el-card>
      <template #header>
        <div class="header">
          <span>My Annotation Tasks</span>
          <el-button type="primary" @click="fetchTasks" :loading="loading">Refresh</el-button>
        </div>
      </template>
      
      <el-table :data="tasks" border>
        <el-table-column prop="id" label="Task ID" width="80" />
        <el-table-column prop="name" label="Task Name" />
        <el-table-column prop="status" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'done' ? 'success' : 'warning'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Action">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="startLabeling(row)">Start Labeling</el-button>
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
import { taskService } from '@/services/modules'

const router = useRouter()
const tasks = ref<any[]>([])
const loading = ref(false)

const fetchTasks = async () => {
  loading.value = true
  try {
    const res: any = await taskService.getTasks({ page: 1, limit: 50 })
    const data = res?.data?.data || res?.data
    tasks.value = data.items || []
  } catch (e) {
    ElMessage.error('加载任务失败')
  } finally {
    loading.value = false
  }
}

const startLabeling = (row: any) => {
  router.push({ path: '/annotation/workspace', query: { taskId: String(row.id) } })
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

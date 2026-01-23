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
        <el-table-column prop="assignee_id" label="Assignee" width="120" />
        <el-table-column prop="status" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'done' ? 'success' : 'warning'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Action">
          <template #default="{ row }">
            <el-button v-if="!row.assignee_id" size="small" @click="claim(row)" :loading="claimingId === row.id">
              Claim
            </el-button>
            <el-button type="primary" size="small" @click="startLabeling(row)" :disabled="row.assignee_id && row.assignee_id !== userId">
              Start Labeling
            </el-button>
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
import 'element-plus/es/components/message/style/css'
import { taskService } from '@/services/modules'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const tasks = ref<any[]>([])
const loading = ref(false)
const claimingId = ref<number | null>(null)
const userId = Number(userStore.userInfo?.id || 0)

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

const claim = async (row: any) => {
  claimingId.value = row.id
  try {
    await taskService.claimTask(row.id)
    ElMessage.success('领取成功')
    await fetchTasks()
  } catch (e) {
    ElMessage.error('领取失败')
  } finally {
    claimingId.value = null
  }
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

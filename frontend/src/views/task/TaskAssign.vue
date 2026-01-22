<template>
  <div class="task-assign-page">
    <el-card header="任务分配">
      <div style="display:flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px;">
        <el-button type="primary" :loading="loading.tasks" @click="fetchTasks">刷新任务</el-button>
        <el-button type="success" @click="dialogVisible = true">创建任务</el-button>
      </div>

      <el-table :data="tasks" border>
        <el-table-column prop="id" label="任务ID" width="90" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="status" label="状态" width="140" />
        <el-table-column prop="assignee_id" label="标注员ID" width="120" />
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="创建任务" width="640px">
      <el-form label-position="top">
        <el-form-item label="任务名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
        <el-form-item label="指派标注员">
          <el-select v-model="form.assigneeId" style="width: 100%;" placeholder="请选择用户">
            <el-option v-for="u in users" :key="u.id" :label="`${u.username} (#${u.id})`" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择样本">
          <el-select v-model="form.sampleIds" multiple filterable style="width: 100%;" placeholder="请选择样本">
            <el-option v-for="s in samples" :key="s.id" :label="`#${s.id} ${s.content?.slice(0, 20)}`" :value="s.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="loading.create" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { sampleService, settingsService, taskService } from '@/services/modules'

const tasks = ref<any[]>([])
const users = ref<any[]>([])
const samples = ref<any[]>([])
const dialogVisible = ref(false)
const loading = reactive({ tasks: false, users: false, samples: false, create: false })

const form = reactive({
  name: '',
  description: '',
  assigneeId: null as number | null,
  sampleIds: [] as number[]
})

const fetchTasks = async () => {
  loading.tasks = true
  try {
    const res: any = await taskService.getTasks({ page: 1, limit: 100 })
    const data = res?.data?.data || res?.data
    tasks.value = data.items || []
  } catch (e) {
    ElMessage.error('加载任务失败')
  } finally {
    loading.tasks = false
  }
}

const fetchUsers = async () => {
  loading.users = true
  try {
    const res: any = await settingsService.getUsers({ page: 1, limit: 200 })
    const data = res?.data?.data || res?.data
    users.value = data.items || []
  } catch (e) {
    ElMessage.error('加载用户失败')
  } finally {
    loading.users = false
  }
}

const fetchSamples = async () => {
  loading.samples = true
  try {
    const res: any = await sampleService.getSamples({ page: 1, limit: 200 })
    const data = res?.data?.data || res?.data
    samples.value = data.items || []
  } catch (e) {
    ElMessage.error('加载样本失败')
  } finally {
    loading.samples = false
  }
}

const handleCreate = async () => {
  if (!form.name) {
    ElMessage.warning('请输入任务名称')
    return
  }
  loading.create = true
  try {
    await taskService.createTask({
      name: form.name,
      description: form.description,
      sample_ids: form.sampleIds,
      assignees: form.assigneeId ? [form.assigneeId] : []
    })
    ElMessage.success('创建成功')
    dialogVisible.value = false
    form.name = ''
    form.description = ''
    form.assigneeId = null
    form.sampleIds = []
    await fetchTasks()
  } catch (e) {
    ElMessage.error('创建失败')
  } finally {
    loading.create = false
  }
}

onMounted(() => {
  fetchTasks()
  fetchUsers()
  fetchSamples()
})
</script>


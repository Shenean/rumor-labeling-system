<template>
  <div class="review-task-detail">
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span>任务审核 #{{ taskId }}</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <div v-if="loading">Loading...</div>
      <div v-else>
        <el-table :data="samples" border>
          <el-table-column prop="id" label="样本ID" width="90" />
          <el-table-column prop="content" label="内容" show-overflow-tooltip />
          <el-table-column prop="label" label="最终标签" width="140" />
        </el-table>

        <div style="margin-top: 16px; display:flex; gap: 12px;">
          <el-input v-model="comments" placeholder="审核意见（可选）" />
          <el-button type="success" :loading="submitting" @click="submit(true)">通过</el-button>
          <el-button type="danger" :loading="submitting" @click="submit(false)">驳回</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const taskId = computed(() => Number(route.params.id))
const loading = ref(false)
const submitting = ref(false)
const samples = ref<any[]>([])
const comments = ref('')

const fetchDetail = async () => {
  loading.value = true
  try {
    const res: any = await api.get(`/review/tasks/${taskId.value}`)
    const data = res?.data?.data || res?.data
    samples.value = data.samples || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const submit = async (approved: boolean) => {
  submitting.value = true
  try {
    await api.post(`/review/tasks/${taskId.value}`, { approved, comments: comments.value })
    ElMessage.success('操作成功')
    router.push('/review/tasks')
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchDetail()
})
</script>

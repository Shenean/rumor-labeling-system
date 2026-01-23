<template>
  <div class="event-list-container">
    <el-card header="Event Clustering">
      <el-button type="primary" style="margin-bottom: 20px;" :loading="clustering" @click="handleCluster">
        Run Clustering Algorithm
      </el-button>

      <el-table :data="events" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="Title" />
        <el-table-column prop="status" label="Status" width="140" />
        <el-table-column prop="sample_count" label="Samples" width="120" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { eventService } from '@/services/modules'

const events = ref<any[]>([])
const clustering = ref(false)

const fetchEvents = async () => {
  try {
    const res: any = await eventService.getEvents()
    const data = res?.data?.data || res?.data
    events.value = data.items || data.events || []
  } catch (e) {
    ElMessage.error('加载事件失败')
  }
}

const handleCluster = async () => {
  clustering.value = true
  try {
    await eventService.clusterEvents()
    ElMessage.success('聚合完成')
    await fetchEvents()
  } catch (e) {
    ElMessage.error('聚合失败')
  } finally {
    clustering.value = false
  }
}

onMounted(() => {
  fetchEvents()
})
</script>

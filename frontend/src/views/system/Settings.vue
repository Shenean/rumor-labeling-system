<template>
  <div class="settings-page">
    <el-card header="系统设置">
      <div style="margin-bottom: 12px;">
        <el-button type="primary" :loading="loading.config" @click="fetchConfig">刷新配置</el-button>
        <el-button type="primary" :loading="loading.logs" @click="fetchLogs" style="margin-left: 8px;">刷新日志</el-button>
      </div>

      <el-divider>配置</el-divider>
      <el-input v-model="configText" type="textarea" :rows="6" />
      <el-button type="success" style="margin-top: 8px;" :loading="loading.save" @click="saveConfig">保存</el-button>

      <el-divider style="margin-top: 16px;">操作日志</el-divider>
      <el-table :data="logs" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_id" label="用户ID" width="90" />
        <el-table-column prop="method" label="方法" width="90" />
        <el-table-column prop="path" label="路径" />
        <el-table-column prop="status_code" label="状态" width="90" />
        <el-table-column prop="created_at" label="时间" width="190" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { settingsService } from '@/services/modules'

const loading = ref({ config: false, save: false, logs: false })
const configText = ref('{}')
const logs = ref<any[]>([])

const fetchConfig = async () => {
  loading.value.config = true
  try {
    const res: any = await settingsService.getConfig()
    const data = res?.data?.data || res?.data
    configText.value = JSON.stringify(data || {}, null, 2)
  } catch (e) {
    ElMessage.error('加载配置失败')
  } finally {
    loading.value.config = false
  }
}

const saveConfig = async () => {
  loading.value.save = true
  try {
    const payload = JSON.parse(configText.value || '{}')
    await settingsService.updateConfig(payload)
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    loading.value.save = false
  }
}

const fetchLogs = async () => {
  loading.value.logs = true
  try {
    const res: any = await settingsService.getLogs({ page: 1, limit: 50 })
    const data = res?.data?.data || res?.data
    logs.value = data.items || []
  } catch (e) {
    ElMessage.error('加载日志失败')
  } finally {
    loading.value.logs = false
  }
}

onMounted(() => {
  fetchConfig()
  fetchLogs()
})
</script>

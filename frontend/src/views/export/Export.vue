<template>
  <div class="export-page">
    <el-card header="导出报表">
      <div style="display:flex; gap: 12px; flex-wrap: wrap;">
        <el-button type="primary" :loading="loading.samples" @click="downloadSamples">导出样本</el-button>
        <el-button type="primary" :loading="loading.annotations" @click="downloadAnnotations">导出标注</el-button>
        <el-button type="primary" :loading="loading.audits" @click="downloadAudits">导出审核记录</el-button>
        <el-button type="success" :loading="loading.report" @click="downloadReport">导出汇总报表</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { exportService } from '@/services/modules'

const loading = reactive({
  samples: false,
  annotations: false,
  audits: false,
  report: false
})

const saveBlob = (blob: Blob, filename: string) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  window.URL.revokeObjectURL(url)
}

const downloadSamples = async () => {
  loading.samples = true
  try {
    const res: any = await exportService.exportSamples()
    saveBlob(res.data, 'samples_export.xlsx')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    loading.samples = false
  }
}

const downloadAnnotations = async () => {
  loading.annotations = true
  try {
    const res: any = await exportService.exportAnnotations()
    saveBlob(res.data, 'annotations_export.xlsx')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    loading.annotations = false
  }
}

const downloadAudits = async () => {
  loading.audits = true
  try {
    const res: any = await exportService.exportAudits()
    saveBlob(res.data, 'audits_export.xlsx')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    loading.audits = false
  }
}

const downloadReport = async () => {
  loading.report = true
  try {
    const res: any = await exportService.exportReports({ type: 'summary' })
    saveBlob(res.data, 'report_summary.xlsx')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    loading.report = false
  }
}
</script>


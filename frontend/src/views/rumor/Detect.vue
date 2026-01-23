<template>
  <div class="rumor-detect-container">
    <el-card header="Rumor Detection">
      <el-form>
        <el-form-item label="Input Text">
          <el-input
            v-model="text"
            type="textarea"
            :rows="6"
            placeholder="Please input text to detect..."
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleDetect" :loading="loading">Detect</el-button>
          <el-button @click="text = ''">Clear</el-button>
        </el-form-item>
      </el-form>

      <div v-if="result" class="result-box">
        <el-divider>Result</el-divider>
        <el-descriptions title="Prediction Info" border>
          <el-descriptions-item label="Label">
            <el-tag :type="result.label === 'Real' ? 'success' : 'danger'">{{ result.label }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Confidence">{{ result.confidence }}%</el-descriptions-item>
          <el-descriptions-item label="Model">BERT-Base-Chinese</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { rumorService } from '@/services/modules'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'

const text = ref('')
const loading = ref(false)
const result = ref<any>(null)

const handleDetect = async () => {
  if (!text.value) return
  loading.value = true
  try {
    const res: any = await rumorService.detect(text.value)
    const data = res?.data?.data || res?.data
    const confidence = data?.confidence ?? 0
    result.value = {
      label: data?.label,
      confidence: (Number(confidence) * 100).toFixed(2)
    }
    ElMessage.success('Detection Complete')
  } catch (e) {
    ElMessage.error('Detection Failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.result-box {
  margin-top: 20px;
}
</style>

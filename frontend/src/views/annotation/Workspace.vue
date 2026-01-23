<template>
  <div class="workspace-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card header="Content to Label">
          <div class="content-box">
            <div v-if="loading">Loading...</div>
            <div v-else-if="currentSample">
              <p>{{ currentSample.content }}</p>
              <p>Source: {{ currentSample.source || '-' }}</p>
              <p>Language: {{ currentSample.language || '-' }}</p>
            </div>
            <div v-else>No sample</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="Annotation Tool">
          <el-form label-position="top">
            <el-form-item label="Label">
              <el-radio-group v-model="label">
                <el-radio label="Real" border>Real</el-radio>
                <el-radio label="Rumor" border>Rumor</el-radio>
                <el-radio label="Unverified" border>Unverified</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Comment">
              <el-input v-model="comment" type="textarea" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" style="width: 100%;" :loading="submitting" @click="handleSubmit">
                Submit & Next
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { annotationService, taskService } from '@/services/modules'

const route = useRoute()
const label = ref('')
const comment = ref('')
const loading = ref(false)
const submitting = ref(false)
const samples = ref<any[]>([])
const currentIndex = ref(0)

const taskId = computed(() => Number(route.query.taskId || 0))
const currentSample = computed(() => samples.value[currentIndex.value])

const fetchSamples = async () => {
  if (!taskId.value) return
  loading.value = true
  try {
    const res: any = await taskService.getTaskSamples(taskId.value)
    const data = res?.data?.data || res?.data
    samples.value = Array.isArray(data) ? data : []
    currentIndex.value = 0
  } catch (e) {
    ElMessage.error('加载样本失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!taskId.value || !currentSample.value) return
  if (!label.value) {
    ElMessage.warning('请选择标签')
    return
  }
  submitting.value = true
  try {
    await annotationService.submitTaskSampleLabel(taskId.value, currentSample.value.id, {
      label: label.value,
      comments: comment.value
    })
    ElMessage.success('提交成功')
    label.value = ''
    comment.value = ''
    if (currentIndex.value < samples.value.length - 1) {
      currentIndex.value += 1
    } else {
      await fetchSamples()
    }
  } catch (e) {
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchSamples()
})
</script>

<style scoped>
.content-box {
  font-size: 16px;
  line-height: 1.6;
  min-height: 300px;
}
</style>

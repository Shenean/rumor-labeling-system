<template>
  <div class="workspace-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card header="Content to Label">
          <div class="content-box">
            <p>This is a sample text that needs to be labeled. It contains some claims that might be rumors.</p>
            <p>Source: Social Media</p>
            <p>Date: 2023-10-01</p>
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
              <el-button type="primary" style="width: 100%;">Submit & Next</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const label = ref('')
const comment = ref('')
</script>

<style scoped>
.content-box {
  font-size: 16px;
  line-height: 1.6;
  min-height: 300px;
}
</style>

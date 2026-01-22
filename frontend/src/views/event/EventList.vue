<template>
  <div class="event-list-container">
    <el-card header="Event Clustering">
      <el-button type="primary" style="margin-bottom: 20px;">Run Clustering Algorithm</el-button>
      
      <el-collapse accordion>
        <el-collapse-item title="Event: Earthquake Rumors (5 samples)" name="1">
          <el-table :data="event1" size="small">
             <el-table-column prop="content" label="Content" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="Event: Celebrity Scandal (12 samples)" name="2">
          <div>...</div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup lang="ts">
const event1 = [
  { content: 'Did you feel the shake?' },
  { content: 'Earthquake in city center!' },
]
</script>

<template>
  <div class="task-list-container">
    <el-card>
      <template #header>
        <div class="header">
          <span>My Annotation Tasks</span>
          <el-button type="primary">Refresh</el-button>
        </div>
      </template>
      
      <el-table :data="tasks" border>
        <el-table-column prop="id" label="Task ID" width="80" />
        <el-table-column prop="name" label="Task Name" />
        <el-table-column prop="status" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'done' ? 'success' : 'warning'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Action">
          <template #default>
            <el-button type="primary" size="small" @click="$router.push('/annotation/workspace')">Start Labeling</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
const tasks = [
  { id: 101, name: 'Batch #1 Weibo Data', status: 'pending' },
  { id: 102, name: 'Batch #2 Twitter Data', status: 'done' },
]
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

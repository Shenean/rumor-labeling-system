<template>
  <div class="sample-list-container">
    <div class="toolbar" style="margin-bottom: 20px;">
      <el-input v-model="search" placeholder="Search content..." style="width: 200px; margin-right: 10px;" />
      <el-button type="primary" icon="Search">Search</el-button>
      <el-button type="success" icon="Plus">Add Sample</el-button>
    </div>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="content" label="Content" show-overflow-tooltip />
      <el-table-column prop="source" label="Source" width="120" />
      <el-table-column prop="language" label="Lang" width="80" />
      <el-table-column prop="rumor_label" label="Label" width="100">
        <template #default="{ row }">
          <el-tag>{{ row.rumor_label }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="180">
        <template #default>
          <el-button size="small">Edit</el-button>
          <el-button size="small" type="danger">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 20px;"
      layout="prev, pager, next"
      :total="100"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const search = ref('')
const tableData = [
  { id: 1, content: 'Some rumor content example 1...', source: 'Weibo', language: 'zh', rumor_label: 'Rumor' },
  { id: 2, content: 'Official news release...', source: 'News', language: 'zh', rumor_label: 'Real' },
  { id: 3, content: 'Suspicious post...', source: 'Twitter', language: 'en', rumor_label: 'Pending' },
]
</script>

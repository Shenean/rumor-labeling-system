<template>
  <div class="user-list-container">
    <el-button type="primary" style="margin-bottom: 20px;">Add User</el-button>
    <el-table :data="users" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="Username" />
      <el-table-column prop="role" label="Role" />
      <el-table-column prop="email" label="Email" />
      <el-table-column label="Actions">
        <template #default>
          <el-button size="small">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
const users = [
  { id: 1, username: 'admin', role: 'admin', email: 'admin@example.com' },
  { id: 2, username: 'user1', role: 'annotator', email: 'user1@example.com' },
]
</script>

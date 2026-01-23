<template>
  <div class="user-list-container">
    <el-button type="primary" style="margin-bottom: 20px;" @click="handleAdd">Add User</el-button>
    <el-table :data="users" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="Username" />
      <el-table-column prop="role" label="Role" />
      <el-table-column prop="email" label="Email" />
      <el-table-column label="Actions">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { settingsService } from '@/services/modules'

const users = ref<any[]>([])

const fetchUsers = async () => {
  try {
    const res: any = await settingsService.getUsers({ page: 1, limit: 50 })
    const data = res?.data?.data || res?.data
    users.value = data.items || []
  } catch (e) {
    ElMessage.error('加载用户失败')
  }
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑用户 #${row.id} 尚未实现`)
}

const handleAdd = () => {
  ElMessage.info('新增用户尚未实现')
}

onMounted(() => {
  fetchUsers()
})
</script>

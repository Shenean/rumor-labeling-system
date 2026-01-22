<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>{{ $t('message.hello') }}</h2>
      </template>
      <el-form :model="form" ref="formRef" :rules="rules" label-position="top">
        <el-form-item :label="$t('common.username')" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item :label="$t('common.password')" prop="password">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" @click="handleLogin" :loading="loading">
            {{ $t('common.login') }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="tips">
        <p>Admin: admin / any</p>
        <p>User: user / any</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { authService } from '@/services/modules'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)

const form = reactive({
  username: 'admin',
  password: '123'
})

const rules = {
  username: [{ required: true, trigger: 'blur' }],
  password: [{ required: true, trigger: 'blur' }]
}

const handleLogin = async () => {
  loading.value = true
  try {
    const res: any = await authService.login(form)
    userStore.setToken(res.data.token)
    userStore.setUserInfo(res.data.user)
    ElMessage.success('Login Success')
    router.push('/dashboard')
  } catch (error) {
    ElMessage.error('Login Failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2d3a4b;
}
.login-card {
  width: 400px;
}
.tips {
  font-size: 12px;
  color: #666;
  margin-top: 10px;
}
</style>

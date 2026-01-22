<template>
  <el-menu
    :default-active="activeMenu"
    class="el-menu-vertical"
    background-color="#304156"
    text-color="#bfcbd9"
    active-text-color="#409EFF"
    router
  >
    <el-menu-item index="/dashboard">
      <el-icon><Odometer /></el-icon>
      <template #title>{{ $t('menu.dashboard') }}</template>
    </el-menu-item>

    <el-menu-item index="/rumor/detect">
      <el-icon><Aim /></el-icon>
      <template #title>{{ $t('menu.rumor') }}</template>
    </el-menu-item>

    <el-menu-item index="/samples">
      <el-icon><Document /></el-icon>
      <template #title>{{ $t('menu.samples') }}</template>
    </el-menu-item>

    <el-menu-item index="/annotation/tasks">
      <el-icon><EditPen /></el-icon>
      <template #title>{{ $t('menu.annotation') }}</template>
    </el-menu-item>

    <el-menu-item index="/events">
      <el-icon><Connection /></el-icon>
      <template #title>{{ $t('menu.events') }}</template>
    </el-menu-item>

    <el-sub-menu index="/system" v-if="userStore.isAdmin">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>{{ $t('menu.system') }}</span>
      </template>
      <el-menu-item index="/system/users">{{ $t('menu.users') }}</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'

const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => {
  return route.path
})
</script>

<style scoped>
.el-menu-vertical {
  height: 100vh;
  border-right: none;
}
</style>

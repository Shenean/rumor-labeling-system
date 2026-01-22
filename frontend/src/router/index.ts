import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'
import Layout from '@/layout/Layout.vue'

const routes = [
  {
    path: '/login',
    component: () => import('@/views/login/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue')
      },
      {
        path: 'rumor/detect',
        name: 'RumorDetection',
        component: () => import('@/views/rumor/Detect.vue')
      },
      {
        path: 'samples',
        name: 'SampleList',
        component: () => import('@/views/sample/SampleList.vue')
      },
      {
        path: 'annotation/tasks',
        name: 'TaskList',
        component: () => import('@/views/annotation/TaskList.vue')
      },
      {
        path: 'annotation/workspace',
        name: 'AnnotationWorkspace',
        component: () => import('@/views/annotation/Workspace.vue')
      },
      {
        path: 'events',
        name: 'EventList',
        component: () => import('@/views/event/EventList.vue')
      },
      {
        path: 'system/users',
        name: 'UserList',
        component: () => import('@/views/system/UserList.vue'),
        meta: { roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.public) {
    next()
  } else {
    if (userStore.isLoggedIn) {
      if (to.meta.roles && !(to.meta.roles as string[]).includes(userStore.role)) {
        next('/dashboard') // No permission
      } else {
        next()
      }
    } else {
      next('/login')
    }
  }
})

export default router

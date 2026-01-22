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
        path: 'tasks/assign',
        name: 'TaskAssign',
        component: () => import('@/views/task/TaskAssign.vue'),
        meta: { roles: ['admin'] }
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
        path: 'review/tasks',
        name: 'TaskReviewList',
        component: () => import('@/views/review/TaskReviewList.vue'),
        meta: { roles: ['admin', 'reviewer'] }
      },
      {
        path: 'review/tasks/:id',
        name: 'TaskReviewDetail',
        component: () => import('@/views/review/TaskReviewDetail.vue'),
        meta: { roles: ['admin', 'reviewer'] }
      },
      {
        path: 'review/events',
        name: 'EventReviewList',
        component: () => import('@/views/review/EventReviewList.vue'),
        meta: { roles: ['admin', 'reviewer'] }
      },
      {
        path: 'review/events/:id',
        name: 'EventReviewDetail',
        component: () => import('@/views/review/EventReviewDetail.vue'),
        meta: { roles: ['admin', 'reviewer'] }
      },
      {
        path: 'export',
        name: 'Export',
        component: () => import('@/views/export/Export.vue'),
        meta: { roles: ['admin'] }
      },
      {
        path: 'system/users',
        name: 'UserList',
        component: () => import('@/views/system/UserList.vue'),
        meta: { roles: ['admin'] }
      },
      {
        path: 'system/settings',
        name: 'SystemSettings',
        component: () => import('@/views/system/Settings.vue'),
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

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import store from './store'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: 'zh',
  fallbackLocale: 'en',
  messages: {
    zh: {
      message: { hello: '欢迎使用谣言标注系统' },
      menu: {
        dashboard: '仪表盘',
        rumor: '谣言检测',
        samples: '样本管理',
        tasks: '任务分配',
        annotation: '标注任务',
        review: '标注审核',
        events: '事件聚合',
        export: '导出报表',
        system: '系统管理',
        users: '用户管理'
      },
      common: {
        search: '搜索',
        add: '新增',
        edit: '编辑',
        delete: '删除',
        submit: '提交',
        cancel: '取消',
        login: '登录',
        logout: '退出登录',
        username: '用户名',
        password: '密码'
      }
    },
    en: {
      message: { hello: 'Welcome to Rumor Labeling System' },
      menu: {
        dashboard: 'Dashboard',
        rumor: 'Rumor Detect',
        samples: 'Sample Mgmt',
        tasks: 'Task Assign',
        annotation: 'Annotation',
        review: 'Review',
        events: 'Events',
        export: 'Export',
        system: 'System',
        users: 'Users'
      },
      common: {
        search: 'Search',
        add: 'Add',
        edit: 'Edit',
        delete: 'Delete',
        submit: 'Submit',
        cancel: 'Cancel',
        login: 'Login',
        logout: 'Logout',
        username: 'Username',
        password: 'Password'
      }
    }
  }
})

const app = createApp(App)

app.use(router)
app.use(store)
app.use(i18n)

app.mount('#app')

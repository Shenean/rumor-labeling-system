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
    zh: { message: { hello: '欢迎使用谣言标注系统' } },
    en: { message: { hello: 'Welcome to Rumor Labeling System' } }
  }
})

const app = createApp(App)

app.use(router)
app.use(store)
app.use(i18n)
app.mount('#app')

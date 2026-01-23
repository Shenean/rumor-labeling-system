import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendHost = env.VITE_BACKEND_HOST || env.BACKEND_HOST || 'localhost'
  const backendPort = env.VITE_BACKEND_PORT || env.BACKEND_PORT || '5000'
  const backendProtocol = env.VITE_BACKEND_PROTOCOL || env.BACKEND_PROTOCOL || 'http'
  const backendTarget = `${backendProtocol}://${backendHost}:${backendPort}`

  return {
    plugins: [
      vue(),
      AutoImport({
        resolvers: [ElementPlusResolver()]
      }),
      Components({
        resolvers: [ElementPlusResolver({ importStyle: 'css' })]
      })
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    server: {
      proxy: {
        '/api': {
          target: backendTarget,
          changeOrigin: true
        }
      }
    }
  }
})
